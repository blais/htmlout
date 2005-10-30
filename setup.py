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
      package_dir = {'': 'lib/python'},
      py_modules = ['htmlout'],
     )
