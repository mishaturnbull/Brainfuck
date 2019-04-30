# -*- coding: utf-8 -*-

"""
One-cell additive clearing translator.
"""

def onecell(string):

    fckd = ""
    fmt = "{}.[-] "

    for char in string:
        plus = "+" * ord(char)
        fckd += fmt.format(plus)

    return fckd
