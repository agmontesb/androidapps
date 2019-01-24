# -*- coding: utf-8 -*-
import collections
import ctypes


class AndroidArray(collections.Sequence):
    def __init__(self, atype, size, tupleseq):
        self._type = atype
        if not tupleseq:
            initseq = size*[tuple()]
        self._bytes = map(lambda w: atype(*tupleseq[w]), range(size))

    def __getitem__(self, idx_or_name):
        try:
            return self._bytes[idx_or_name]
        except IndexError:
            return 'ERROR'

    def __len__(self):
        return len(self._bytes)

    def type(self):
        return self._type


class StringArray(AndroidArray):
    def __init__(self, stringSeq):
        tupleSeq = map(lambda x: (x,), stringSeq)
        super(StringArray, self).__init__(type(''), len(stringSeq), tupleSeq)


class IntegerArray(AndroidArray):
    def __init__(self, stringSeq):
        tupleSeq = map(lambda x: (x,), stringSeq)
        super(IntegerArray, self).__init__(ctypes.c_int32, len(stringSeq), tupleSeq)


class LongArray(AndroidArray):
    def __init__(self, stringSeq):
        tupleSeq = map(lambda x: (x,), stringSeq)
        super(IntegerArray, self).__init__(ctypes.c_int32, len(stringSeq), tupleSeq)