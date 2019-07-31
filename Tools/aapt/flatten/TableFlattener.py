# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/flatten/TableFlattener.h
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/flatten/TableFlattener.cpp
#
import ctypes
import collections

from Tools.aapt.BigBuffer import BigBuffer
from Tools.aapt.Compile.ResourceTable import ResourceTableType
from Tools.aapt.Resource import ResourceType, ResourceId, ResourceNameRef
from Tools.aapt.StringPool import StringPool
from Tools.aapt.ResourcesValues import Reference, Attribute, BinaryPrimitive, \
    Style, Styleable, Array, Plural
from Tools.aapt.ResourcesTypes import Res_value, ResTable_type, \
    ResTable_typeSpec, ResTable_entry, ResTable_header, ResTable_package, ResTable_map
from Tools.aapt.ResourceTypeExtensions import ResTable_entry_ext, ResTable_entry_source, \
    Public_header, Public_entry, RES_TABLE_PUBLIC_TYPE, RES_TABLE_SOURCE_POOL_TYPE, RES_TABLE_SYMBOL_TABLE_TYPE, \
    SymbolTable_header, SymbolTable_entry
from Tools.aapt.flatten.ChunkWriter import ChunkWriter

from Tools.aapt.ResourcesTypes import ResChunk_header

RES_TABLE_TYPE = ResChunk_header.RES_TABLE_TYPE
RES_TABLE_TYPE_SPEC_TYPE = ResChunk_header.RES_TABLE_TYPE_SPEC_TYPE
RES_TABLE_TYPE_TYPE = ResChunk_header.RES_TABLE_TYPE_TYPE
RES_TABLE_PACKAGE_TYPE = ResChunk_header.RES_TABLE_PACKAGE_TYPE


class SymbolWriter(object):
    Entry = collections.namedtuple('Entry', 'name offset')

    def __init__(self):
        super(SymbolWriter, self).__init__()
        self.pool = StringPool()
        self.symbols = []

    def addSymbol(self, name, offset):
        self.symbols.append(
            SymbolWriter.Entry(
                self.pool.makeRef(name.toString()),
                offset
            )
        )


