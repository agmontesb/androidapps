# -*- coding: utf-8 -*-
import os
import sys
import io
import zipfile
import contextlib
import codecs
from collections import namedtuple
from ctypes import *

import ResourcesTypes as ru

def printHeader(base=16):
    headerStr = ' '.join(['OFFSET  '] + ['{:0>2x}'.format(x).upper() for x in range(base)])
    sepStr = lambda k: ('-' if k == 2 else '').join([k*'-' if (x + 1) % 4 else k*'+' for x in range(base)])
    print len(headerStr) * '-'
    print headerStr
    print 8*'-' + '-' + sepStr(2) + '   ' + sepStr(1)

def printHexIoData(data, offset, size=-1, base=16, shift=0, label=''):
    if offset is not None:
        offset = data.seek(offset)
    else:
        offset = 0
    size = 0x7FFF if size < 0 else size
    linf = shift / base
    lsup = (size - 1) / base + 1
    data.seek(offset + base * linf)
    for nlin in range(linf, lsup):
        colinf = (shift % base) if shift and nlin == linf else 0
        colsup = min(base * (nlin + 1), size) - base * nlin
        codes = ((colsup - colinf) * c_uint8)()
        breaded = data.readinto(codes)
        lsup = min(breaded, colsup - colinf)
        pos = map(lambda x: '{:0>2x}'.format(x).upper(), codes[:lsup])
        chars = label or ''.join(map(lambda x: chr(x) if 31 < x < 127 else '.', codes[:lsup]))
        saddr = '{:0>8x}'.format(base * nlin)
        # print saddr + ' ' + ' '.join(pos) + (base - lsup + 1)*'   '+ ''.join(chars)
        print saddr + ' ' + \
              colinf*'   ' + \
              ' '.join(pos) + \
              (base - colsup + 1)*'   ' + \
              chars
        if lsup < colsup - colinf: break

@contextlib.contextmanager
def ioData(data=None, offset=0, output=None):
    dataFlag = bool(data)
    if dataFlag:
        closeFlag = False
        if not hasattr(data, 'readinto'):
            if isinstance(data, basestring):
                if os.path.exists(data):
                    data = io.FileIO(data, 'rb')
                    closeFlag = True
                else:
                    data = io.BytesIO(data)
            else:
                raise ArgumentError('data must be an io object or a raw string')
        dataPtr = data.tell()
        offset += dataPtr
        data.seek(offset)
    outFlag = bool(output)
    if outFlag:
        output = codecs.getwriter('utf-8')(open(output, 'wb'))
        old_target, sys.stdout = sys.stdout, output
    try:
        yield data if dataFlag else None
    finally:
        if outFlag:
            sys.stdout = old_target
            output.close()
        if dataFlag:
            if closeFlag:
                data.close()
            else:
                data.seek(dataPtr)

def dumpHexData(data, offset=0, size=-1, base=16, outFile=None):
    with ioData(data, offset, output=outFile) as iodata:
        print 'BASE = {:0>8x}'.format(iodata.tell())
        printHeader(base)
        printHexIoData(iodata, iodata.tell(), size, base)

def dumpHexCtypeStruct(data, ctypeStruct, offset=0, outFile=None, shift=0, pheader=True, lprefix=''):
    # assert isinstance(ctypeStruct, Structure)
    with ioData(data, 0, output=outFile) as iodata:
        if pheader:
            print 'BASE = {:0>8x}'.format(iodata.tell())
            printHeader()
        for fname, fclass in ctypeStruct._fields_:
            fsize = sizeof(fclass)
            label = ('' if not lprefix else (lprefix + '.')) + fname
            if hasattr(fclass, '_fields_'):
                dumpHexCtypeStruct(iodata, fclass, offset=offset, shift=shift, pheader=False, lprefix=label)
            else:
                printHexIoData(iodata, offset=offset + shift, size=fsize + shift, shift=shift, label=label)
            shift += fsize

def aapt(**kwargs):
    aaptArgs = dict(
        action='',
        v=False,
        a=False,
        filename='',
        logFile=None,
        values=None,
        include_meta_data=False,
        what='',
        assets=[]
    )
    aaptArgs.update(**kwargs)
    Args = type('Args', (object,), aaptArgs)
    # Checking positional args
    if Args.action not in ['crawl', 'l', 'list', 'd', 'dump']:
        raise ArgumentError('Valid actions are "l[ist]", "d[ump]"')
    if os.path.splitext(Args.filename)[-1] not in ['.zip', '.jar', '.apk']:
        raise ArgumentError('Valid files are "zip", "jar" and "apk"')
    with ioData(output=Args.logFile):
        if Args.action in ['l', 'list']:
            if not (Args.v or Args.a):
                nopt = 1
            elif Args.a:
                nopt = 2
            elif Args.v:
                nopt = 0
            listApk(Args.filename, opt=nopt)
            return
        zf = zipfile.ZipFile(Args.filename)
        targetFunc = None
        args = ()
        kwargs = {}
        if Args.action == 'crawl':
            targetFunc = ResTableCrawler
            Args.assets = Args.assets or ['resources.arsc']
        elif Args.action in ['d', 'dump']:
            if Args.what in ['strings', 'resources', 'configurations']:
                targetFunc = dumpResources
                Args.assets = ('resources.arsc',)
                args = (Args.what,)
                kwargs = dict(incValues=Args.values, )
            elif Args.what in ['permissions', 'xmltree', 'xmlstrings']:
                targetFunc = dumpXmlTree
                if Args.what == 'permissions':
                    Args.assets = ('AndroidManifest.xml',)
                args = (Args.what,)
                # kwargs = dict(outFile=Args.logFile)
        for filename in Args.assets:
            file = io.BytesIO(zf.read(filename))
            with ioData(file, offset=0):
                targetFunc(file, *args, **kwargs)
    pass


