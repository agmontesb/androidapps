# -*- coding: utf-8 -*-
import ctypes


class BigBuffer(object):

    class Block(object):
        def __init__(self):
            super(BigBuffer.Block, self).__init__()
            self.buffer = None
            self.size = None
            self.mBlockSize = None

        def __add__(self, other):
            if isinstance(other, BigBuffer.Block):
                return self.buffer[:self.size] + other.buffer[:other.size]
            elif isinstance(other, bytearray):
                return self.buffer[:self.size] + other
            raise AttributeError()

        def __radd__(self, other):
            if isinstance(other, bytearray):
                return other + self.buffer[:self.size]

    def __init__(self, blockSize):
        super(BigBuffer, self).__init__()
        self.mBlockSize = blockSize
        self.mSize = 0
        self.mBlocks = []

    def size(self):
        return self.mSize

    def nextBlock(self, ctypeClass, count=0):
        return self._nextBlockImpl(ctypeClass, count)

    def appendBuffer(self, bigBuffer):
        self.mBlocks.extend(bigBuffer.mBlocks)
        self.mSize += bigBuffer.mSize
        bigBuffer.mBlocks = []
        bigBuffer.mSize = 0

    def pad(self, bytes):
        self.nextBlock(ctypes.c_char, bytes)

    def align4(self):
        unaligned = self.mSize % 4
        if unaligned:
            self.pad(4 - unaligned)

    def __iter__(self):
        self._ndx = -1
        return self

    def next(self):
        try:
            self._ndx += 1
            return self.mBlocks[self._ndx]
        except:
            raise StopIteration()

    def _nextBlockImpl(self, ctypeClass, isize):
        size = max(1, isize) * ctypes.sizeof(ctypeClass)
        ctypeClass = (ctypeClass if isize == 0 else isize * ctypeClass)
        if self.mBlocks:
            block = self.mBlocks[-1]
            if block.mBlockSize - block.size >= size:
                offset = block.size
                block.size += size
                self.mSize += size
                return ctypeClass.from_buffer(block.buffer, offset)

        actualSize = max(self.mBlockSize, size)
        block = BigBuffer.Block()
        block.buffer = bytearray(actualSize)
        block.size = size
        block.mBlockSize = actualSize
        self.mBlocks.append(block)
        self.mSize += size
        return ctypeClass.from_buffer(self.mBlocks[-1].buffer)



