# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/flatten/ChunkWriter.h
#
from ctypes import *

from Tools.aapt.ResourcesTypes import ResChunk_header


class ChunkWriter(object):

    def __init__(self, buffer):
        super(ChunkWriter, self).__init__()
        self.mBuffer = buffer
        self.mStartSize = 0
        self.mHeader = None

    def startChunk(self, atype, ctypeClass=ResChunk_header):
        self.mStartSize = self.mBuffer.size()
        chunk = self.mBuffer.nextBlock(ctypeClass)
        self.mHeader = chunk.header if hasattr(chunk, 'header') else chunk
        self.mHeader.type = atype
        self.mHeader.headerSize = sizeof(ctypeClass)
        return chunk

    def nextBlock(self, ctypeClass, count=0):
        return self.mBuffer.nextBlock(ctypeClass, count)

    def getBuffer(self):
        return self.mBuffer

    def getChunkHeader(self):
        return self.mHeader

    def size(self):
        return self.mBuffer.size()

    def finish(self):
        self.mBuffer.align4()
        self.mHeader.size = self.mBuffer.size() - self.mStartSize
        return self.mHeader