class ResChunkHeader(ru.ResChunk_header):
    typeMap = {
        0x0000 : 'RES_NULL_TYPE',
        0x0001 : 'RES_STRING_POOL_TYPE',
        0x0002 : 'RES_TABLE_TYPE',
        0x0003 : 'RES_XML_TYPE',

        #  Chunk types in RES_XML_TYPE
        0x0100 : 'RES_XML_FIRST_CHUNK_TYPE',
        0x0100 : 'RES_XML_START_NAMESPACE_TYPE',
        0x0101 : 'RES_XML_END_NAMESPACE_TYPE',
        0x0102 : 'RES_XML_START_ELEMENT_TYPE',
        0x0103 : 'RES_XML_END_ELEMENT_TYPE',
        0x0104 : 'RES_XML_CDATA_TYPE',
        0x017f : 'RES_XML_LAST_CHUNK_TYPE',
        #  This contains a uint32_t array mapping strings in the string
        #  pool back to resource identifiers.  It is optional.
        0x0180 : 'RES_XML_RESOURCE_MAP_TYPE',

        #  Chunk types in RES_TABLE_TYPE
        0x0200 : 'RES_TABLE_PACKAGE_TYPE',
        0x0201 : 'RES_TABLE_TYPE_TYPE',
        0x0202 : 'RES_TABLE_TYPE_SPEC_TYPE',
        0x0203 : 'RES_TABLE_LIBRARY_TYPE',
    }

    @property
    def typeName(self):
        return self.typeMap.get(self.type)

    def isValid(self):
        return self.typeName and self.headerSize <= self.size

    def hasData(self):
        return self.typeName in [
            'RES_STRING_POOL_TYPE',
            'RES_TABLE_TYPE_TYPE',
            'RES_TABLE_TYPE_SPEC_TYPE',
            'RES_XML_START_NAMESPACE_TYPE',
            'RES_XML_END_NAMESPACE_TYPE',
            'RES_XML_START_ELEMENT_TYPE',
            'RES_XML_END_ELEMENT_TYPE',
            'RES_XML_CDATA_TYPE',
            'RES_XML_RESOURCE_MAP_TYPE',
        ]


class ResTableTypeSpec(ru.ResTable_typeSpec):
    confFlagsMap = dict(
        ACONFIGURATION_MCC=0x0001,
        ACONFIGURATION_MNC = 0x0002,
        ACONFIGURATION_LOCALE = 0x0004,
        ACONFIGURATION_TOUCHSCREEN = 0x0008,
        ACONFIGURATION_KEYBOARD = 0x0010,
        ACONFIGURATION_KEYBOARD_HIDDEN = 0x0020,
        ACONFIGURATION_NAVIGATION = 0x0040,
        ACONFIGURATION_ORIENTATION = 0x0080,
        ACONFIGURATION_DENSITY = 0x0100,
        ACONFIGURATION_SCREEN_SIZE = 0x0200,
        ACONFIGURATION_VERSION = 0x0400,
        ACONFIGURATION_SCREEN_LAYOUT = 0x0800,
        ACONFIGURATION_UI_MODE = 0x1000,
        ACONFIGURATION_SMALLEST_SCREEN_SIZE = 0x2000,
        ACONFIGURATION_LAYOUTDIR = 0x4000,
        ACONFIGURATION_SCREEN_ROUND = 0x8000,
        ACONFIGURATION_COLOR_MODE = 0x10000,
    )
    confFlagsMap = {value:key[1:] for key, value in confFlagsMap.items()}

    def __init__(self, data, offset=None):
        offset = offset or data.tell()
        data.seek(offset)
        data.readinto(self)
        if self.entryCount:
            self.data = (self.entryCount * c_uint32)()
            data.readinto(self.data)
        else:
            self.data = None

    def confFlags(self, idx):
        try:
            flags = self.data[idx]
        except:
            return
        mflags = lambda flags: reduce(
            lambda t, x, strFlags=bin(flags): ([1 << (len(strFlags) - 1 - x)] + t) if strFlags[x] == '1' else t, range(len(bin(flags))), []
        )
        return ' | '.join([self.confFlagsMap[x] for x in mflags(flags)]) if flags else 'CONFIGURATION_DEFAULT'


