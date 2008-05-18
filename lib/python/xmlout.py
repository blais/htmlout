"""
An XML tree building library for output, much simpler than htmlout, and more
efficient, built on top of ElementTree.

This module adds some niceties from the htmlout module to the tree serialization
capabilities of ElementTree, and is much more efficient than htmlout.
"""

# elementtree/lxml imports
## from lxml import etree
## from lxml.etree import Element
from elementtree.ElementTree import Element, ElementTree


class Base(Element):
    "Our base element."

    def __init__(self, *children, **attribs):
        if attribs:
            attribs = translate_attribs(attribs)
        Element.__init__(self, self.__class__.__name__.lower(), attribs)

        for child in children:
            if isinstance(child, (str, unicode)):
                if self.text is None:
                    self.text = ""
                self.text = child
            else:
                self.append(child)

    def add(self, *children):
        return self.extend(children)

    def extend(self, children):
        "A more flexible version of extend."
    
        for child in children:
            # Add child element.
            if isinstance(child, Base):
                self.append(child)

            # Add string.
            elif isinstance(child, (str, unicode)):
                if not self._children:
                    if not self.text: self.text = ''
                    self.text += child
                else:
                    lchild = self._children[-1]
                    if not lchild.tail: lchild.tail = ''
                    lchild.tail += child

        return child # Return the last child.




_attribute_trans_tbl = {
    'class_': 'class',
    '_class': 'class',
    'class': 'class',
    'CLASS': 'class',
    'Class': 'class',
    'Klass': 'class',
    'klass': 'class',
    '_id': 'id',
    'id_': 'id',
    'ID': 'id',
    'Id': 'id',
    }

_attribute_translate = _attribute_trans_tbl.get

def translate_attribs(attribs):
    """ Given a dict of attributes, apply a translation table on the attribute
    names. This is made to support specifying classes directly."""
    return dict((_attribute_translate(k, k), v) for k, v in attribs.iteritems())

def tostring(node, *args, **kwds):
    indent(node)
    return ElementTree(node).write(*args, **kwds)

# From: http://effbot.org/zone/element-lib.htm#prettyprint
# indent: Adds whitespace to the tree, so that saving it as usual results in a
# prettyprinted tree.
def indent(elem, level=0):
    "in-place prettyprint formatter"
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


## def indent(elem, level=0):
##     i = "\n" + level*"  "
##     if len(elem):
##         if not elem.text or not elem.text.strip():
##             elem.text = i + "  "
##         for e in elem:
##             indent(e, level+1)
##             if not e.tail or not e.tail.strip():
##                 e.tail = i + "  "
##         if not e.tail or not e.tail.strip():
##             e.tail = i
##     else:
##         if level and (not elem.tail or not elem.tail.strip()):
##             elem.tail = i





from htmlnodes import init
clsdict = init(Base)
__all__ = ['tostring'] + clsdict.keys()
globals().update(clsdict)