class MapFlattenVisitor(object):

    def __init__(self, symbols, entry, buffer):
        super(MapFlattenVisitor, self).__init__()
        self.mSymbols = symbols
        self.mEntry = entry
        self.mBuffer = buffer
        self.mEntryCount = 0
        self.mParentIdent = None
        self.mParentName = None
    
    def flattenKey(self, key, outEntry):
        if not key.id:
            assert key.name, "reference must have a name"
            outEntry.name.ident = 0
            self.mSymbols.addSymbol(
                key.name,
                (self.mBuffer.size() - ctypes.sizeof(ResTable_map)) +
                ResTable_map.name.offset
            )
        else:
            outEntry.name.ident = key.id.id
        
    
    def flattenValue(self, value, outEntry):
        ref = value if isinstance(value, Reference) else None
        if ref:
            if not ref.id:
                assert ref.name, "reference must have a name"
                self.mSymbols.addSymbol(
                    ref.name,
                    (self.mBuffer.size() - ctypes.sizeof(ResTable_map)) +
                    ResTable_map.value.offset + Res_value.data.offset
                )
        result = value.flatten(outEntry.value)
        assert result, "flatten failed"
    
    def flattenEntry(self, key, value):
        outEntry = self.mBuffer.nextBlock(ResTable_map)
        self.flattenKey(key, outEntry)
        self.flattenValue(value, outEntry)
        outEntry.value.size = ctypes.sizeof(outEntry.value)
        self.mEntryCount += 1
    
    @staticmethod
    def cmpStyleEntries(a, b):
        if a.key.id:
            if b.key.id:
                return a.key.id < b.key.id
            return True
        elif not b.key.id:
            return a.key.name < b.key.name
        return False
    
    def visit(self, arg1):
        if isinstance(arg1, Attribute):
            attr = arg1
            key = Reference(ResourceId(ResTable_map.ATTR_TYPE))
            val = BinaryPrimitive(Res_value.TYPE_INT_DEC, attr.typeMask)
            self.flattenEntry(key, val)

            for s in attr.symbols:
                val = BinaryPrimitive(Res_value.TYPE_INT_DEC, s.value)
                self.flattenEntry(s.symbol, val)
        elif isinstance(arg1, Style):
            style = arg1
            if style.parent:
                if not style.parent.id:
                    assert style.parent.name, "reference must have a name"
                    self.mParentName = style.parent.name
                else:
                    self.mParentIdent = style.parent.id.id
            #  Sort the style.
            style.entries.sort(cmp=self.cmpStyleEntries)
            for entry in style.entries:
                self.flattenEntry(entry.key, entry.value)
        elif isinstance(arg1, Styleable):
            styleable = arg1
            for attrRef in styleable.entries:
                val = BinaryPrimitive(Res_value())
                self.flattenEntry(attrRef, val)
        elif isinstance(arg1, Array):
            array = arg1
            for item in array.items:
                outEntry = self.mBuffer.nextBlock(ResTable_map)
                self.flattenValue(item, outEntry)
                outEntry.value.size = ctypes.sizeof(outEntry.value)
                self.mEntryCount += 1
        elif isinstance(arg1, Plural):
            plural = arg1
            count = len(plural.values)
            for i in range(count):
                if not plural.values[i]:continue
                q = ResourceId()
                if i == Plural.Zero:
                    q.id = ResTable_map.ATTR_ZERO
                elif i == Plural.One:
                    q.id = ResTable_map.ATTR_ONE
                elif i == Plural.Two:
                    q.id = ResTable_map.ATTR_TWO
                elif i == Plural.Few:
                    q.id = ResTable_map.ATTR_FEW
                elif i == Plural.Many:
                    q.id = ResTable_map.ATTR_MANY
                elif i == Plural.Other:
                    q.id = ResTable_map.ATTR_OTHER
                else:
                    assert False
                key = Reference(q)
                self.flattenEntry(key, plural.values[i])

FlatEntry = collections.namedtuple('FlatEntry', 'entry value entryKey sourcePathKey sourceLine')
TableFlattenerOptions = collections.namedtuple('TableFlattenerOptions', 'useExtendedChunks')
TableFlattenerOptions.__new__.func_defaults = (False,)

class TableFlattener(object):

    def __init__(self, buffer, options):
        super(TableFlattener, self).__init__()
        self.mBuffer = buffer
        self.mOptions = options

    def consume(self, context, table):
        for package in table.packages:
            if context.getCompilationPackage() != package.name:
                errStr = "resources for package '%s' can't be flattened when compiling package '%s'"
                context.getDiagnostic().error = errStr % (package.name, context.getCompilationPackage())
                return False
            if not package.id or package.id != context.getPackageId():
                errStr = "package '%s' must have package id %s"
                context.getDiagnostic().error = errStr % (package.name, hex(context.getPackageId()))
                return False
            flattener = PackageFlattener(context.getDiagnostics(), self.mOptions, table, package)
            if not flattener.flattenPackage(self.mBuffer): return False
            return True
        context.getDiagnostics().error = "compilation package '%s' not found" % context.getCompilationPackage()
        return False