class ResTableType(ru.ResTable_type):
    def __init__(self, data, offset=None):
        headerOffset = offset or data.tell()
        data.seek(headerOffset)
        data.readinto(self)
        self.res_entry = []
        self.res_value = []
        self.idx = []
        if not self.entryCount: return
        offset = headerOffset + self.entriesStart
        sparseOffset = offset
        data.seek(offset)
        bFlag= self.flags & ru.ResTable_type.FLAG_SPARSE
        if bFlag:
            entries = (self.res_entry * ru.ResTable_sparseTypeEntry)()
            data.readinto(entries)
        for k in range(self.entryCount):
            if bFlag:
                self.idx.append(entries[k].idx)
                offset = entries[k].offset + headerOffset
            if data.tell() != offset:
                data.seek(offset)
            entry = ru.ResTable_entry()
            offset += data.readinto(entry)
            self.res_entry.append(entry)
            value = ru.Res_value()
            offset += data.readinto(value)
            self.res_value.append(value)

    def getEntryAt(self, idx):
        if self.flags & ru.ResTable_type.FLAG_SPARSE:
            try:
                idx = self.idx.index(idx)
            except:
                return
        try:
            return self.res_entry[idx], self.res_value[idx]
        except:
            pass

class GenCrawler(object):
    _allowed_cases_ = None

    @staticmethod
    def readResHeader(stream, headerClass, offset=None):
        if offset is not None:
            stream.seek(offset)
        x = headerClass()
        stream.readinto(x)
        return None if stream.tell() < offset + sizeof(headerClass) else x

    def crawl(self, file, headerClass=None):
        headerClass = headerClass or ResChunkHeader
        offset = 0
        stack = []
        while True:
            rch = self.readResHeader(file, headerClass, offset=offset)
            if not rch: break
            if not rch.isValid():
                raise ArgumentError('Error at 0x{:0>8x}, 0x{:0>4x} not a valid type'.format(offset, rch.type))
            elif self._allowed_cases_ and rch.type not in self.allowedCases:
                raise ArgumentError('Element at 0x{:0>8x} not an alloed RES_CHUNK_TYPE'.format(offset))
            depth = len(stack)
            yield (depth, offset, rch)
            if not stack or not rch.hasData():
                stack.append((offset, rch.type, rch.typeName, rch.headerSize, rch.size))
            offset += rch.headerSize
            if rch.hasData():
                offset += rch.size - rch.headerSize
            while stack and offset >= (stack[-1][0] + stack[-1][4]):
                stack.pop()
                # stack.pop()
            # if offset >= stack[0][4]: break
        assert not stack

