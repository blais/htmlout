#!/usr/bin/env python

"""
Install script for the htmlout HTML output library.
"""

__author__ = "Martin Blais <blais@furius.ca>"

import sys
from distutils.core import setup

def read_version():
    try:
        return open('VERSION', 'r').readline().strip()
    except IOError, e:
        raise SystemExit(
            "Error: you must run setup from the root directory (%s)" % str(e))


# Include all files without having to create MANIFEST.in
def add_all_files(fun):
    import os, os.path
    from os.path import abspath, dirname, join
    def f(self):
        for root, dirs, files in os.walk('.'):
            if '.hg' in dirs: dirs.remove('.hg')
            self.filelist.extend(join(root[2:], fn) for fn in files
                                 if not fn.endswith('.pyc'))
        return fun(self)
    return f
from distutils.command.sdist import sdist
sdist.add_defaults = add_all_files(sdist.add_defaults)


setup(name="htmlout",
      version=read_version(),
      description=\
      "A simple HTML output library.",
      long_description="""
htmlout is a simple library that makes it really easy to build a tree of HTML
nodes and then to serialize this tree into text for final output.
""",
      license="GPL",
      author="Martin Blais",
      author_email="blais@furius.ca",
      url="http://furius.ca/htmlout",
      download_url="http://github.com/blais/htmlout",
      package_dir = {'': 'lib/python'},
      py_modules = ['htmlout'],
     )
