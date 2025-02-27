#
# Copyright (C) 2024-2025 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+

import os
import shutil
import tempfile

from sphinx.application import Sphinx


def sphinx_make_html(
    spec_dir,
    output_dir,
) -> bool:
    """Build HTML from reStructured Text using Sphinx."""

    with tempfile.TemporaryDirectory() as doctree_tmp:
        sphinx = Sphinx(
            srcdir=spec_dir,
            confdir=spec_dir,
            outdir=output_dir,
            doctreedir=doctree_tmp,
            buildername="html",
        )
        sphinx.build()
