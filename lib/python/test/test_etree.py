"""
Tests for creating trees using ElementTree.
Use py.test to run these tests.
"""

from elementtree.ElementTree import *


class TestSimple(object):

    def test_simple(self):
        div = Element('DIV')
        el = Element('P')
        div.append(el)
        el.text = u"Some contents"
        tree = ElementTree(div)
        tree.write(open('test.xml', 'w'))





