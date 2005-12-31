#!/usr/bin/env python
#
# $Source: /home/blais/repos/cvsroot/conf/common/lib/python/htmlout_et.py,v $
# $Id$
#
# Copyright (C) 2001-2003, Martin Blais <blais@furius.ca>
#

"""

(This is a version of htmlout.py that uses elementtree instead of minidom.  See
htmlout.py for a more easily portable version of this library.)

HTML output builder module.  Valid HTML output is made easy by building an XML
tree of nodes and serializing.  This is a version of the library that uses
ElementTree.

Usage
-----

To build an HTML file you build a tree of XML element using the classes in this
module.  A class with the name of each of the HTML element names is defined, in
capital letters.  By creating instances of these classes and forming a tree you
build the documen tree.  Thus, this module should be import with::

   from htmltree import *

Then all you need do it something like this (an example)::

    doc = HTML(
        META(generator='This Script'),
        LINK(rel="stylesheet", href="style.css", type="text/css")
        )

    body = BODY(parent=doc)

    body.append( P('Some paragraph.') )
    body += P('Some other paragraph.')
    body += ( P('Bla.'),
              P('Bla.') )

    table = TABLE()
    table.append(
        TBODY('ahasa',
              TR( TD('blabla'),
                  TD('blabla'),
                  TD('blabla') )
              ))

    doc += table

Constructor, append and += methods are all equivalent and are processed the same
way, which allows the creation process to be as flexible as possible to
accommodate all use cases:

- other nodes passed in are added as children;

- attributes are set by specifying keyword arguments.  You can also offer a
  dictionary and the key/value pairs will update the attributes list;

- strings are added between child nodes in the order they are seen;

- there is a special attribute 'parent' that can be used to parent the node.
  This is useful when creating a node and storing it in a variable, e.g.::

     body = BODY( ... )
     table = TABLE(parent=body,
                 TR( ...

- tuples are expanded and then processed the same way when used with the +=
  operator. This allows the following syntax::

     table += ( TR( ... ),
                TR( ... ),
                TR( ... ) )

Special attributes
~~~~~~~~~~~~~~~~~~

You can specify the main text content as a keyword attribute by using the
special ``text`` or ``TEXT`` attribute.

You can specify the HTML class by using the ``class_`` or ``CLASS`` keyword
attribute. These are translated into 'class' attributes (the reason for this is
that 'class' is a reserved keyword in Python).


Features
--------

Using such a library presents several advantages:

- tags do not have to be generated in the order that they appear; you can create
  multiple containers, fill them up in parallel and eventually add them to a
  parent container.

- the generated XML is always well-formed;


HTML output
-----------

All the nodes are direct descendants of elementtree nodes, and as such, you can
use the serializing operation that elementtree provides to output your XHTML
code.

Validation
----------

The original version of this library had an automatic validation component. This
is not supported right now.

"""

__release__ = "0.1"
__version__ = "$Revision$"
__author__ = "Martin Blais <blais@furius.ca>"

import sys

from elementtree.ElementTree import _Element, ElementTree
import types
import elementtree_helpers


