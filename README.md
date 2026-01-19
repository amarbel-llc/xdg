xdg-specs
=========

This repository contains the XDG specifications that are
readable at:

  https://specifications.freedesktop.org/

To discuss the specifications, you may use the xdg mailing list:

  http://lists.freedesktop.org/mailman/listinfo/xdg

Building specifications website
===============================

The specifications website is automatically built using the [Gitlab
continuous integration](https://gitlab.freedesktop.org/xdg/xdg-specs/-/blob/master/.gitlab-ci.yml).

The sources files are in the [`doc-builder`](https://gitlab.freedesktop.org/xdg/xdg-specs/-/tree/master/doc-builder)
directory.

Building a single spec
======================

To build a single spec in `article` docbook xml format you can use xmlto, e.g.:
```bash
    xmlto html-nochunks notification/notification-spec.xml -o _build/
```

To build the website HTML of a single spec, you can invoke the doc-builder with
the specification name as a parameter:
```bash
    ./doc-builder/build.py notification
```

How to report issues
====================

Issues should be reported to:

   https://gitlab.freedesktop.org/xdg/xdg-specs/-/issues


Licenses
========

Please refer to the individual files for their licenses.