class ResourceCrawler(GenCrawler):
    _allowedCases_ = [
        ru.ResChunk_header.RES_STRING_POOL_TYPE,
        ru.ResChunk_header.RES_TABLE_TYPE,
        ru.ResChunk_header.RES_TABLE_LIBRARY_TYPE,
        ru.ResChunk_header.RES_TABLE_TYPE_SPEC_TYPE,
        ru.ResChunk_header.RES_TABLE_TYPE_TYPE,
        ru.ResChunk_header.RES_TABLE_PACKAGE_TYPE
    ]

    def __init__(self):
        super(ResourceCrawler, self).__init__()
        self._resetcrawler_()

    def _resetcrawler_(self):
        self.nPackage = 0
        self.entryName = None
        self.entryValue = []
        self.configData = []

    def getValueRep(self, stringPool, resvalue):
        case = resvalue.dataType
        if case == resvalue.TYPE_STRING:
            prtStr = '(string8)' if stringPool.isUTF8() else '(string16)'
            return prtStr + ' "%s"' % stringPool.stringAt(resvalue.data)
        elif case == resvalue.TYPE_FLOAT:
            return '(float) **************'
        elif case == resvalue.TYPE_DIMENSION or case == resvalue.TYPE_FRACTION:
            complex = resvalue.data
            mantissa = (complex >> resvalue.COMPLEX_MANTISSA_SHIFT) & resvalue.COMPLEX_MANTISSA_MASK
            neg = mantissa > (1 << 23)
            if neg: mantissa ^= resvalue.COMPLEX_MANTISSA_MASK
            radix = (complex >> resvalue.COMPLEX_RADIX_SHIFT) & resvalue.COMPLEX_RADIX_MASK
            shift = 1 << max(8, 8 * (radix + 1) - 1)
            fvalue = (mantissa << resvalue.COMPLEX_MANTISSA_SHIFT) * (1.0 / shift)
            if neg: fvalue = -fvalue
            if case == resvalue.TYPE_DIMENSION:
                fkey = 'dimension'
                COMPLEX_UNITS = ["px", "dp", "sp", "pt", "in", "mm"]
            else:
                fkey = 'fraction'
                COMPLEX_UNITS = ["%", "%p"]
            funits = COMPLEX_UNITS[(complex >> resvalue.COMPLEX_UNIT_SHIFT) & resvalue.COMPLEX_UNIT_MASK]
            return '({}) {:0.6f}{}'.format(fkey, fvalue, funits)
        elif resvalue.TYPE_FIRST_INT <= case <= resvalue.TYPE_LAST_INT:
            if case == resvalue.TYPE_INT_DEC:
                return '(integer) %s' % resvalue.data
            if case == resvalue.TYPE_INT_HEX:
                return '(integer) 0x{:0>8x}'.format(resvalue.data)
            if case == resvalue.TYPE_INT_BOOLEAN:
                return '(boolean) %s' % bool(resvalue.data)
            if case == resvalue.TYPE_INT_COLOR_ARGB8:
                return '(color) #{:0>8x}'.format(resvalue.data)
            if case == resvalue.TYPE_INT_COLOR_RGB8:
                return '(color) #{:0>8x}'.format(resvalue.data)
            if case == resvalue.TYPE_INT_COLOR_ARGB4:
                return '(color) #{:0>4x}'.format(resvalue.data)
            if case == resvalue.TYPE_INT_COLOR_RGB4:
                return '(color) #{:0>4x}'.format(resvalue.data)
        if case == resvalue.TYPE_NULL:
            return '(null) ' + 'UNDIFINED' if not resvalue.data else 'EMPTY'
        else:
            if case == resvalue.TYPE_REFERENCE:
                fkey = 'reference'
            elif case == resvalue.TYPE_ATTRIBUTE:
                fkey =  'attribute'
            elif case == resvalue.TYPE_DYNAMIC_REFERENCE:
                fkey =  'dynamic reference'
            elif case == resvalue.TYPE_DYNAMIC_ATTRIBUTE:
                fkey = 'dynamic attribute'
            return '({}) 0x{:0>8x}'.format(fkey, resvalue.data)

    def crawl(self, file):
        crawler = super(ResourceCrawler, self).crawl(file)
        for dummy, offset, rch in crawler:
            self.rch = rch
            case = rch.type
            if case == ru.ResChunk_header.RES_TABLE_TYPE_TYPE:
                nConfig += 1
                rtt = self.readResHeader(file, ru.ResTable_type, offset=offset)
                if self.startResTableTypeHandler(nPackage, nConfig, rtt):
                    break
                notSparse = not rtt.flags & ru.ResTable_type.FLAG_SPARSE
                resClass = c_uint32 if notSparse else ru.ResTable_sparseTypeEntry
                indx = self.readResHeader(file, (rtt.entryCount * resClass), offset=offset + rtt.header.headerSize)
                for k in range(rtt.entryCount):
                    if notSparse:
                        if indx[k] == ru.ResTable_type.NO_ENTRY:continue
                        eOff = offset + rtt.entriesStart + indx[k]
                    else:
                        eOff = offset + rtt.entriesStart + indx[k].offset # OJO dice que debe dividirse por 4
                    entry = self.readResHeader(file, ru.ResTable_entry, offset=eOff)
                    if not entry.flags & ru.ResTable_entry.FLAG_COMPLEX:
                        value = self.readResHeader(file, ru.Res_value, offset=eOff + sizeof(entry))
                        s, r, t, d = value.size, value.res0, value.dataType, value.data
                        strValue = 't=0x{:0>2x} d=0x{:0>8x} (s=0x{:0>4x} r=0x{:0>2x})'.format(t, d, s, r)
                    else:
                        rtme = self.readResHeader(file, ru.ResTable_map_entry, offset=eOff + sizeof(entry))
                        rtm = self.readResHeader(file, (rtme.count*ru.ResTable_map), offset=eOff + sizeof(entry) + sizeof(rtme))
                        value = (rtme.parent, rtm)
                        strValue = '<bag>'
                    entryid, entryname, entryvalue = k, entry.key, value
                    if self.entryDataHandler(nConfig, entryid, entryname, entryvalue):
                        break
                if self.endResTableTypeHandler(nPackage, nConfig):
                    break
                header = self.readResHeader(file, ru.ResChunk_header)
                if header.type == case: continue
                if self.endResTableTypeSpecHandler(nPackage):
                    break
                if header.type == ru.ResChunk_header.RES_TABLE_TYPE:
                    if self.endResTablePackageHandler(nPackage):
                        break
            elif case == ru.ResChunk_header.RES_TABLE_TYPE_SPEC_TYPE:
                rtts = self.readResHeader(file, ru.ResTable_typeSpec, offset=offset)
                offset += rtts.header.headerSize
                if not rtts.entryCount:
                    continue
                nConfig = -1
                flags = self.readResHeader(file, (rtts.entryCount * c_uint32), offset=offset)
                if self.startResTableTypeSpecHandler(nPackage, rtts, flags):
                    break
                self.entryName = (rtts.entryCount * ru.ResStringPool_ref)()
                self.configData = []
            elif case == ru.ResChunk_header.RES_TABLE_PACKAGE_TYPE:
                nPackage += 1
                rtp = self.readResHeader(file, ru.ResTable_package, offset=offset)
                if self.startResTablePackageHandler(nPackage, rtp):
                    break
            elif case == ru.ResChunk_header.RES_STRING_POOL_TYPE:
                stringpool = ru.ResStringPool(file, offset=offset)
                dmySpArr += 1
                if self.stringPoolHandler(dmySpArr, stringpool):
                    break
            elif case == ru.ResChunk_header.RES_TABLE_TYPE:
                dmySpArr = 0
                nPackage = -1
                rth = self.readResHeader(file, ru.ResTable_header, offset=offset)
                if self.startResTableHandler(rth.packageCount):
                    break
            elif case == ru.ResChunk_header.RES_TABLE_LIBRARY_TYPE:
                pass

    @staticmethod
    def startResTableHandler(packageCount):
        pass

    @staticmethod
    def stringPoolHandler(spType, stringPool):
        pass

    @staticmethod
    def startResTablePackageHandler(nPackage, rtp):
        pass

    @staticmethod
    def endResTablePackageHandler(nPackage):
        pass

    @staticmethod
    def startResTableTypeSpecHandler(nPackage, rtts, flags):
        pass

    @staticmethod
    def endResTableTypeSpecHandler(nPackage):
        pass

    @staticmethod
    def startResTableTypeHandler(nPackage, nConfig, rtt):
        pass

    @staticmethod
    def endResTableTypeHandler(nPackage, nConfig):
        pass

    @staticmethod
    def entryDataHandler(nConfig, entryid, entryname, entryvalue):
        pass