class Base(_Element, object):

    subelems = None

    def __init__( self, *children, **attribs ):
        self.cname = self.__class__.__name__.lower()
        _Element.__init__(self, self.cname, {})

        self.append(*children, **attribs)

    def __iadd__( self, *children ):
        # Deal with tuples, to allow el += (c1, c2, c3, ...)
        if len(children) == 1 and type(children[0]) is types.TupleType:
            return self.append(*children[0])
        else:
            return self.append(*children)

    def append( self, *children, **attribs ):
        #
        # Add attributes.
        #

        if attribs:
            ##print >> sys.stderr, attribs
            # Treat class attribute specially.
            if 'class_' in attribs:
                attribs['class'] = attribs['class_']
                del attribs['class_']

            if 'CLASS' in attribs:
                attribs['class'] = attribs['CLASS']
                del attribs['CLASS']

            if 'text_' in attribs:
                if not self.text: self.text = ''
                self.text += attribs['text_']
                del attribs['text_']

            if 'TEXT' in attribs:
                if not self.text: self.text = ''
                self.text += attribs['TEXT']
                del attribs['TEXT']

            # Allow adding parent like this "n = NAME(parent=p)"
            if 'parent' in attribs:
                attribs['parent'].append(self)
                del attribs['parent']

            ## # Allow adding an attribute actually named 'parent'
            ## if 'parent_' in attribs:
            ##     attribs['parent'] = attribs['parent_']
            ##     del attribs['parent_']
            ## Note: this is not used, you can use the dict syntax instead.

            # Add all other attributes.
            self.attrib.update(attribs)

        #
        # Add children and text.
        #
        for child in children:
            # Add child element.
            if isinstance(child, Base):
                ##print >> sys.stderr, "ELEMENT"
                _Element.append(self, child)

            # Add string.
            elif type(child) in [type(''), type(u'')]:
                ##print >> sys.stderr, "STRING"
                if not self.getchildren():
                    if not self.text: self.text = ''
                    self.text += child
                else:
                    lchild = self.getchildren()[-1]
                    if not lchild.tail: lchild.tail = ''
                    lchild.tail += child

            # Add attributes in map.
            # This can be useful when there are children put
            # the attributes before the children.
            elif isinstance(child, types.DictionaryType):
                ##print >> sys.stderr, "DICT"
                self.attrib.update(child)

        return self

    def append_raw( self, element ):
        _Element.append(self, element)

# Validation code (not needed for now).

## class Error(StandardError):
##     pass

##         if self.doco.check_subelems:
##             subelems = self.subelems_strict
##             if self.doco.transitional:
##                 subelems += self.subelems_transit
##             if not subelems:
##                 raise Error(
##                     "'%s' element cannot contain any other element.'" % \
##                     self.cname)
##             elif child.cname not in subelems:
##                 raise Error(
##                     "'%s' element cannot contain '%s' element.'" %
##                     (self.cname, child.cname))

## class Document(xml.dom.minidom.Document):

##     def __init__( self, check_subelems=True, transitional=False ):
##         self.check_subelems = check_subelems
##         self.transitional = transitional


# main attribute groups
attr_core = ['id', 'class', 'style', 'title']
attr_i18n = ['lang', 'dir']
attr_common = attr_core + attr_i18n

elems_both = ['applet', 'button', 'del', 'iframe', 'ins', 'map',
              'object', 'script']

elems_inline = ['a', 'abbr', 'acronym', 'b', 'basefont', 'bdo', 'big', 'br',
                'cite', 'code', 'dfn', 'em', 'font', 'i', 'img', 'input', 'kbd',
                'label', 'q', 's', 'samp', 'select', 'small', 'span', 'strike',
                'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var']

elems_block = ['address', 'blockquote', 'center', 'dir', 'div', 'dl',
               'fieldset', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
               'isindex', 'menu', 'noframes', 'noscript', 'ol', 'p', 'pre',
               'table', 'ul', 'dd', 'dt', 'frameset', 'li', 'tbody', 'td',
               'tfoot', 'th', 'thead', 'tr']

# Mapping of child elements for each element, for both strict and transitional
# doctypes, so that while we're generating the HTML document we're validating
# which child elements are allowed.
#
# Note: this is not exact, but a useful approximation.
# ----------------------------------------------------

