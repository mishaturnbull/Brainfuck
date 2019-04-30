# -*- coding: utf-8 -*-

"""
N-cell optimizing multiplicative translator
"""

from . import helpers


def optimul(string):
    fmtm = "{a}[>{b}<-]>.> "
    fmtb = "{a}[>{b}<-]>{p}.> "
    fckd = ''

    for char in string:
        char = ord(char)
        if char in helpers.PRIMES:
            a, b, p = helpers.find_good_factors(char)
            fckd += fmtb.format(a='+'*a, b='+'*b, p='+'*p)
        else:
            a, b, p = helpers.find_good_factors(char)
            fckd += fmtm.format(a='+'*a, b='+'*b)
    return fckd
