# -*- coding: utf-8 -*-
import collections

PngOptions = collections.namedtuple('PngOptions', ('grayScaleTolerance',))
PngOptions.__new__.func_defaults = (0,)

class Png(object):
    def __init__(self, diag):
        super(Png, self).__init__()
        self.mDiag = diag

    def process(self, source, input, outBuffer, options=PngOptions()):
        pass