def dumpResources(file, what, incValues=False, include_meta_data=False, outFile=None):
    INDENT = '  '
    spArray = []
    rtpArray = []
    flagsArray = []
    rttArray = []
    rttsArray = []
    entryInfo = {}
    configData = []

    rc = ResourceCrawler()

    with ioData(file, 0, output=outFile) as file:
        if what == 'strings':
            def handler(spType, dmySp):
                nStrings = dmySp.stringCount()
                encoding = 'UTF-8' if dmySp.isUTF8() else 'UTF-8'
                sorted = 'sorted' if dmySp.isSorted() else 'non-sorted'
                nStyles = dmySp.styleCount()
                bytes = rc.rch.size
                prtStr = 'String pool of {0} unique {1} {2} strings, ' \
                         '{0} entries and {3} styles using {4} bytes:'.format(
                    nStrings, encoding, sorted, nStyles, bytes,
                )
                print prtStr
                for k in range(nStrings):
                    print 'String #%s: %s' % (k, dmySp.stringAt(k))
                return 1
            rc.stringPoolHandler = handler

        if what == 'resources':
            def handler(packageCount):
                print 'Package Groups (%s)' % packageCount
            rc.startResTableHandler = handler

            def handler(spType, stringPool):
                spArray.append(stringPool)
            rc.stringPoolHandler = handler

            def handler(nPackage, rtp):
                rtpArray.append(rtp)
                pckName = bytearray(rtp.name).decode('UTF-16').split('\0', 1)[0]
                prtStr = 'Package {} id=0x{:0>2x} name={}'.format(nPackage, rtp.id, pckName)
                print 1 * INDENT + prtStr
            rc.startResTablePackageHandler = handler

            def handler(nPackage, rtts, flags):
                rttsArray.append(rtts)
                flagsArray.append(flags)
            rc.startResTableTypeSpecHandler = handler

            def handler(nPackage):
                rtp = rtpArray[-1]
                pckName = bytearray(rtp.name).decode('UTF-16').split('\0', 1)[0]
                flags = flagsArray.pop()
                rtts = rttsArray.pop()
                rtt =  rttArray.pop()
                prtStr = 'type {} configCount={} entryCount={}'
                prtStr = prtStr.format(rtts.id - 1, len(configData), rtts.entryCount)
                print 2 * INDENT + prtStr
                for k in range(rtts.entryCount):
                    resId = ru.Res_MAKEID(rtp.id - 1, rtts.id - 1, k)
                    strId = '%s:%s/%s' % (pckName, spArray[1].stringAt(rtts.id - 1), spArray[2].stringAt(entryInfo[k]))
                    prtStr = 'spec resource 0x{:0>8x} {}: flags=0x{:0>8x}'.format(resId, strId, flags[k])
                    print 3 * INDENT + prtStr
                while configData:
                    entryValue = configData.pop(0)
                    print 3 * INDENT + 'config ****-****:'
                    for idx, value in entryValue:
                        ename = spArray[2].stringAt(entryInfo[idx])
                        resId = ru.Res_MAKEID(rtp.id - 1, rtt.id - 1, idx)
                        strId = '%s:%s/%s' % (pckName, spArray[1].stringAt(rtts.id - 1), ename)
                        isBag = isinstance(value, tuple)
                        if isBag:
                            strValue = '<bag>'
                        else:
                            s, r, t, d = value.size, value.res0, value.dataType, value.data
                            strValue = 't=0x{:0>2x} d=0x{:0>8x} (s=0x{:0>4x} r=0x{:0>2x})'.format(t, d, s, r)
                        prtStr = '{}resource 0x{:0>8x} {}: {}'
                        print 4 * INDENT + prtStr.format('spec ' if not incValues else '', resId, strId, strValue)
                        if incValues:
                            if not isBag:
                                ptrStr = rc.getValueRep(spArray[0], value)
                                print 5 * INDENT + ptrStr.format(value.data)
                            else:
                                ptrStr = 'Parent=0x{:0>8x}(Resolved=0x{:0<8x}), Count={}'
                                print 5 * INDENT + ptrStr.format(value[0].ident, 0x7f, len(value[1]))
                                ptrStr = '#{} (Key=0x{:0>8x}): {}'
                                for k, rtm in enumerate(value[1]):
                                    print 5 * INDENT + ptrStr.format(k, rtm.name.ident, rc.getValueRep(spArray[0], rtm.value))
                entryInfo.clear()
            rc.endResTableTypeSpecHandler = handler

            def handler(nPackage, nConfig, rtt):
                rttArray.append(rtt)
                configData.append([])
            rc.startResTableTypeHandler = handler

            def handler(nConfig, entryid, entryname, entryvalue):
                entryValue = configData[-1]
                if not entryInfo.has_key(entryid):
                    entryInfo[entryid] = entryname
                entryValue.append((entryid, entryvalue))
            rc.entryDataHandler = handler

        rc.crawl(file)

