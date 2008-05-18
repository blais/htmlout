"""
Definition of valid HTML nodes and their children.
This is in essence a reduced declaration of the valid HTML schema.
We could eventually use this in order to validate the tree of nodes before
output.
"""

# stdlib imports
import types

__all__ = ('init',)



def init(cls):
    """
    Creates an instance of the class 'cls' and return a dict of new instances
    names to class object. The returned dict should probably be appended to the
    __all__ list of the module.
    """
    all = {}
    for k, v in elems_map.iteritems():
        name = k.upper()
        newclass = type(name, (cls,), {})

        if isinstance(v, types.TupleType):
            assert len(v) == 2
            newclass.subelems_strict, newclass.subelems_transit = v
        else:
            newclass.subelems_strict, newclass.subelems_transit = v, []

        all[name] = newclass
    return all





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
 'noop': [],
}


