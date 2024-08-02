#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import os
import sys

import tomllib


class SpecsRegistry:
    """Load the index of Freedesktop specifications."""

    def __init__(self, root_dir):
        self._root_dir = root_dir

        self.spec_index = []

    def load(self) -> bool:
        # read the specification index
        with open(os.path.join(self._root_dir, 'spec-index.toml'), 'rb') as f:
            spec_info_index = tomllib.load(f)
        with open(os.path.join(self._root_dir, 'spec-revs.toml'), 'rb') as f:
            spec_revs = tomllib.load(f)

        # sanity check
        for spec_name in spec_revs.keys():
            if spec_name not in spec_info_index:
                print(
                    'ERROR:',
                    'Spec "{}" not found in spec-index.toml'.format(spec_name),
                    file=sys.stderr,
                )
                return False
        for spec_name, spec_info in spec_info_index.items():
            if spec_info.get('externally_managed'):
                continue
            if spec_name not in spec_revs:
                print(
                    'ERROR:',
                    'No version of spec "{}" found in spec-revs.toml'.format(spec_name),
                    file=sys.stderr,
                )
                return False

        # create our index
        self.spec_index = []
        for spec_name, spec_info in spec_info_index.items():
            revs = spec_revs.get(spec_name, [])
            self.spec_index.append(dict(name=spec_name, info=spec_info, revs=revs))

        return True
