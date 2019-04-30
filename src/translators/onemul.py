# -*- coding: utf-8 -*-

"""
One-cell clearing multiplicative translator.
"""

from . import helpers


def onemul(string):
    fmtm = "{a}[>{b}<-]>.[-]< "
    fmtb = "{a}[>{b}<-]>{p}.[-]< "
    fckd = ''

    for char in string:
        char = ord(char)
        if char in helpers.PRIMES:
            if char > 10:
                n_sub = 0
                while char in helpers.PRIMES:
                    char -= 1
                    n_sub += 1
                padd = "+" * n_sub
                a, b = helpers.get_added(char)
            fckd += fmtb.format(a='+' * a, b='+' * b, p=padd)
        else:
            a, b = helpers.get_added(char)
            fckd += fmtm.format(a='+' * a, b='+' * b)
    return fckd
