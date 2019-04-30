# -*- coding: utf-8 -*-

"""
Multi-cell additive translator.  Non-clearing.
"""


def ncell(string):
    fckd = ''
    fmt = "{}.> "

    for char in string:
        plus = "+" * ord(char)
        fckd += fmt.format(plus)

    return fckd
