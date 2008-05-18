"""
Old htmlout tests split out.
"""

def test():
    # just to make pychecker shut up
    import sys

    doc = HTML(
        HEAD('ankjwajhsjasa',
             META('blabal'),
             STYLE()
        ) )

    body = BODY(
               TABLE(
                   TBODY('ahasa',
                       TR(
                           TD('blabla'),
                           TD('blabla'),
                           TD('blabla'),
                           )
                         ),
                   blabla='somevlue')
               )
    
    body.append( NOOP(P("YEAH"), DIV("prout")), NOOP("proutprout"), NOOP() )

    p1, p2 = P('blabla'), P('bli')

    p2.text += 'dhsdhshkds'
    p2.styles.append('p { font-style: italic; }')


    div = DIV("some random text", id='bli', parent=body)
    div.styles.append("#bli { font-size: xx-large; }")

    doc.append( body )
    doc += (p1, p2)


    url = 'http://furius.ca'
    doc.append(
        DIV( {'name': 'value'},
             P("""Some child tesxtksjddf jkdsdshdshdks dhsd hs
             huhdsudhwiudhsk hdjshdjs dhjksldhssd""",
               A(url, href=url), """more text.""")
             )
        )

    doc.append(
        DIV( VERBATIM("""Some verbatim
        text in multipl>
        lines with >>>>> embedded in them.
        """)))

    sys.stdout.write(tostring(doc, doctype=1, ctnttype=1, styles=1))

if __name__ == "__main__":
    test()



