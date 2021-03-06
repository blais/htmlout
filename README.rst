==================================
   htmlout: HTML Output Library
==================================

.. contents::
..
    1  Description
      1.1  Features
      1.2  History
    2  Documentation
    3  Download
    4  Reporting Bugs
    5  Installation and Dependencies
    6  Copyright and License
    7  Author

Description
===========

htmlout is a simple library that makes it really easy to build a tree of HTML
nodes and then to serialize this tree into text for final output.

This library really needs a rewrite, but I have a lot of code using it, and some
public code in Atocha uses it, so I thought I would open source it anyway.  If
you need it, here it is.


Features
--------

- Has an option to output a nicely indented output or compressed output;
- A simple interface;


History
-------

I have been using and refining this library for years, and although it is long
due for a rewrite, it still serves me well.  It has a fair amount of value, in
the sense that many issues related to browsers have been ironed out, for
example, avoiding outputting empty div tags.  Little details like that.


Documentation
=============

There is no documentation, read the source if you need it.


Download
========

A Mercurial repository can be found at:

  http://github.com/blais/htmlout


Reporting Bugs
==============

Send email to the author: Martin Blais <blais@furius.ca>.


Installation and Dependencies
=============================

Run the setup.py script in the root.


Copyright and License
=====================

Copyright (C) 2001-2005  Martin Blais.
This is not open source software at this moment.


Author
======

Martin Blais <blais@furius.ca>