def ResTableCrawler(file, headerClass=None, logFile=None):
    def reportData(indent, data):
        fmtStr = indent * INDENT + '0x{1:0>4x} {2} 0x{0:0>8x} {3} {4}'
        print fmtStr.format(*data).upper()
    rc = GenCrawler()
    INDENT = '    '
    # print 'Crawling: %s' % filename
    with ioData(file, 0, output=logFile) as file:
        for depth, offset, rch in rc.crawl(file, headerClass):
            reportData(depth, (offset, rch.type, rch.typeName, rch.headerSize, rch.size))
            if rch.hasData():
                data = (offset + rch.headerSize, 0xFFFF, 'ARRAY_TYPE', 0, rch.size - rch.headerSize)
                reportData(depth + 1, data)


class NameSpace(object):
    def __init__(self):
        self._prefix = []
        self._uri = []

    def add(self, prefix, uri):
        self._prefix.append(prefix)
        self._uri.append(uri)

    def remove(self, prefix, uri):
        k = self._indexFor(uri)
        if k < 0:
            raise ArgumentError('(%s, %s) not in namespace' % (prefix, uri))
        self._prefix.pop(k)
        self._uri.pop(k)

    def prefixForUri(self, uri):
        k = self._indexFor(uri)
        if k < 0:
            raise ArgumentError('uri=%s not in namespace' % uri)
        return self._prefix[k]

    def _indexFor(self, uri):
        kmax = len(self._uri)
        kmin = 0
        k = kmax - 1
        while kmin <= k < kmax and self._uri[k] != uri:
            k -= 1
        return k

def dumpXmlTree(filename, dcase='xmltree', headerClass=None, outFile=None):
    if dcase not in ['xmlstrings', 'xmltree', 'permissions']:
        raise ArgumentError('dcase="%s" is not a valid case' % dcase)
    namespace = NameSpace()
    dmySp = None
    dmyAttrsIds = None
    INDENT = '  '
    depth = -1
    bXmlInfo = False
    rc = GenCrawler()
    with ioData(filename, 0, output=outFile) as file:
        for dummy, offset, rch in rc.crawl(file, headerClass):
            case = rch.type
            try:
                cData = XmlFactory(file, dmySp, namespace, attrIds=dmyAttrsIds, offset=offset)
                cType = cData[0]
                if cType == ru.ResChunk_header.RES_XML_START_ELEMENT_TYPE:
                    depth += 1
                    if dcase == 'xmltree':
                        print depth * INDENT + 'E: {2} (line={1})'.format(*cData)
                        for key, value, resId in cData[3]:
                            key = key.split('}')[-1]
                            resId = '(0x{:0>8x})'.format(resId) if resId else ''
                            if isinstance(value, basestring):
                                prtStr = 'A: {0}{2}="{1}" (Raw: "{1}")'.format(key, value, resId)
                            else:
                                prtStr = 'A: {0}{3}=(type 0x{1:0>2x})(0x{2:0>8x})'.format(key, value.dataType, value.data, resId)
                            print (depth + 1) * INDENT + prtStr
                    elif dcase == 'permissions' and cData[2] == 'uses-permission':
                        print "%s: name='%s'" % (cData[2], cData[3][0][1])
                elif cType == ru.ResChunk_header.RES_XML_END_ELEMENT_TYPE:
                    depth -= 1
                elif cType == ru.ResChunk_header.RES_XML_START_NAMESPACE_TYPE:
                    depth += 1
                    if dcase == 'xmltree':
                        print depth * INDENT + 'N: {2}={3}'.format(*cData)
                elif cType == ru.ResChunk_header.RES_XML_END_NAMESPACE_TYPE:
                    depth -= 1
                elif cType == ru.ResChunk_header.RES_XML_CDATA_TYPE:
                    print (depth + 1) * INDENT + 'D: {2} (line={1})'.format(*cData)
            except Exception as e:
                if case == ru.ResChunk_header.RES_STRING_POOL_TYPE and bXmlInfo:
                    dmySp = ru.ResStringPool(file, offset=offset)
                    if dcase == 'xmlstrings':
                        nStrings = dmySp.stringCount()
                        encoding = 'UTF-8' if dmySp.isUTF8() else 'UTF-8'
                        sorted = 'sorted' if dmySp.isSorted() else 'non-sorted'
                        nStyles = dmySp.styleCount()
                        bytes = rch.size
                        prtStr = 'String pool of {0} unique {1} {2} strings, ' \
                        '{0} entries and {3} styles using {4} bytes:'.format(
                            nStrings, encoding, sorted, nStyles, bytes,
                        )
                        print prtStr
                        for k in range(nStrings):
                            print 'String #%s: %s' % (k, dmySp.stringAt(k))
                        break
                elif case == ru.ResChunk_header.RES_XML_RESOURCE_MAP_TYPE:
                    nids = (rch.size - rch.headerSize) / sizeof(c_uint32)
                    offset += rch.headerSize
                    dmyAttrsIds = rc.readResHeader(file, (nids*c_uint32), offset)
                elif case == ru.ResChunk_header.RES_XML_TYPE:
                    bXmlInfo = True
                else:
                    pass   # raise e


