#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import os
import sys
import shutil
import subprocess
from contextlib import contextmanager

from .git import GitObject
from .utils import temp_dir


class Daps:
    def __init__(self):
        self._style_root = None
        self._daps_exe = shutil.which('daps')
        if not self._daps_exe:
            raise RuntimeError('"daps" is not installed - please install it to continue!')

    @property
    def style_root(self):
        return self._style_root

    @style_root.setter
    def style_root(self, value):
        self._style_root = value

    @contextmanager
    def _make_daps_workspace(self, spec_files):
        with temp_dir() as tdir:
            xml_target = os.path.join(tdir, 'xml')
            os.makedirs(xml_target, exist_ok=True)

            # copy files into a structure that DAPS likes
            for fname in spec_files:
                shutil.copy(os.path.join('spec', fname), xml_target)

            yield xml_target

    def validate(self, xml_files, validate_tables=True) -> bool:
        with self._make_daps_workspace(xml_files) as dws:
            # validate
            for fname in xml_files:
                fname_base = os.path.basename(fname)
                print('➤', 'Validating:', fname_base)

                cmd = [self._daps_exe, '-m', os.path.join(dws, fname_base), 'validate']
                if not validate_tables:
                    cmd.append('--not-validate-tables')

                res = subprocess.run(cmd, check=False)
                if res.returncode != 0:
                    return False
        return True

    def make_html(
        self,
        book_name,
        spec_files,
        output_dir,
        book_filename: str | None = None,
        single=True,
        draft=False,
        validate_tables=True,
    ) -> bool:
        git_objects = [item for item in spec_files if isinstance(item, GitObject)]
        spec_in_files = [item for item in spec_files if not isinstance(item, GitObject)]
        if not book_filename:
            book_filename = book_name + '.xml'

        with self._make_daps_workspace(spec_in_files) as dws:
            # save Git objects
            for o in git_objects:
                o.fetch()
                tmp_book_fname = os.path.join(dws, book_filename)
                with open(tmp_book_fname, 'wb') as f:
                    f.write(o.data)

            cmd = [self._daps_exe]
            if self._style_root:
                cmd.extend(['--styleroot', self._style_root])
            cmd.extend(
                [
                    '-m',
                    os.path.join(dws, book_filename),
                    'html',
                    '--name',
                    book_name,
                ]
            )
            if single:
                cmd.append('--single')
            if draft:
                cmd.append('--draft')
            if not validate_tables:
                cmd.append('--not-validate-tables')

            res = subprocess.run(cmd, check=False)
            if res.returncode != 0:
                return False

            if single:
                result_path = os.path.join(
                    dws,
                    '..',
                    'build',
                    book_name,
                    'single-html',
                    book_name + '_draft' if draft else book_name,
                )
            else:
                result_path = os.path.join(
                    dws,
                    '..',
                    'build',
                    book_name,
                    'html',
                    book_name + '_draft' if draft else book_name,
                )
            if not os.path.exists(result_path):
                raise RuntimeError('DAPS succeeded, but we could not find any generated data!')

            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            for fname in list(os.listdir(result_path)):
                target_fname = os.path.join(output_dir, fname)
                if os.path.exists(target_fname):
                    if os.path.isdir(target_fname):
                        shutil.rmtree(target_fname)
                    else:
                        os.remove(target_fname)
                shutil.move(os.path.join(result_path, fname), output_dir)

        return True
