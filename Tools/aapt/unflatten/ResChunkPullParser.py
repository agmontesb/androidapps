# -*- coding: utf-8 -*-
import ctypes

#
#  A pull parser, modeled after XmlPullParser, that reads
#  android.ResChunk_header structs from a block of data.
#
#  An android.ResChunk_header specifies a type, headerSize,
#  and size. The pull parser will verify that the chunk's size
#  doesn't extend beyond the available data, and will iterate
#  over each chunk in the given block of data.
#
#  Processing nested chunks is done by creating a new ResChunkPullParser
#  pointing to the data portion of a chunk.
#
from Tools.aapt.ResourcesTypes import ResChunk_header


class ResChunkPullParser(object):
    #
    #  Create a ResChunkPullParser to read android.ResChunk_headers
    #  from the memory pointed to by data, of len bytes.
    #

    class Event(object):
        StartDocument = 0
        EndDocument = 1
        BadDocument = 2
        Chunk = 3

    def __init__(self, data, dLen):
        super(ResChunkPullParser, self).__init__()
        self.mEvent = self.Event.StartDocument
        self.mData = iter(data)
        self.mBlkOffset = 0
        self.mOffset = 0
        self.mLen = dLen
        self.mCurrentChunk = None
        self.mLastError = ''

    def isGoodEvent(self, event):
        #
        #  Returns False if the event is EndDocument or BadDocument.
        #
        return event != self.Event.EndDocument and event != self.Event.BadDocument

    def getEvent(self):
        return self.mEvent

    def getLastError(self):
        return self.mLastError

    def getChunk(self):
        return self.convertTo(self.mCurrentChunk, ResChunk_header, self.mBlkOffset)

    def next(self):
        #
        #  Move to the next android.ResChunk_header.
        #
        if not self.isGoodEvent(self.mEvent):
            return self.mEvent

        if self.mEvent == self.Event.StartDocument:
            self.mCurrentChunk = self.mData.next()
            self.mBlkOffset = 0
            self.mOffset = 0
        else:
            block, offset = self.mCurrentChunk, self.mBlkOffset
            header = ResChunk_header.from_buffer(block.buffer, offset)
            if block.size >= offset + header.size:
                self.mBlkOffset += header.size
                self.mOffset += header.size
            else:
                self.mOffset += block.size
                self.mCurrentChunk = self.mData.next()
                self.mBlkOffset = 0

        diff = self.mOffset
        assert diff >= 0, "diff is negative"
        offset = diff
        if offset == self.mLen:
            self.mCurrentChunk = None
            self.mEvent = self.Event.EndDocument
            return self.mEvent
        elif (offset + ctypes.sizeof(ResChunk_header)) > self.mLen:
            self.mLastError = "chunk is past the end of the document"
            self.mCurrentChunk = None
            self.mEvent = self.Event.BadDocument
            return self.mEvent

        header = ResChunk_header.from_buffer(self.mCurrentChunk.buffer, self.mBlkOffset)
        if header.headerSize < ctypes.sizeof(ResChunk_header):
            self.mLastError = "chunk has too small header"
            self.mCurrentChunk = None
            self.mEvent = self.Event.BadDocument
            return self.mEvent
        elif header.size < self.mCurrentChunk.headerSize:
            self.mLastError = "chunk's total size is smaller than header"
            self.mCurrentChunk = None
            self.mEvent = self.Event.BadDocument
            return self.mEvent
        elif offset + self.mCurrentChunk.size > self.mLen:
            mLastError = "chunk's data extends past the end of the document"
            self.mCurrentChunk = None
            self.mEvent = self.Event.BadDocument
            return self.mEvent
        self.mEvent = self.Event.Chunk
        return self.mEvent

def convertTo(chunk, ctypeClass, offset=0):
    header = ResChunk_header.from_buffer(chunk.buffer, offset)
    if header.headerSize < ctypes.sizeof(ctypeClass):
        return None
    return ctypeClass.from_buffer(chunk.buffer, offset)

def getChunkData(chunk, offset=0):
    header = ResChunk_header.from_buffer(chunk.buffer, offset)
    ctypeClass = (header.size - header.headerSize) * ctypes.c_uint8
    return ctypeClass.from_buffer(chunk.buffer, offset + header.headerSize)

def getChunkDataLen(chunk, offset=0):
    header = ResChunk_header.from_buffer(chunk.buffer, offset)
    return header.size - header.headerSize