def XmlFactory(data, resStringPool, namespace, attrIds=None, offset=None):
    _StateClass = namedtuple(
        '_StateClass', 'byte_index, line_number, column_number, depth, event_type, event_data'
    )
    stringAt = resStringPool.stringAt
    def fullTagName(ns, name):
        ns = stringAt(ns) or ''
        if ns:
            ns = '{%s}%s:' % (ns, namespace.prefixForUri(ns))
        name = stringAt(name)
        return ns + name
    headerOffset = offset or data.tell()
    resXMLTree_node = GenCrawler.readResHeader(data, ru.ResXMLTree_node, headerOffset)
    offset = headerOffset + resXMLTree_node.header.headerSize

    case = resXMLTree_node.header.type
    if not ru.ResChunk_header.RES_XML_FIRST_CHUNK_TYPE <= case <= ru.ResChunk_header.RES_XML_LAST_CHUNK_TYPE:
        raise ArgumentError('Element at 0x{:0>8x} not a RES_XML_CHUNK_TYPE'.format(headerOffset))
    elif case == ru.ResChunk_header.RES_XML_START_ELEMENT_TYPE:
        resXMLTree_attrExt = GenCrawler.readResHeader(data, ru.ResXMLTree_attrExt, offset)
        tag = fullTagName(resXMLTree_attrExt.ns, resXMLTree_attrExt.name)
        offset = headerOffset + resXMLTree_node.header.headerSize + resXMLTree_attrExt.attributeStart
        attributeSize = resXMLTree_attrExt.attributeSize
        attributeCount = resXMLTree_attrExt.attributeCount
        attr = GenCrawler.readResHeader(data, (attributeCount * ru.ResXMLTree_attribute), offset)
        assert attributeSize * attributeCount == sizeof(attr)
        attribs = []
        for k in range(attributeCount):
            ns, name, rawvalue, typedvalue = attr[k].ns, attr[k].name, attr[k].rawValue, attr[k].typedValue
            key = fullTagName(ns, name)
            value = stringAt(rawvalue) or typedvalue
            attribs.append((key, value, attrIds[name.index] if attrIds and '}' in key else None))
        return (case, resXMLTree_node.lineNumber, tag, attribs)
    elif case == ru.ResChunk_header.RES_XML_END_ELEMENT_TYPE:
        resXMLTree_endElementExt = GenCrawler.readResHeader(data, ru.ResXMLTree_endElementExt, offset)
        tag = fullTagName(resXMLTree_endElementExt.ns, resXMLTree_endElementExt.name)
        return (case, resXMLTree_node.lineNumber, tag,)
    elif case == ru.ResChunk_header.RES_XML_START_NAMESPACE_TYPE or \
            case == ru.ResChunk_header.RES_XML_END_NAMESPACE_TYPE:
        dataHeader = GenCrawler.readResHeader(data, ru.ResXMLTree_namespaceExt, offset)
        prefix = stringAt(dataHeader.prefix)
        uri = stringAt(dataHeader.uri)
        if case == ru.ResChunk_header.RES_XML_START_NAMESPACE_TYPE:
            namespace.add(prefix, uri)
        else:
            namespace.remove(prefix, uri)
        return (case, resXMLTree_node.lineNumber, prefix, uri)
    elif case == ru.ResChunk_header.RES_XML_CDATA_TYPE:
        dataHeader = GenCrawler.readResHeader(data, ru.ResXMLTree_cdataExt, offset)
        data = stringAt(dataHeader.data)
        typedData = str(dataHeader.typedData)
        return (case, resXMLTree_node.lineNumber, data, typedData)

