# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 19:04:51 2015
Take a string and fuck it!
@author: Misha
"""

import functools


ASCII = dict(zip(range(256), [chr(c) for c in range(256)]))
R_ASCII = dict(zip(ASCII.values(), ASCII.keys()))

# yes, I know 0 and 1 aren't prime but for this it works that way
PRIMES = [0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
          61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131,
          137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
          211, 223, 227, 229, 233, 239, 241, 251]


def get_prime_factors(number):
    for i in range(2, number):
        rd, qt = divmod(number, i)
        if not qt: # if equal to zero
            return [i] + get_prime_factors(rd)
    return [number]


def find_good_factors(number):
    a, b, p = 1, 72, 0
    if number in PRIMES:
        number -= 1
        p += 1

    primefactors = get_prime_factors(number)

    ratio = lambda a, b: abs(1 - a/b)

    def factors(pfactors, s):
        l_a, l_b = pfactors[:s], pfactors[s:]
        p = functools.reduce(lambda x, y: x*y, l_a)
        q = functools.reduce(lambda x, y: x*y, l_b)
        return p, q

    best_ratio = ratio(a, b)
    best_s = 0
    for s in range(1, len(primefactors)):
        newratio = ratio(*factors(primefactors, s))
        if newratio < best_ratio:
            best_ratio = newratio
            best_s = s

    c, d = factors(primefactors, best_s)
    return c, d, p


class Fucker(object):

    def __init__(self, fucking):
        self.fucking = fucking
        asciip1 = list(self.fucking)
        self.ascii = [R_ASCII[s] for s in asciip1]
        self.fucked = ''

    def _fmtmake(self, fmt):
        fckd = ''
        for char in self.ascii:
            fckd += fmt.format('+' * char)
        return fckd

    @classmethod
    def fuckit(cls, string):
        return cls(string).optimul()

    def onecell(self):
        return self._fmtmake("{}.[-]")

    def ncell(self):
        return self._fmtmake("{}.>")

    def onemul(self):
        fmtm = "{a}[>{b}<-]>.[-]< "
        fmtb = "{a}[>{b}<-]>{p}.[-]< "
        fckd = ''

        def get_added(char):
            pfactors = get_prime_factors(char)
            s = int(round(len(pfactors)/2.))
            l_a, l_b = pfactors[:s], pfactors[s:]
            a = functools.reduce(lambda x, y: x*y, l_a)
            b = functools.reduce(lambda x, y: x*y, l_b)
            return a, b

        for char in self.ascii:
            if char in PRIMES:
                if char > 10:
                    n_sub = 0
                    while char in PRIMES:
                        char -= 1
                        n_sub += 1
                    padd = "+" * n_sub
                    a, b = get_added(char)
                fckd += fmtb.format(a='+'*a, b='+'*b, p=padd)
            else:
                a, b = get_added(char)
                fckd += fmtm.format(a='+'*a, b='+'*b)
        return fckd

    def nmul(self):
        fmtm = "{a}[>{b}<-]>.> "
        fmtb = "{a}[>{b}<-]>{p}.> "
        fckd = ''

        def get_added(char):
            pfactors = get_prime_factors(char)
            s = int(round(len(pfactors)/2.))
            l_a, l_b = pfactors[:s], pfactors[s:]
            a = functools.reduce(lambda x, y: x*y, l_a)
            b = functools.reduce(lambda x, y: x*y, l_b)
            return a, b

        for char in self.ascii:
            if char in PRIMES:
                if char > 10:
                    n_sub = 0
                    while char in PRIMES:
                        char -= 1
                        n_sub += 1
                    padd = "+" * n_sub
                    a, b = get_added(char)
                fckd += fmtb.format(a='+'*a, b='+'*b, p=padd)
            else:
                a, b = get_added(char)
                fckd += fmtm.format(a='+'*a, b='+'*b)
        return fckd

    def optimul(self):
        fmtm = "{a}[>{b}<-]>.> "
        fmtb = "{a}[>{b}<-]>{p}.> "
        fckd = ''

        for char in self.ascii:
            if char in PRIMES:
                a, b, p = find_good_factors(char)
                fckd += fmtb.format(a='+'*a, b='+'*b, p='+'*p)
            else:
                a, b, p = find_good_factors(char)
                fckd += fmtm.format(a='+'*a, b='+'*b)
        return fckd