elems_map = {
 'html': ['head', 'body', 'frameset'],
 'head': ['title', 'base', 'isindex', 'script', 'style', 'meta', 'link',
          'object'],
 'body': (elems_block + ['script', 'ins', 'del'], elems_inline),
 'frameset': ['frame', 'noframes'],
 'base': [],
 'isindex': [],
 'link': [],
 'meta': [],
 'script': [],
 'style': [],
 'title': [],
 'address': (elems_inline, ['p']),
 'blockquote': (elems_block + ['script'], ['elems_inline']),
 'center': elems_inline + elems_block,
 'del': elems_inline + elems_block,
 'div': elems_inline + elems_block,
 'h1': elems_inline,
 'h2': elems_inline,
 'h3': elems_inline,
 'h4': elems_inline,
 'h5': elems_inline,
 'h6': elems_inline,
 'hr': [],
 'ins': elems_inline + elems_block,
 'isindex': [],
 'noscript': elems_inline + elems_block,
 'p': elems_inline,
 'pre': elems_inline + ['img', 'object', 'applet', 'big', 'small', 'sub', 'sup',
         'font', 'basefont'],
 'dir': ['li'],
 'dl': ['dt', 'dd'],
 'dt': elems_inline,
 'dd': elems_inline + elems_block,
 'li': elems_inline + elems_block,
 'menu': ['li'],
 'ol': ['li'],
 'ul': ['li'],
 'table': ['caption', 'col', 'colgroup', 'thead', 'tfoot', 'tbody'],
 'caption': elems_inline,
 'colgroup': ['col'],
 'col': [],
 'thead': ['tr'],
 'tfoot': ['tr'],
 'tbody': ['tr'],
 'tr': ['th', 'td'],
 'td': elems_inline + elems_block,
 'th': elems_inline + elems_block,
 'form': (['script'] + elems_block, elems_inline),
 'button': elems_inline + elems_block,
 'fieldset': ['legend'] + elems_inline + elems_block,
 'legend': elems_inline,
'input': [],
 'label': elems_inline,
 'select': ['optgroup', 'option'],
 'optgroup': ['option'],
 'option': [],
 'textarea': [],
 'a': elems_inline,
 'applet': ['param'] + elems_inline + elems_block,
 'basefont': [],
 'bdo': elems_inline,
 'br': [],
 'font': elems_inline,
 'iframe': elems_inline + elems_block,
 'img': [],
 'map': elems_block + ['area'],
 'area': [],
 'bject': ['param'] + elems_inline + elems_block,
 'param': [],
 'q': elems_inline,
 'script': [],
 'span': elems_inline,
 'sub': elems_inline,
 'sup': elems_inline,
 'abbr': elems_inline,
 'acronym': elems_inline,
 'cite': elems_inline,
 'code': elems_inline,
 'del': elems_inline + elems_block,
 'dfn': elems_inline,
 'em': elems_inline,
 'ins': elems_inline + elems_block,
 'kbd': elems_inline,
 'samp': elems_inline,
 'strong': elems_inline,
 'var': elems_inline,
 'b': elems_inline,
 'big': elems_inline,
 'i': elems_inline,
 's': elems_inline,
 'small': elems_inline,
 'strike': elems_inline,
 'tt': elems_inline,
 'u': elems_inline,
 'frameset': ['frameset', 'frame', 'noframes'],
 'frame': [],
 'noframes': ('', elems_inline + elems_block),
}

for k, v in elems_map.iteritems():
    n = k.upper()
    newclass = type(n, (Base,), {})

    if isinstance(v, types.TupleType):
        assert len(v) == 2
        newclass.subelems_strict, newclass.subelems_transit = v
    else:
        newclass.subelems_strict, newclass.subelems_transit = v, []

    globals()[n] = newclass


#===============================================================================
# TEST
#===============================================================================

def test():
    import sys

    doc = HTML(
        HEAD('ankjwajhsjasa',
        META('blabal')
        ) )

    table = TABLE()
    body = BODY(
        table.append(TBODY('ahasa',
        TR(
        TD('blabla'),
        TD('blabla'),
        TD('blabla'),
        )))
        )

    p1, p2 = P('blabla'), P('bli')

    p2.text += 'dhsdhshkds'
    doc += body
    doc += (p1, p2)

    ElementTree(doc).write_fmt(sys.stdout)

if __name__ == "__main__":
    test()


    doc = HTML(
        META(generator='This Script'),
        LINK(rel="stylesheet", href="style.css", type="text/css")
        )

    body = BODY(parent=doc)

    body.append( P('Some paragraph.') )
    body += P('Some other paragraph.')
    body += ( P('Bla.'),
              P('Bla.') )

    table = TABLE()
    table.append(
        TBODY('ahasa',
              TR( TD('blabla'),
                  TD('blabla'),
                  TD('blabla') )
              ))

    doc += table