def listApk(filename, opt=1):
    if not zipfile.is_zipfile(filename):
        raise ArgumentError('File: "%s" not a valid apk file')
    zf = zipfile.ZipFile(filename, 'r')
    if opt == 0:
        prtStr1 = '{:^8} {:^8} {:^8} {:^8} {:^8} {:^16} {:^8} {:^8}'
        print prtStr1.format('Length', 'Method', 'Size', 'Ratio', 'Offset', 'Date Time',
                            'CRC-32', 'Name')
        print 5 * (8 * '-' + ' ') + 16*'-' + 2*(' ' + 8 * '-')
        prtStr = '{:8d} {:8} {:8d} {:7d}% {:8d} {:16} {:8} {:8}'
        totsize = totcsize = 0
        for zinfo in zf.infolist():
            totsize += zinfo.file_size
            totcsize += zinfo.compress_size
            method = 'Deflate' if zinfo.compress_type == zipfile.ZIP_DEFLATED else 'Stored'
            ratio = int(100.0 - 100.0 * zinfo.compress_size / zinfo.file_size)
            date_time = '{0}-{1}-{2} {3}:{4}'.format(*zinfo.date_time[:-1])
            CRC = '{:0>8x}'.format(int(zinfo.CRC))
            data = (zinfo.file_size, method, zinfo.compress_size,
                    ratio, zinfo.header_offset, date_time, CRC, zinfo.filename)
            print prtStr.format(*data)
        ratio = int(100.0 - 100.0 * totcsize / totsize)
        print 8*'-' + 10* ' ' + 8*'-' + ' ' + 8*'-' + 27*' ' + 8*'-'
        prtStr = '{:8}' + 10* ' ' + '{:8}' + ' ' + '{:7}%' + 27*' ' + '{} files'
        print prtStr.format(totsize, totcsize, ratio, len(zf.namelist()))
    else:
        print '\n'.join(zf.namelist())
        if opt > 1:
            print '\n\nResource table:'
            file = io.BytesIO(zf.read('resources.arsc'))
            dumpResources(file)
            print '\n\nAndroid manifest:'
            file = io.BytesIO(zf.read('AndroidManifest.xml'))
            dumpXmlTree(file)





if __name__ == '__main__':
    import ResourcesTypes as ru
    apk = 'apk'
    test = 'test'
    apk0 = r'/media/amontesb/HITACHI/BASURA/ResourceTypesData/android-4.1.1.4.jar'
    apk1 = r'/media/amontesb/HITACHI/BASURA/ResourceTypesData/testAAPT/android/bin/hello.unaligned.apk'
    apk2 = r'/media/amontesb/HITACHI/BASURA/ResourceTypesData/Lunar Lander_v1.1.1_apkpure.com.apk'
    apk3 = r'/media/amontesb/HITACHI/BASURA/ResourceTypesData/teatv-9-2r.apk'
    resources = r'/media/amontesb/HITACHI/BASURA/ResourceTypesData/resources.arsc'
    manifest = r'/media/amontesb/HITACHI/BASURA/ResourceTypesData/AndroidManifest.xml'
    commandline = r'commandline'
    filename = commandline
    try:
        with open(filename, 'rb') as f:
            fileStr = f.read()
        file = io.open(filename, 'rb')
    except:
        pass

    if filename == test:
        zf = zipfile.ZipFile(apk2)
        data = io.BytesIO(zf.read('resources.arsc'))
        with ioData(data, 0, output='/media/amontesb/HITACHI/BASURA/ResourceTypesData/test.txt') as file:
            dumpResources(file, 'resources', values=True)
    elif filename == commandline:
        kwargs = dict(
            # logFile='/media/amontesb/HITACHI/BASURA/ResourceTypesData/test.txt',
            filename=apk3,      # file.{zip, jar, apk}
            action='dump',         # l[ist], d[ump]
            # parametros
            # list ->           -a -v
            # dump ->           --values, --include-meta-data WHAT [asset [asset ...]
            what='resources',
            assets=['AndroidManifest.xml', 'res/layout/activity_main.xml',],
        )
        aapt(**kwargs)
        pass
    elif filename == apk1:
        listApk(filename, 2)
    elif filename == resources:
        ResTableCrawler(filename)
        dumpResources(filename)
    elif filename == manifest:
        ResTableCrawler(filename)
        dmySp = ru.ResStringPool(file, 0X00000008)
        namespace = NameSpace()
        dumpXmlChunk = lambda x: XmlFactory(file, dmySp, namespace, offset=x)
        print dumpXmlChunk(0X000006FC)
        print dumpXmlChunk(0X00000714)
        print dumpXmlChunk(0x00000950)
        print dumpXmlChunk(0X00000C00)
        dumpXmlTree(filename, dcase='permissions')