class PackageFlattener(object):

    def __init__(self, diag, options, table, package):
        super(PackageFlattener, self).__init__()
        self.mDiag = diag
        self.mOptions = options
        self.mTable = table
        self.mPackage = package
        self.mSymbols = SymbolWriter()
        self.mTypePool = StringPool()
        self.mKeyPool = StringPool()
        self.mSourcePool = StringPool()

    def writeEntry(self, entry, buffer, ctypeClass):
        assert issubclass(ctypeClass, (ResTable_entry, ResTable_entry_ext))
        result = buffer.nextBlock(ctypeClass)
        outEntry = result       # ResTable_entry(result)
        if entry.entry.publicStatus.isPublic:
            outEntry.flags |= ResTable_entry.FLAG_PUBLIC
        if entry.value.isWeak():
            outEntry.flags |= ResTable_entry.FLAG_WEAK
        if not entry.value.isItem():
            outEntry.flags |= ResTable_entry.FLAG_COMPLEX
        outEntry.key.index = entry.entryKey
        outEntry.size = ctypes.sizeof(ctypeClass)
        if self.mOptions.useExtendedChunks:
            sourceBlock = buffer.nextBlock(ResTable_entry_ext)
            sourceBlock.pathindex = entry.sourcePathKey
            sourceBlock.line = entry.sourceLine
            outEntry.size = ctypes.sizeof(sourceBlock)
            pass
        outEntry.flags = outEntry.flags
        outEntry.size = outEntry.size
        return result

    def flattenValue(self, entry, buffer):
        if entry.value.isItem():
            self.writeEntry(entry, buffer, ResTable_entry)
            ref = entry.value if isinstance(entry.value, Reference) else None
            if ref:
                if not ref.id:
                    assert ref.name, 'Reference must have at least a name'
                    self.mSymbols.addSymbol(ref.name, buffer.size() + Res_value.data.offset)
            outValue = buffer.nextBlock(Res_value)
            result = entry.value.flatten(outValue)
            assert result, 'flatten failed'
            outValue.size = ctypes.sizeof(outValue)
        else:
            beforeEntry = buffer.size()
            outEntry = self.writeEntry(entry, buffer, ResTable_entry_ext)
            visitor = MapFlattenVisitor(self.mSymbols, entry, buffer)
            entry.value.accept(visitor)
            outEntry.count = visitor.mEntryCount
            if visitor.mParentName:
                self.mSymbols.addSymbol(
                    visitor.mParentName,
                    beforeEntry + ResTable_entry_ext.parent.offset
                )
                pass
            elif visitor.mParentIdent:
                outEntry.parent.ident = visitor.mParentIdent
        return True


    def flattenConfig(self, atype, config, entries, buffer):
        typeWriter = ChunkWriter(buffer)
        typeHeader = typeWriter.startChunk(RES_TABLE_TYPE_TYPE, ResTable_type)
        typeHeader.id = atype.id
        typeHeader.config = config
        # typeHeader.config.swapHtoD()
        #  Find the largest entry ID. That is how many entries we will have.
        entryCount = max([a.id for a in atype.entries]) + 1
        typeHeader.entryCount = entryCount
        indices = typeWriter.nextBlock(ctypes.c_uint32, entryCount)
        assert entryCount <= 1 << 16 + 1
        ctypes.memset(indices, 0xff, entryCount * ctypes.sizeof(ctypes.c_uint32))
        typeHeader.entriesStart = typeWriter.size()
        entryStart = typeWriter.getBuffer().size()
        for flatEntry in entries:
            assert flatEntry.entry.id < entryCount
            indices[flatEntry.entry.id] =(
                typeWriter.getBuffer().size() - entryStart
            )
            if not self.flattenValue(flatEntry, typeWriter.getBuffer()):
                self.mDiag.error = \
                    "failed to flatten resource '" + \
                    ResourceNameRef(self.mPackage.name, atype.type, flatEntry.entry.name).toString() + \
                    "' for configuration '" + config.toString() + "'"
                return False
        typeWriter.finish()
        return True

    def collectAndSortTypes(self):
        sortedTypes = []
        for atype in self.mPackage.types:
            if atype.type == ResourceType.kStyleable and not self.mOptions.useExtendedChunks:
                #  Styleables aren't real Resource Types, they are represented in the R.java
                #  file.
                continue
            assert atype.id, "type must have an ID set"
            sortedTypes.append(atype)
        sortedTypes.sort(key=lambda x: x.id)
        return sortedTypes

    def collectAndSortEntries(self, atype):
        #  Sort the entries by entry ID.
        sortedEntries = []
        for entry in atype.entries:
            assert entry.id is not None, "entry must have an ID set"
            sortedEntries.append(entry)
        sortedEntries.sort(key=lambda x: x.id)
        return sortedEntries

    def flattenTypeSpec(self, atype, sortedEntries, buffer):
        typeSpecWriter= ChunkWriter(buffer)
        specHeader = typeSpecWriter.startChunk(RES_TABLE_TYPE_SPEC_TYPE, ResTable_typeSpec)
        specHeader.id = atype.id
        if not sortedEntries:
            typeSpecWriter.finish()
            return True
        #  We can't just take the size of the vector. There may be holes in the entry ID space.
        #  Since the entries are sorted by ID, the last one will be the biggest.
        numEntries = sortedEntries[-1].id + 1
        specHeader.entryCount = numEntries
        #  Reserve space for the masks of each resource in this type. These
        #  show for which configuration axis the resource changes.
        configMasks = typeSpecWriter.nextBlock(ctypes.c_uint32, numEntries)
        for entry in sortedEntries:
            #  Populate the config masks for this entry.
            if entry.publicStatus.isPublic:
                configMasks[entry.id] |= ResTable_typeSpec.SPEC_PUBLIC
            configCount = len(entry.values)
            for i in range(configCount):
                config = entry.values[i].config
                for j in range(i + 1, configCount):
                    configMasks[entry.id] |= config.diff(entry.values[j].config)
        typeSpecWriter.finish()
        return True

    def flattenPublic(self, atype, sortedEntries, buffer):
        publicWriter = ChunkWriter(buffer)
        publicHeader = publicWriter.startChunk(RES_TABLE_PUBLIC_TYPE, Public_header)
        publicHeader.typeId = atype.id
        for entry in sortedEntries:
            if not entry.publicStatus.isPublic: continue
            #  Write the public status of this entry.
            publicEntry = publicWriter.nextBlock(Public_entry)
            publicEntry.entryId = entry.id
            publicEntry.key.index = self.mKeyPool.makeRef(entry.name).getIndex()
            publicEntry.source.index = self.mSourcePool.makeRef(entry.publicStatus.source.path).getIndex()
            if entry.publicStatus.source.line:
                publicEntry.sourceLine = entry.publicStatus.source.line
            #  Don't hostToDevice until the last step.
            publicHeader.count += 1
        publicHeader.count = publicHeader.count
        publicWriter.finish()
        return True
    
    def flattenTypes(self, buffer):
        #  Sort the types by their IDs. They will be inserted into the StringPool in this order.
        sortedTypes = self.collectAndSortTypes()
        expectedTypeId = 1
        for atype in sortedTypes:
            #  If there is a gap in the type IDs, fill in the StringPool
            #  with empty values until we reach the ID we expect.
            while atype.id > expectedTypeId:
                typeName = u"?%s" % expectedTypeId
                self.mTypePool.makeRef(typeName)
                expectedTypeId += 1
            expectedTypeId += 1
            self.mTypePool.makeRef(ResourceType.toString(atype.type))
            sortedEntries = self.collectAndSortEntries(atype)
            if not self.flattenTypeSpec(atype, sortedEntries, buffer):
                return False
            if self.mOptions.useExtendedChunks:
                if not self.flattenPublic(atype, sortedEntries, buffer):
                    return False
            #  The binary resource table lists resource entries for each configuration.
            #  We store them inverted, where a resource entry lists the values for each
            #  configuration available. Here we reverse this to match the binary table.
            configToEntryListMap = collections.defaultdict(list)
            for entry in sortedEntries:
                keyIndex = self.mKeyPool.makeRef(entry.name).getIndex()
                #  Group values by configuration.
                for configValue in entry.values:
                    path, line = configValue.source.split(':') \
                        if ':' in configValue.source else (configValue.source, '0')
                    configToEntryListMap[configValue.config].append(
                        FlatEntry(
                            entry, configValue.value, keyIndex,
                            self.mSourcePool.makeRef(path).getIndex(),
                            int(line)
                        )
                   )
            #  Flatten a configuration value.
            for config, entry in configToEntryListMap.items():
                if not self.flattenConfig(atype, config, entry, buffer):
                    return False
        return True
    
    def flattenPackage(self, buffer):
        #  We must do this before writing the resources, since the string pool IDs may change.
        def strPoolcmp(a, b):
            diff = a.context.priority - b.context.priority
            if diff < 0: return True
            if diff > 0: return False
            diff = a.context.config.compare(b.context.config)
            if diff < 0: return True
            if diff > 0: return False
            return a.value < b.value
        self.mTable.stringPool.sort(strPoolcmp)
        self.mTable.stringPool.prune()
        beginningIndex = buffer.size()
        typeBuffer = BigBuffer(1024)
        if not self.flattenTypes(typeBuffer):
            return False
        tableWriter = ChunkWriter(buffer)
        tableHeader = tableWriter.startChunk(RES_TABLE_TYPE, ResTable_header)
        tableHeader.packageCount = 1
        symbolEntryData = None
        if self.mOptions.useExtendedChunks and self.mSymbols.symbols:
            #  Sort the offsets so we can scan them linearly.
            self.mSymbols.symbols.sort(cmp=lambda a, b: cmp(a.offset, b.offset))
            symbolWriter = ChunkWriter(tableWriter.getBuffer())
            symbolHeader = symbolWriter.startChunk(RES_TABLE_SYMBOL_TABLE_TYPE, SymbolTable_header)
            symbolHeader.count = len(self.mSymbols.symbols)
            symbolEntryData = symbolWriter.nextBlock(SymbolTable_entry, len(self.mSymbols.symbols))
            StringPool.flattenUtf8(self.mSymbols.pool, symbolWriter.getBuffer())
            symbolWriter.finish()
        
        if self.mOptions.useExtendedChunks and self.mSourcePool.size() > 0:
            #  Write out source pool.
            srcWriter = ChunkWriter(tableWriter.getBuffer())
            srcWriter.startChunk(RES_TABLE_SOURCE_POOL_TYPE, ResChunk_header)
            StringPool.flattenUtf8(self.mSourcePool, srcWriter.getBuffer())
            srcWriter.finish()
        StringPool.flattenUtf8(self.mTable.stringPool, tableWriter.getBuffer())
        pkgWriter = ChunkWriter(tableWriter.getBuffer())
        pkgHeader = pkgWriter.startChunk(RES_TABLE_PACKAGE_TYPE, ResTable_package)
        pkgHeader.id = self.mPackage.id
        if len(self.mPackage.name) >= 128:
            self.mDiag.error = \
                "package name '" + self.mPackage.name + "' is too long"
            return False
        pkgHeader.name = self.mPackage.name.encode('utf-8')
        pkgHeader.typeStrings = pkgWriter.size()
        StringPool.flattenUtf16(self.mTypePool, pkgWriter.getBuffer())
        pkgHeader.keyStrings = pkgWriter.size()
        StringPool.flattenUtf16(self.mKeyPool, pkgWriter.getBuffer())
        #  Actually write out the symbol entries if we have symbols.
        if symbolEntryData:
            for k, entry in enumerate(self.mSymbols.symbols):
                symbolEntryData[k].stringIndex = entry.name.getIndex()
                #  The symbols were all calculated with the typeBuffer offset. We need to
                #  add the beginning of the output buffer.
                symbolEntryData[k].offset = pkgWriter.getBuffer().size() - beginningIndex + entry.offset
        #  Write out the types and entries.
        pkgWriter.getBuffer().appendBuffer(typeBuffer)
        pkgWriter.finish()
        tableWriter.finish()
        return True
    
