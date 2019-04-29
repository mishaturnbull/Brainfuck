# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 21:48:10 2015

@author: Misha
"""

import pybf
import os
import uuid

INITIAL_CHAR = '\x00'
INITIAL_ARRAY = INITIAL_CHAR * 3


class BF_Array (object):

    def __init__(self, filename):
        self._len = len(INITIAL_ARRAY)
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write(INITIAL_ARRAY)

    def _read(self):
        with open(self.filename, 'r') as f:
            ret = f.read()
        return [ord(c) for c in ret]

    def _write(self, pos, val):
        text = self._read()
        if len(text) <= pos:
            text += INITIAL_CHAR * (pos - len(text))
        text[pos] = val
        s = ''.join([chr(c) for c in text])
        with open(self.filename, 'w') as f:
            f.write(s)
        return text

    def __getitem__(self, item):
        return self._read()[item]

    def __setitem__(self, item, val):
        self._write(item, val)
        self._len += 1

    def __len__(self):
        return self._len

    def __contains__(self, item):
        return item < self._len

    def __str__(self):
        with open(self.filename, 'r') as f:
            ret = f.read()
        return ret

    def update(self, d):
        for key in d:
            self._write(key, d[key])


class BF_Inf_Object (pybf.BF_Object):

    def __init__(self, code, input_val='', debug=False):
        super(BF_Inf_Object, self).__init__(code, input_val, debug)
        self.a = BF_Array(hex(uuid.uuid4().int)[2:6] + "_arraytemp.bfa")

    def execute(self):
        super(BF_Inf_Object, self).execute()
        os.remove(self.a.filename)
