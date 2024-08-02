#!/usr/bin/env python3
#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import os
import sys
import shutil
import datetime
import subprocess
from glob import glob

from xdgspecbuild import Daps, GitObject, SpecsRegistry, TemplateRenderer
from xdgspecbuild.utils import print_section_title


class FdoSpecBuilder:
    """Helper to build the Freedesktop specification website."""

    def __init__(self, script_dir):
        self._root_dir = os.path.normpath(os.path.join(script_dir, '..'))
        self._output_root = os.path.join(self._root_dir, 'public')

        self._templates = TemplateRenderer(os.path.join(script_dir, 'templates'))
        self._daps = Daps()
        self._daps.style_root = os.path.join(script_dir, 'fdo-style')

        self.spec_index = []

    def load(self) -> bool:
        """Load the specification index and revisions."""

        registry = SpecsRegistry(self._root_dir)
        if not registry.load():
            return False
        self.spec_index = registry.spec_index

        return True

    def _run_makefile(self, spec_name: str, spec_info, spec_rev, *, command: str | None = None):
        """Run Makefile for a subproject, if one exists."""

        spec_location_root = spec_rev.get('location', spec_info.get('location', spec_name))

        project_root = spec_info.get('project_root', None)
        if project_root:
            project_root = os.path.join(self._root_dir, project_root)
        else:
            project_root = spec_location_root

        # run Makefile if one exists to generate any files
        if os.path.exists(os.path.join(project_root, 'Makefile')):
            if spec_info.get('make_commands', None) is None:
                args = ['make', '-C', project_root]
                if command:
                    args.append(command)
                subprocess.run(
                    args,
                    check=True,
                )
            return True
        return False

    def _create_spec_html(self, spec_name: str, spec_info, spec_rev) -> bool:
        """Render HTML page from a DocBook specification."""

        spec_ver = spec_rev.get('version')
        spec_gitrev = spec_rev.get('gitrev')
        spec_is_local = spec_info.get('local', False)
        makefile_run = False

        spec_out_root = os.path.join(self._output_root, spec_name + '-spec')
        os.makedirs(spec_out_root, exist_ok=True)

        spec_versioned_out_basename = os.path.join(
            spec_out_root, '{}-spec-{}'.format(spec_name, spec_ver)
        )
        spec_location = spec_rev.get(
            'location', spec_info.get('location', '{0}/{0}-spec.xml'.format(spec_name))
        )
        book_filename = spec_name + '-spec.xml'

        if spec_ver == 'latest' or spec_gitrev == 'HEAD':
            if spec_is_local:
                spec_location_root = os.path.dirname(os.path.join(self._root_dir, spec_location))
                book_filename = os.path.basename(spec_location)

                # build any specification data that we may need
                makefile_run = self._run_makefile(spec_name, spec_info, spec_rev)

                # find all XML files that we want to render
                spec_files = glob(os.path.join(spec_location_root, '*.xml'))

                if len(spec_files) == 1:
                    shutil.copy(
                        spec_files[0],
                        os.path.join(spec_out_root, '{}-spec-latest.xml'.format(spec_name)),
                    )
            else:
                spec_doc = GitObject(
                    spec_info['gitweb'],
                    spec_location,
                    spec_rev.get('gitrev'),
                )
                spec_files = [spec_doc]

            self._templates.render_to_file(
                'simple-redirect.html', os.path.join(spec_out_root, 'index.html'), url='latest/'
            )
            if spec_ver != 'latest':
                latest_symlink = os.path.join(spec_out_root, 'latest')
                if os.path.islink(latest_symlink):
                    os.unlink(latest_symlink)
                os.symlink(spec_ver, latest_symlink)

        else:
            spec_doc = GitObject(
                spec_info['gitweb'],
                spec_location,
                spec_rev.get('gitrev'),
            )
            spec_doc.fetch()
            with open(spec_versioned_out_basename + '.xml', mode='wb') as f:
                f.write(spec_doc.data)
            spec_files = [spec_doc]

        # create redirect to keep older links working
        self._templates.render_to_file(
            'simple-redirect.html', spec_versioned_out_basename + '.html', url=spec_ver + '/'
        )

        # render DocBook XML to HTML
        print('\033[1m➤', 'Generating:', spec_name, spec_ver, '\033[0m')
        spec_ver_out_dir = os.path.join(spec_out_root, spec_ver)
        ret = self._daps.make_html(
            spec_name,
            spec_files,
            spec_ver_out_dir,
            book_filename=book_filename,
            single=spec_rev.get('single_page', spec_info.get('single_page', False)),
            validate_tables=False,
            draft=spec_info.get('draft', False),
        )
        if not ret:
            print('ERROR:', 'Failed to generate HTML for', spec_name, spec_ver, file=sys.stderr)
            return False

        spec_out_static_dir = os.path.join(spec_ver_out_dir, 'static')
        if os.path.islink(spec_out_static_dir):
            os.unlink(spec_out_static_dir)
        elif os.path.exists(spec_out_static_dir):
            shutil.rmtree(spec_out_static_dir)
        os.symlink(
            os.path.relpath(os.path.join(self._output_root, 'static'), spec_ver_out_dir),
            spec_out_static_dir,
        )

        # clean up if we executed a Makefile
        if makefile_run:
            self._run_makefile(spec_name, spec_info, spec_rev, command='clean')

        return True

    def _copy_spec_aux_data(self, spec_name: str, spec_info, file_rev) -> bool:
        """Copy some auxiliary data needed for a specification to a specific location."""

        file_gitrev = file_rev.get('gitrev', 'HEAD')
        file_from = file_rev['from']
        file_to = file_rev['to']
        spec_dirname = file_rev.get('export_root', spec_name)

        if not file_from or not file_to:
            raise ValueError(
                'Missing "from" or "to" in copy-file revision for "{}"'.format(spec_name)
            )

        fname_dst = os.path.join(self._output_root, spec_dirname, file_to)
        os.makedirs(os.path.dirname(fname_dst), exist_ok=True)

        if spec_info.get('local', False) and file_gitrev == 'HEAD':
            fname_src = os.path.dirname(os.path.join(self._root_dir, file_from))
            shutil.copy(fname_src, fname_dst)
            print('\033[1m➤', 'Copied:\033[0m', file_to, '(from {})'.format(file_from))
        else:
            file_remote = GitObject(
                spec_info['gitweb'],
                file_from,
                file_gitrev,
            )
            file_remote.fetch()
            with open(fname_dst, 'wb') as f:
                f.write(file_remote.data)
            print(
                '\033[1m➤',
                'Copied:\033[0m',
                file_to,
                '(from {} @ {})'.format(spec_info['gitweb'], file_gitrev),
            )

        return True

    def _copy_spec_data_dir(self, spec_name: str, spec_info, dir_rev) -> bool:
        """Copy a local directory with data, e.g. for a spec with a separate build system."""

        dir_from = dir_rev['from']
        dir_to = dir_rev['to']
        treat_as_spec = dir_rev.get('treat_as_spec', False)
        spec_dirname = dir_rev.get('export_root', spec_name)

        if not dir_from or not dir_to:
            raise ValueError(
                'Missing "from" or "to" in copy-dir revision for "{}"'.format(spec_name)
            )

        if treat_as_spec:
            spec_dirname = spec_name + '-spec'

        # we may need to build the data to copy first
        makefile_run = self._run_makefile(spec_name, spec_info, dir_rev)

        dir_dst = os.path.join(self._output_root, spec_dirname, dir_to)
        os.makedirs(os.path.dirname(dir_dst), exist_ok=True)

        dir_src = os.path.dirname(os.path.join(self._root_dir, dir_from))
        shutil.copytree(dir_src, dir_dst, dirs_exist_ok=True)
        print('\033[1m➤', 'Copied:\033[0m', dir_to, '(from {})'.format(dir_from))

        if treat_as_spec:
            self._templates.render_to_file(
                'simple-redirect.html',
                os.path.join(os.path.join(self._output_root, spec_dirname), 'index.html'),
                url='latest/',
            )

        # clean up if we executed a Makefile
        if makefile_run:
            self._run_makefile(spec_name, spec_info, dir_rev, command='clean')

        return True

    def process(self) -> bool:
        """Process all specifications and generate the website."""

        for spec_data in self.spec_index:
            spec_revs = spec_data['revs']
            spec_name = spec_data['name']
            spec_info = spec_data['info']

            if not spec_revs:
                continue
            print_section_title(spec_name)

            for spec_rev in spec_revs:
                rev_type = spec_rev.get('type', 'spec')
                rev_ver = spec_rev.get('version')
                if not rev_ver:
                    raise ValueError('No version specified for spec "{}"'.format(spec_name))

                if rev_type == 'spec':
                    if not self._create_spec_html(spec_name, spec_info, spec_rev):
                        return False
                elif rev_type == 'copy-file':
                    if not self._copy_spec_aux_data(spec_name, spec_info, spec_rev):
                        return False
                elif rev_type == 'copy-dir':
                    if not self._copy_spec_data_dir(spec_name, spec_info, spec_rev):
                        return False
                else:
                    raise ValueError(
                        'Encountered unknown revision type for "{}": {}'.format(spec_name, rev_type)
                    )

        self._templates.render_to_file(
            'index.html',
            os.path.join(self._output_root, 'index.html'),
            specifications=self.spec_index,
            current_year=datetime.datetime.now().year,
            path_basename=os.path.basename,
        )
        shutil.copytree(
            os.path.join(self._daps.style_root, 'static'),
            os.path.join(self._output_root, 'static'),
            dirs_exist_ok=True,
        )
        favicon_fname = os.path.join(self._output_root, 'favicon.ico')
        if os.path.exists(favicon_fname):
            os.unlink(favicon_fname)
        os.symlink('static/images/favicon.ico', favicon_fname)

        return True


def run(script_dir, args):

    builder = FdoSpecBuilder(script_dir)
    if not builder.load():
        return 5
    if not builder.process():
        return 1
    return 0


if __name__ == '__main__':
    thisfile = os.path.realpath(__file__)
    if not os.path.isabs(thisfile):
        thisfile = os.path.normpath(os.path.join(os.getcwd(), thisfile))
    thisdir = os.path.normpath(os.path.join(os.path.dirname(thisfile)))
    os.chdir(thisdir)

    sys.exit(run(thisdir, sys.argv[1:]))
