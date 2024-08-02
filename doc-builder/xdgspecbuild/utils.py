#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import io
import os
import sys
import shutil
import hashlib
from contextlib import contextmanager

from jinja2 import Environment, FileSystemLoader

HASH = 'md5'


@contextmanager
def temp_dir(basename=None):
    import tempfile

    if not basename:
        basename = 'temp'

    current_dir = os.getcwd()
    temp_dir = tempfile.mkdtemp(prefix=f'_{basename}', dir=current_dir)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


def get_hash_from_fd(fd, algo=HASH, read_blocks=1024):
    if algo not in ['md5']:
        raise Exception('Internal error: hash algorithm \'%s\' not planned in code.' % algo)

    hash = hashlib.new(algo)
    while True:
        data = fd.read(read_blocks)
        if not data:
            break
        hash.update(data)
    return hash.digest()


def get_hash_from_data(data, algo=HASH):
    fd = io.BytesIO(data)
    digest = get_hash_from_fd(fd, algo, read_blocks=32768)
    fd.close()
    return digest


class TemplateRenderer:
    """Simple class to render Jinja2 templates."""

    def __init__(self, template_dir):
        self._env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template_name, **kwargs):
        template = self._env.get_template(template_name)
        return template.render(**kwargs)

    def render_to_file(self, template_name, output_fname, **kwargs):
        template = self._env.get_template(template_name)
        result = template.render(**kwargs)
        with open(output_fname, mode='w', encoding='utf-8') as f:
            f.write(result)


def print_textbox(title, tl, hline, tr, vline, bl, br):
    def write_utf8(s):
        sys.stdout.buffer.write(s.encode('utf-8'))

    tlen = len(title)
    write_utf8('\n{}'.format(tl))
    write_utf8(hline * (10 + tlen))
    write_utf8('{}\n'.format(tr))

    write_utf8('{}  {}'.format(vline, title))
    write_utf8(' ' * 8)
    write_utf8('{}\n'.format(vline))

    write_utf8(bl)
    write_utf8(hline * (10 + tlen))
    write_utf8('{}\n'.format(br))

    sys.stdout.flush()


def print_section_title(title):
    print_textbox(title, '┌', '─', '┐', '│', '└', '┘')
