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

    def test_caching(self):
        html = HTML()
        body = html.add(BODY())
        el = DIV(P("Special sauce."))
        el.cache = 1
        body.add(el)
        body.add(el)
        tostring(html, open('caching.xml', 'w'))


