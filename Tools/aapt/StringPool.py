# -*- coding: utf-8 -*-
import ctypes
from collections import namedtuple

from Tools.aapt import ResourcesTypes as rt

pointee = lambda x: x.__pointee__()
redirect = lambda x, y: x.__redirect__(y)

Span = namedtuple('Span', 'name firstChar lastChar')
StyleString = namedtuple('StyleString', 'str spans')


class StringPool(object):
    Context = namedtuple('Context', 'priority config')

    class Ref(object):

        def __init__(self, arg1=None):
            super(StringPool.Ref, self).__init__()
            self._mEntry = None
            if isinstance(arg1, StringPool.Ref):
                self._mEntry = arg1._mEntry
            elif isinstance(arg1, StringPool.Entry):
                self._mEntry = arg1

            if self._mEntry:
                self._mEntry.ref += 1

        def __del__(self):
            self._mEntry.ref -= 1

        def __pointee__(self):
            # const std::u16string& StringPool::Ref::operator*()
            return self._mEntry.value

        def __redirect__(self, rhs):
            # StringPool::Ref& StringPool::Ref::operator=(const StringPool::Ref& rhs)
            assert isinstance(rhs, StringPool.Ref)
            if rhs._mEntry != None:
                rhs._mEntry.ref += 1
            if self._mEntry != None:
                self._mEntry.ref -= 1
            self._mEntry = rhs._mEntry
            return self.__pointee__()

        def getIndex(self):
            return self._mEntry.index

        def getContext(self):
            return self._mEntry.context


    class StyleRef(object):

        def __init__(self, arg1=None):
            super(StringPool.StyleRef, self).__init__()
            self._mEntry = None
            if isinstance(arg1, StringPool.StyleRef):
                self._mEntry = arg1._mEntry
            elif isinstance(arg1, StringPool.StyleEntry):
                self._mEntry = arg1

            if self._mEntry:
                self._mEntry.ref += 1

        def __getattr__(self, item):
            return getattr(self._mEntry, item)

        def __del__(self):
            if self._mEntry:
                self._mEntry.ref -= 1

        def __redirect__(self, rhs):
            assert isinstance(rhs, StringPool.StyleRef)
            if rhs._mEntry:
                rhs._mEntry.ref += 1
            if self._mEntry:
                self._mEntry.ref -= 1
            self._mEntry = rhs._mEntry
            return self.__pointee__()

        def __pointee__(self):
            return self._mEntry.__pointee__()

        def getIndex(self):
            return self._mEntry.str.getIndex()

        def getContext(self):
            return self._mEntry.str.getContext()

    class Entry(object):
        def __init__(self):
            super(StringPool.Entry, self).__init__()
            self.value = None
            self.context = None
            self.index = None
            self.ref = 0

    Span = namedtuple('Span', 'name firstChar lastChar')

    class StyleEntry(object):
        def __init__(self):
            super(StringPool.StyleEntry, self).__init__()
            self.str = None
            self.spans = []
            self.ref = 0

        def __pointee__(self):
            return self.str.__pointee__()

    def __init__(self):
        super(StringPool, self).__init__()
        self.mStrings = []              # array of <Entry>
        self.mStyles = []               # array of <StyleEntry>
        self.mIndexedStrings = []       # dict with <key=str, value=<Entry>

    def _makeRefImpl(self, strPiece16, context, unique, spans):
        ehash = hash(strPiece16)
        if not spans and unique and ehash in self.mIndexedStrings:
            ndx = self.mIndexedStrings.index(ehash)
            return StringPool.Ref(self.mStrings[ndx])
        entry = StringPool.Entry()
        entry.value = strPiece16
        entry.context = context
        entry.index = len(self.mStrings)
        entry.ref = 0
        self.mStrings.append(entry)
        self.mIndexedStrings.append(ehash)
        ref = StringPool.Ref(entry)
        if spans is None: return ref
        styleEntry = StringPool.StyleEntry()
        styleEntry.str = ref
        for span in spans:
            to_add = StringPool.Span(self.makeRef(span.name), span.firstChar, span.lastChar)
            styleEntry.spans.append(to_add)
        styleEntry.ref = 0
        self.mStyles.append(styleEntry)
        return StringPool.StyleRef(styleEntry)

    def hintWillAdd(self, stringCount, styleCount):
        self.mStrings.extend(stringCount*[None])
        self.mStyles.extend(styleCount*[None])

    def prune(self):
        self.mStyles = filter(lambda x: x.ref > 0, self.mStyles)

        toDelete = [k for k, entry in enumerate(self.mStrings) if entry.ref <= 0][::-1]
        [(self.mStrings.pop(k), self.mIndexedStrings.pop(k)) for k in toDelete]
        map(lambda x: setattr(self.mStrings[x], 'index', x), range(self.size()))

    def sort(self, cmpFunc):
        self.mStrings.sort(cmp=cmpFunc)
        self.mIndexedStrings = [self.mIndexedStrings[entry.index] for entry in self.mStrings]
        map(lambda x: setattr(self.mStrings[x], 'index', x), range(self.size()))

        self.mStyles.sort(cmp=lambda x, y: cmp(x.getIndex(), y.getIndex()))

    def size(self):
        return len(self.mStrings)

    def merge(self, stringPool):
        self.mIndexedStrings.extend(stringPool.mIndexedStrings)
        stringPool.mIndexedStrings = []
        self.mStrings.extend(stringPool.mStrings)
        stringPool.mStrings = []
        self.mStyles.extend(stringPool.mStyles)
        stringPool.mStyles = []
        map(lambda x: setattr(self.mStrings[x], 'index', x), range(self.mStrings))

    def makeRef(self, arg1, context=None):
        if isinstance(arg1, basestring):
            strPiece16,context, unique, spans = arg1, context, True, None

        if isinstance(arg1, StyleString):
            strPiece16,context, unique, spans = arg1.str, context, False, arg1.spans

        if isinstance(arg1, StringPool.StyleRef):
            strPiece16 = pointee(arg1._mEntry.str)
            context = arg1._mEntry.str._mEntry.context
            unique = False
            spans = [StringPool.Span(pointee(x.name), x.firstChar, x.lastChar) for x in arg1._mEntry.spans]
        return self._makeRefImpl(strPiece16, context, unique, spans)

    def _flatten(stringPool, bigBufferOut, utf8):
        # def writeCType(ctype, offset=-1):
        #     actual = bigBufferOut.tell()
        #     if offset != -1:
        #         bigBufferOut.seek(offset)
        #     bigBufferOut.write(ctype)
        #     if offset != -1:
        #         bigBufferOut.seek(actual)

        def encodeLength(data, cType, length):
            kMask = 1 << ((ctypes.sizeof(cType) * 8) - 1)
            kMaxSize = kMask - 1
            if length > kMaxSize:
                lenc = kMask | (kMaxSize & (length >> (ctypes.sizeof(cType) * 8)))
                # data.write(cType(lenc))
                dmy = data.nextBlock(cType)
                dmy.value = lenc
            dmy = data.nextBlock(cType)
            dmy.value = length

        # startIndex = bigBufferOut.tell()
        startIndex = bigBufferOut.size()
        # header = rt.ResStringPool_header()
        # bigBufferOut.write(header)
        header = bigBufferOut.nextBlock(rt.ResStringPool_header)
        header.header.type = rt.ResChunk_header.RES_STRING_POOL_TYPE
        header.header.headerSize = ctypes.sizeof(header)
        header.stringCount = stringPool.size()
        if utf8:
            header.flags |= rt.ResStringPool_header.UTF8_FLAG
        if header.stringCount:
            # indices = (header.stringCount * ctypes.c_uint32)()
            # bigBufferOut.write(indices)
            indices = bigBufferOut.nextBlock(ctypes.c_uint32, header.stringCount)
        if stringPool.mStyles:
            header.styleCount = stringPool.mStyles[-1].str.getIndex() + 1
            # styleIndices = (header.styleCount * ctypes.c_uint32)()
            # bigBufferOut.write(styleIndices)
            styleIndices = bigBufferOut.nextBlock(ctypes.c_uint32, header.styleCount)

        # beforeStringsIndex = bigBufferOut.tell()
        beforeStringsIndex = bigBufferOut.size()
        header.stringsStart = beforeStringsIndex - startIndex
        if header.stringCount:
            for k, entry in enumerate(stringPool):
                # indices[k] = bigBufferOut.tell() - beforeStringsIndex
                indices[k] = bigBufferOut.size() - beforeStringsIndex
                enc = entry.value
                lenc = len(enc)
                if utf8:
                    enc8 = enc.encode('utf-8')
                    lenc8 = len(enc8)
                    encodeLength(bigBufferOut, ctypes.c_uint8, lenc)
                    encodeLength(bigBufferOut, ctypes.c_uint8, lenc8)
                    enc = enc8 + u'\0'.encode('utf-8')
                else:
                    enc16 = entry.value.encode('utf-16')
                    lenc16 = len(enc16)
                    enc = enc16 + u'\0'.encode('utf-16')
                    encodeLength(bigBufferOut, ctypes.c_uint16, lenc16)
                # bigBufferOut.write(enc)
                dmy = bigBufferOut.nextBlock(ctypes.c_char, len(enc))
                dmy[:] = enc
        bigBufferOut.align4()
            # writeCType(indices, offset=startIndex + header.header.headerSize)
        if header.styleCount:
            # beforeStylesIndex = bigBufferOut.tell()
            beforeStylesIndex = bigBufferOut.size()
            header.stylesStart = beforeStylesIndex - startIndex
            # END = ctypes.c_uint32(rt.ResStringPool_span.END)
            currentIndex = 0
            for entry in stringPool.mStyles:
                while entry.str.getIndex() > currentIndex:
                    # styleIndices[currentIndex] = bigBufferOut.tell() - beforeStylesIndex
                    styleIndices[currentIndex] = bigBufferOut.size() - beforeStylesIndex
                    currentIndex += 1
                    # bigBufferOut.write(END)
                    spanOffset = bigBufferOut.nextBlock(ctypes.c_uint32)
                    # spanOffset.value = END
                    spanOffset.value = rt.ResStringPool_span.END
                styleIndices[currentIndex] = bigBufferOut.size() - beforeStylesIndex
                # styleIndices[currentIndex] = bigBufferOut.tell() - beforeStylesIndex
                currentIndex += 1
                # span = (len(entry.spans)*rt.ResStringPool_span)()
                span = bigBufferOut.nextBlock(rt.ResStringPool_span, len(entry.spans))
                for k, s in enumerate(entry.spans):
                    span[k].name.index = s.name.getIndex()
                    span[k].firstChar = s.firstChar
                    span[k].lastChar = s.lastChar
                # bigBufferOut.write(span)
                # bigBufferOut.write(END)
                spanEnd = bigBufferOut.nextBlock(ctypes.c_uint32)
                spanEnd.value = rt.ResStringPool_span.END
            # writeCType(styleIndices, offset=startIndex + header.header.headerSize + 4*header.stringCount)
            paddingLength = ctypes.sizeof(rt.ResStringPool_span)
            paddingLength -= rt.ResStringPool_span.name.size
            # bigBufferOut.write((paddingLength*ctypes.c_uint8)(*(paddingLength*(0xff,))))
            padding = bigBufferOut.nextBlock(ctypes.c_uint8, paddingLength)
            padding[:] = paddingLength * [0xff]
            bigBufferOut.align4()
        header.header.size = bigBufferOut.size() - startIndex
        # writeCType(header, offset=startIndex)
        return True

    def flattenUtf8(stringPool, bigBufferOut):
        return stringPool._flatten(bigBufferOut, True)

    def flattenUtf16(stringPool, bigBufferOut):
        return stringPool._flatten(bigBufferOut, stringPool, False)

    def __iter__(self):
        self._indx = -1
        return self

    def next(self):
        self._indx += 1
        try:
            return self.mStrings[self._indx]
        except IndexError:
            del self._indx
            raise StopIteration

    def packForFlatten(self):
        order = [x.str.getIndex() for x in self.mStyles]

        def orderForFlatten(x):
            return 3 if x.ref <= 0 else (2 if x.index not in order else 1)

        cmpFunc = lambda x, y: cmp(orderForFlatten(x), orderForFlatten(y))
        self.sort(cmpFunc)
        self.prune()



