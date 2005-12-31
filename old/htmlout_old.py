#!/usr/bin/env python
#
# $Source: /home/blais/repos/cvsroot/conf/common/lib/python/htmlout_old.py,v $
# $Id$
#
# Copyright (C) 2001-2003, Martin Blais <blais@furius.ca>
#

"""Valid HTML output made easy thru XML tree building and output.

"""

__release__ = "0.1"
__version__ = "$Revision$"
__author__ = "Martin Blais <blais@furius.ca>"


import xml.dom.minidom
import types


class Error(StandardError):
    pass

class NicerElement(xml.dom.minidom.Element):
    """cut-n-pasted, and then modified, from minidom.py, for compact output
    of elements with a single text child."""

    def writexml(self, writer, indent="", addindent="", newl=""):

        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        writer.write(indent+"<" + self.tagName)

        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            xml.dom.minidom._write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            if len(self.childNodes) == 1 and\
                   self.childNodes[0].nodeType == \
                   xml.dom.minidom.Node.TEXT_NODE:
                node = self.childNodes[0]

                writer.write(">")
                node.writexml(writer)
                writer.write("</%s>%s" % (self.tagName,newl))
            else:
                writer.write(">%s"%(newl))
                for node in self.childNodes:
                    node.writexml(writer,indent+addindent,addindent,newl)
                writer.write("%s</%s>%s" % (indent,self.tagName,newl))
        else:
            writer.write("/>%s"%(newl))

class Base(NicerElement, object):

    subelems = None

    def __init__( self, parent=None, text=None, doco=None, *args, **kwds ):
        self.cname = self.__class__.__name__.lower()
        xml.dom.minidom.Element.__init__(self, self.cname)
        if doco:
            self.doco = doco
        elif parent:
            self.doco = parent.doco
        assert self.doco, "You must have a document set in the parent."

        # special attribute name base 'class' is a language keyword.
        if 'class_' in kwds:
            kwds['class'] = kwds['class_']
            del kwds['class_']
        for it in kwds.items():
            (k, v) = it
            self.setAttribute(k, v)
        if parent:
            parent.add(self)
        if text != None:
            self.appendChild( self.doco.createTextNode(str(text)) )

    def add( self, child ):

        if self.doco.check_subelems:
            subelems = self.subelems_strict
            if self.doco.transitional:
                subelems += self.subelems_transit
            if not subelems:
                raise Error(
                    "'%s' element cannot contain any other element.'" % \
                    self.cname)
            elif child.cname not in subelems:
                raise Error(
                    "'%s' element cannot contain '%s' element.'" %
                    (self.cname, child.cname))

        self.appendChild( child )
        return child

    def addtext( self, text ):
        if text != None:
            self.appendChild( self.doco.createTextNode(str(text)) )

class Document(xml.dom.minidom.Document):

    def __init__( self, check_subelems=True, transitional=False ):
        self.check_subelems = check_subelems
        self.transitional = transitional

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

    check_subelems = 1

    print '------------------------------'
    doc = Document(check_subelems, True)
    html = HTML(doco=doc)
    h = HEAD(html)
    TITLE(h, 'title')
    if check_subelems:
        try:
            DIV(h)
            assert False
        except Error:
            pass
    body = BODY(html)
    t = TABLE(body, href='dudu')

    # mixed content
    #
    # FIXME: in mixed content, when adding a node, the node must be created with
    # the same parent, no? Check this out in more detail.
    p = P(body)
    p.addtext('blabla')
    p.add(BIG(p, 'david!'))
    p.addtext('blabla2')

    ## SPAN(body) # only valid in transitional

    COL(t, 'jdfjd')
    r = TR(TBODY(t), 'jdfjd')
    TD(r, 'jdsd')
    sys.stdout.write( html.toprettyxml(indent='   ') )
    print '------------------------------'

if __name__ == "__main__":
    test()
