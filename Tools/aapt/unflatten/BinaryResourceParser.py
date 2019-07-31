# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/unflatten/BinaryResourceParser.h
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/unflatten/BinaryResourceParser.cpp
#

# struct SymbolTable_entry;
# 
#  Parses a binary resource table (self, resources.arsc) and adds the entries
#  to a ResourceTable. This is different than the libandroidfw ResTable
#  in that it scans the table from top to bottom and doesn't require
#  support for random access. It is also able to parse non-runtime
#  chunks and types.
#
from ctypes import *

from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.ResourceTypeExtensions import SymbolTable_header, SymbolTable_entry
from Tools.aapt.ResourcesTypes import ResStringPool
from Tools.aapt.ResourcesTypes import ResChunk_header
from Tools.aapt.unflatten.ResChunkPullParser import ResChunkPullParser, convertTo, getChunkDataLen, getChunkData


class BinaryResourceParser(object):
    # 
    #  Creates a parser, which will read `len` bytes from `data`, and
    #  add any resources parsed to `table`. `source` is for logging purposes.
    #
    def __init__(self, context, table, source, data, dataLen):
        super(self, BinaryResourceParser, self).__init__()
        self.mContext = context
        self.mTable = table
        self.mSource = source
        self.mData = data
        self.mDataLen = dataLen
        #  The array of symbol entries. Each element points to an offset
        #  in the table and an index into the symbol table string pool.
        self.mSymbolEntries = []
        #  Number of symbol entries.
        self.mSymbolEntryCount = 0
        #  The symbol table string pool. Holds the names of symbols
        #  referenced in this table but not defined nor resolved to an
        #  ID.
        self.mSymbolPool = ResStringPool()
        #  The source string pool. Resource entries may have an extra
        #  field that points into this string pool, which denotes where
        #  the resource was parsed from originally.
        self.mSourcePool = ResStringPool()
        #  The standard value string pool for resource values.
        self.mValuePool = ResStringPool()
        #  The string pool that holds the names of the types defined
        #  in this table.
        self.mTypePool = ResStringPool()
        #  The string pool that holds the names of the entries defined
        #  in this table.
        self.mKeyPool = ResStringPool()
        #  A mapping of resource ID to resource name. When we finish parsing
        #  we use this to convert all resource IDs to symbolic references.
        self.mIdIndex = {}

    # 
    #  Parses the binary resource table and returns true if successful.
    #
    def parse(self):
        parser = ResChunkPullParser(self.mData, self.mDataLen)
        error = False
        while ResChunkPullParser.isGoodEvent(parser.next()):
            if parser.getChunk().type != ResChunk_header.RES_TABLE_TYPE:
                self.mContext.getDiagnostics().warn = \
                "unknown chunk of type '%s'" & parser.getChunk().type
                continue
            if not self.parseTable(parser.getChunk()):
                error = True
        if parser.getEvent() == ResChunkPullParser.Event.BadDocument:
            self.mContext.getDiagnostics().error = \
                self.mSource + "corrupt resource table: %s" % parser.getLastError()
            return False
        return not error

    #  Helper method to retrieve the symbol name for a given table offset specified
    #  as a pointer.
    def getSymbol(self, data, outSymbol):

        if not self.mSymbolEntries or self.mSymbolEntryCount == 0:
            return False

        if data < self.mData:
            return False

        #  We only support 32 bit offsets right now.
        offset = data - self.mData
        # if offset > std.numeric_limits<uint32_t>.max():
        #     return False

        for i in range(self.mSymbolEntryCount):
            if self.mSymbolEntries[i].offset == offset:
                #  This offset is a symbol!
                ndx = self.mSymbolEntries[i].stringIndex
                astr = self.mSymbolPool.stringAt(ndx) or ''
                typeStr = ''
                outSymbol.package, typeStr, outSymbol.entry = \
                ResourceUtils.extractResourceName(astr)
                atype = self.parseResourceType(typeStr)
                if not atype:
                    return False
                outSymbol.type = atype
                #  Since we scan the symbol table in order, we can start looking for the
                #  next symbol from this point.
                self.mSymbolEntryCount -= i + 1
                self.mSymbolEntries += i + 1
                return True
        return False

    def parseTable(self, chunk):
        pass
        
    def parseSymbolTable(self, chunk):
        ##
        #  Parses the SymbolTable_header, which is present on non-final resource tables
        #  after the compile phase.
        #
        #  | SymbolTable_header |
        #  |--------------------|
        #  |SymbolTable_entry 0 |
        #  |SymbolTable_entry 1 |
        #  | ...                |
        #  |SymbolTable_entry n |
        #  |--------------------|
        #
        # /
        header = convertTo(chunk, SymbolTable_header)
        if not header:
            self.mContext.getDiagnostics().error = \
                self.mSource + "corrupt SymbolTable_header"
            return False

        entrySizeBytes = header.count * sizeof(SymbolTable_entry)
        if entrySizeBytes > getChunkDataLen(chunk):
            self.mContext.getDiagnostics().error = \
            self.mSource + "SymbolTable_header data section too long"
            return False

        self.mSymbolEntries = getChunkData(chunk)
        self.mSymbolEntryCount = header.count
        #  Skip over the symbol entries and parse the StringPool chunk that should be next.
        parser = ResChunkPullParser(getChunkData(header.header) + entrySizeBytes, \
                                    getChunkDataLen(header.header) - entrySizeBytes)
        if not ResChunkPullParser.isGoodEvent(parser.next()):
            self.mContext.getDiagnostics().error = \
                self.mSource + "failed to parse chunk in SymbolTable: %s" % parser.getLastError()
            return False

        nextChunk = parser.getChunk()
        if nextChunk.type != ResChunk_header.RES_STRING_POOL_TYPE:
            self.mContext.getDiagnostics().error = \
                self.mSource + "expected string pool in SymbolTable but got " + \
                "chunk of type %s" % nextChunk.type
            return False

        if self.mSymbolPool.setTo(nextChunk, nextChunk.size) != NO_ERROR:
            self.mContext.getDiagnostics().error = \
                self.mSource + "corrupt string pool in SymbolTable: %s" % mSymbolPool.getError()
            return False
        return True

    def parsePackage(self, chunk):
        pass
        
    def parsePublic(self, package, chunk):
        pass
        
    def parseTypeSpec(self, chunk):
        pass
        
    def parseType(self, package, chunk):
        pass
        
    def parseValue(self, name, config, value, flags):
        pass
        
    def parseMapEntry(self, name, config, map):
        pass
        
    def parseStyle(self, name, config, map):
        pass
        
    def parseAttr(self, name, config, map):
        pass
        
    def parseArray(self, name, config, map):
        pass
        
    def parsePlural(self, name, config, map):
        pass
        
    def parseStyleable(self, name, config, map):
        pass

##
#  Iterator functionality for ResTable_map_entry.
#
# inline const ResTable_map* begin(self, const ResTable_map_entry* map) {
#     return (self, const ResTable_map*)(self, (self, const uint8_t*) map + aapt::util::deviceToHost32(self, map->size));
# }
# inline const ResTable_map* end(self, const ResTable_map_entry* map) {
#     def begin(self, map) + aapt::util::deviceToHost32(self, map->count):
#         pass
# }
