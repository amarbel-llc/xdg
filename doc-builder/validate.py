#!/usr/bin/env python3
#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import os
import sys
from glob import glob

from xdgspecbuild import Daps, GitObject, SpecsRegistry, TemplateRenderer
from xdgspecbuild.utils import print_section_title


class SpecValidator:
    """Helper to build the Freedesktop specification website."""

    def __init__(self, script_dir):
        self._root_dir = os.path.realpath(os.path.join(script_dir, '..'))
        self._daps = Daps()

    def load(self) -> bool:
        """Load the specification index and revisions."""

        registry = SpecsRegistry(self._root_dir)
        if not registry.load():
            return False
        self.spec_index = registry.spec_index

        return True

    def process(self) -> bool:
        """Process all specifications and generate the website."""

        for spec_data in self.spec_index:
            spec_revs = spec_data['revs']
            spec_name = spec_data['name']
            spec_info = spec_data['info']
            spec_format = spec_info.get('format', 'docbook')

            if spec_info.get('externally_managed'):
                print('Skip: "{}" (externally managed)'.format(spec_name))
                continue
            if not spec_info.get('local'):
                print('Skip: "{}" (not local)'.format(spec_name))
                continue
            if not spec_revs:
                print('Skip: "{}" (no revisions)'.format(spec_name))
                continue

            print_section_title(spec_name)

            rev_processed = False
            for spec_rev in spec_revs:
                rev_type = spec_rev.get('type', 'spec')
                rev_ver = spec_rev.get('version')
                if not rev_ver:
                    raise ValueError('No version specified for spec "{}"'.format(spec_name))
                if spec_rev.get('gitrev') != 'HEAD':
                    continue
                if rev_type != 'spec':
                    continue
                if spec_format != 'docbook':
                    print(
                        'Skip validating "{}" (can\'t validate "{}" documents yet)'.format(
                            spec_name, spec_format
                        )
                    )
                    continue

                spec_location = spec_rev.get(
                    'location', spec_info.get('location', '{0}/{0}-spec.xml'.format(spec_name))
                )
                spec_location_root = os.path.dirname(os.path.join(self._root_dir, spec_location))
                book_filename = os.path.basename(spec_location)

                xml_files = glob(os.path.join(spec_location_root, '*.xml'))
                if not self._daps.validate(
                    xml_files, book_filename=book_filename, validate_tables=False
                ):
                    return False
                rev_processed = True

            if rev_processed:
                print()

        return True


def run(script_dir, args):

    validator = SpecValidator(script_dir)
    if not validator.load():
        return 5
    if not validator.process():
        return 1
    return 0


if __name__ == '__main__':
    thisfile = os.path.realpath(__file__)
    if not os.path.isabs(thisfile):
        thisfile = os.path.normpath(os.path.join(os.getcwd(), thisfile))
    thisdir = os.path.normpath(os.path.join(os.path.dirname(thisfile)))
    os.chdir(thisdir)

    sys.exit(run(thisdir, sys.argv[1:]))
