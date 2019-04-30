# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 19:04:51 2015
Take a string and fuck it!
@author: Misha
"""

import translators


class Fucker(object):

    def __init__(self, fucking):
        self.fucking = fucking
        asciip1 = list(self.fucking)
        self.ascii = [translators.helpers.R_ASCII[s] for s in asciip1]
        self.fucked = ''

    def _fmtmake(self, fmt):
        fckd = ''
        for char in self.ascii:
            fckd += fmt.format('+' * char)
        return fckd

    def translate(self, mode):
        transmod = translators.__getattribute__(mode)
        translator = transmod.__getattribute__(mode)
        code = translator(self.fucking)
        self.fucked = code
        return self.fucked
