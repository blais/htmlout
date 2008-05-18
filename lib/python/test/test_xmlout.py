"""
Tests for xmlout.
"""

from xmlout import *


class TestSimple(object):

    def test_simple(self):
        html = HTML()
        html.add(DIV(P("Some text")))
        html.add("bli")
        
        tostring(html, open('test.xml', 'w'))





