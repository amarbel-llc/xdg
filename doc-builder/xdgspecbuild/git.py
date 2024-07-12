#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
# Copyright (C) 2019-2020 Bastien Nocera <hadess@hadess.net>
#
# SPDX-License-Identifier: LGPL-3.0+

import os
import re
import subprocess
import urllib.error
import urllib.request

from .utils import get_hash_from_data


def get_main_branch(url):
    out = subprocess.check_output(['git ls-remote --symref ' + url + ' HEAD'], shell=True)
    m = re.search('refs/heads/(.+)\t', out.decode("utf-8"))
    return m.group(1)


class GitObject:
    def __init__(self, gitweb, file, revision=None):
        self.gitweb = gitweb
        self.file = file
        self.revision = revision
        if self.gitweb.endswith('/'):
            self.gitweb = self.gitweb[:-1]
        if not self.revision:
            self.revision = get_main_branch('/'.join((self.gitweb + '.git')))
        self.data = None

    def get_url(self):
        query = {}
        baseurl = self.gitweb
        path = '/'.join(('raw', self.revision, self.file))

        (scheme, netloc, basepath) = urllib.parse.urlsplit(baseurl)[0:3]
        full_path = '/'.join((basepath, path))

        query_str = urllib.parse.quote(bytes(query))
        return urllib.parse.urlunsplit((scheme, netloc, full_path, query_str, ""))

    def fetch(self):
        if self.data:
            return

        if self.revision:
            url = self.get_url()
            try:
                fd = urllib.request.urlopen(url, None)
            except:
                print('Failed to fetch URL: %s' % url)
                raise
            self.data = fd.read()
            fd.close()
        else:
            localpath = (
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + self.file
            )
            fd = open(localpath, 'rb')
            self.data = fd.read()
            fd.close()

    def get_hash(self):
        self.fetch()
        return get_hash_from_data(self.data)
