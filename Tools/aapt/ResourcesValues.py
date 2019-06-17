# -*- coding: utf-8 -*-
#
# Ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceValues.h
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceValues.cpp
#
import operator as op

from Tools.aapt import ResourcesTypes
from Tools.aapt.Resource import ResourceNameRef, ResourceId
from Tools.aapt.ResourcesTypes import Res_INTERNALID

TYPE_RAW_STRING = 0xfe      # ubicado en flatten/ResourceTypeExtensions

class Value(object):
    def __init__(self):
        super(Value, self).__init__()

    def isItem(self):
        return False

    def isWeak(self):
        return False

    def accept(self, rawValueVisitor):
        pass

    def clone(self, stringPool):
        pass

    def toString(self):
        pass


class BaseValue(Value):
    def accept(self, rawValueVisitor):
        rawValueVisitor.visit(self)

class Item(Value):
    def isItem(self):
        return True

    def clone(self, stringPool):
        super(Item, self).clone(stringPool)
        pass

    def flatten(self, res_Value):
        pass


class BaseItem(Item):
    def accept(self, rawValueVisitor):
        rawValueVisitor.visit(self)
        pass

def createEnum(name, *args, **kwargs):
    def __init__(self, value):
        object.__init__()
        self.value = value
    classe = type(name, (object,), {'__init__': __init__})
    if kwargs:
        map(lambda x: setattr(classe, x[0], x[1]), kwargs.items())
    elif args:
        map(lambda x: setattr(classe, x[1], x[0]), enumerate(args))
    return classe


class Reference(BaseItem):

    Type = createEnum('Type', 'kResource', 'kAttribute')

    def __init__(self, arg1=None, aType=None):
        super(Reference, self).__init__()
        self.name = None
        self.id = None
        self.referenceType = aType or Reference.Type.kResource
        self.privateReference = False
        if isinstance(arg1, ResourceNameRef):
            self.name = arg1.toResourceName()
        if isinstance(arg1, ResourceId):
           self.id = arg1

    def flatten(self, res_Value):
        super(Reference, self).flatten(res_Value)
        res_Value.dataType = ResourcesTypes.Res_value.TYPE_REFERENCE \
            if self.referenceType == Reference.Type.kResource else \
            ResourcesTypes.Res_value.TYPE_ATTRIBUTE
        res_Value.data = self.id.id if self.id else 0
        return True

    def clone(self, stringPool):
        super(Reference, self).clone(stringPool)
        ref = Reference()
        ref.referenceType = self.referenceType
        ref.name = self.name
        ref.id = self.id
        return ref

    def toString(self):
        tostring = '(reference) '
        tostring += '@?'[self.referenceType]
        if self.name:
            tostring += self.name.toString()
        if self.id and not Res_INTERNALID(self.id.id):
            tostring += ' %s' % self.id.toString()
        return tostring

class Id(BaseItem):

    def isWeak(self):
        return True

    def flatten(self, res_Value):
        super(Id, self).flatten(res_Value)
        res_Value.dataType = ResourcesTypes.Res_value.TYPE_INT_BOOLEAN
        res_Value.data = 0
        return True

    def clone(self, stringPool):
        super(Id, self).clone(stringPool)
        return Id()

    def toString(self):
        super(Id, self).toString()
        return '(id)    '

class RawString(BaseItem):

    def __init__(self, stringPool_ref):
        super(RawString, self).__init__()
        self.value = stringPool_ref

    def flatten(self, res_Value):
        super(RawString, self).flatten(res_Value)
        res_Value.dataType = TYPE_RAW_STRING
        res_Value.data = self.value.getIndex()
        return True

    def clone(self, stringPool):
        super(RawString, self).clone(stringPool)
        return RawString(stringPool.makeRef(self.value))

    def toString(self):
        return '(raw string) %s' % self.value


class String(BaseItem):

    def __init__(self, stringPool_ref):
        super(String, self).__init__()
        self.value = stringPool_ref

    def __pointee__(self):
        return self.value.__pointee__()

    def flatten(self, res_Value):
        if self.value.getIndex() > 0xFFFFFFFF:
            return False
        res_Value.dataType = ResourcesTypes.Res_value.TYPE_STRING
        res_Value.data = self.value.getIndex()
        return True

    def clone(self, newStringPool):
        return String(newStringPool.makeRef(self.value))

    def toString(self):
        return '(string) "%s"' % self.value.__pointee__()


class StyledString(BaseItem):
    def __init__(self, stringPool_styleref):
        super(StyledString, self).__init__()
        self.value = stringPool_styleref

    def __pointee__(self):
        return self.value.__pointee__()

    def flatten(self, res_Value):
        if self.value.getIndex() > 0xFFFFFFFF:
            return False
        res_Value.dataType = ResourcesTypes.Res_value.TYPE_STRING
        res_Value.data = self.value.getIndex()
        return True

    def clone(self, newStringPool):
        return StyledString(newStringPool.makeRef(self.value))

    def toString(self):
        return '(string) "%s"' % self.value.str.__pointee__()


class FileReference(BaseItem):
    def __init__(self, path=None):
        super(FileReference, self).__init__()
        self.path = path

    def flatten(self, res_Value):
        if self.path.getIndex() > 0xFFFFFFFF:
            return False
        res_Value.dataType = ResourcesTypes.Res_value.TYPE_STRING
        res_Value.data = self.path.getIndex()
        return True

    def clone(self, newStringPool):
        return FileReference(newStringPool.makeRef(self.path.str.__pointee__()))

    def toString(self):
        return "(file) " + self.path.str.__pointee__()


class BinaryPrimitive(BaseItem):
    def __init__(self, arg1=None, data=None):
        super(BinaryPrimitive, self).__init__()
        self.value = None
        if isinstance(arg1, ResourcesTypes.Res_value):
            self.value = arg1
        elif data:
            self.value = value = ResourcesTypes.Res_value()
            value.dataType = arg1
            value.data = data

    def flatten(self, res_Value):
        res_Value.dataType = self.value.dataType
        res_Value.data = self.value.data
        return True

    def clone(self, newStringPool):
        return BinaryPrimitive(self.value)

    def toString(self):
        case = self.value.dataType
        if case == ResourcesTypes.Res_value.TYPE_NULL:
            return '(null)'
        elif case == ResourcesTypes.Res_value.TYPE_INT_DEC:
            return '(integer) %s' % self.value.data
        elif case == ResourcesTypes.Res_value.TYPE_INT_HEX:
            return '(integer) {:0>8x}'.format(self.value.data)
        elif case == ResourcesTypes.Res_value.TYPE_INT_BOOLEAN:
            return '(boolean) %s' % ('true' if self.value.data else 'false')
        elif ResourcesTypes.Res_value.TYPE_FIRST_COLOR_INT <= case <= ResourcesTypes.Res_value.TYPE_LAST_COLOR_INT:
            return '(color) #{:0>8x}'.format(self.value.data)
        else:
            return '(unknown 0x{:0>8x}) 10x{:0>8x}'.format(self.value.dataType, self.value.data)

    def __getattr__(self, item):
        return getattr(self.value, item)

class Attribute(BaseValue):

    class Symbol(object):
        def __init__(self, symbol=None, value=None):
            super(Attribute.Symbol, self).__init__()
            self.symbol = symbol
            self.value = value

        def toString(self):
            tostring = self.symbol.name.entry if self.symbol.name else '???'
            tostring += ' = %s' % self.value
            return tostring

    MASKS = sorted(
        [(key[5:].lower(), value) \
         for key, value in vars(ResourcesTypes.ResTable_map).items() \
         if key.startswith('TYPE_')],
        key=lambda x: x[1]
    )

    def __init__(self, weak, typeMask=0):
        super(Attribute, self).__init__()
        self.weak = weak
        self.typeMask = typeMask
        self.minInt = None
        self.maxInt = None
        self.symbols = []

    def isWeak(self):
        return self.weak

    def clone(self, newPoolString):
        attr = Attribute(self.weak)
        attr.typeMask = self.typeMask
        attr.symbols.extend(self.symbols[:])
        return attr

    def toStringMask(self):
        case = self.typeMask
        if case == ResourcesTypes.ResTable_map.TYPE_ANY:
            return 'any'
        return '|'.join([x[0] for x in self.MASKS if x[1] & case == x[1]])

    def toString(self):
        tostring = '(attr) '
        tostring += self.toStringMask()
        if self.symbols:
            tostring += ' [' + ', '.join(self.symbols) + ']'
        if self.weak:
            tostring += '[weak]'
        return tostring


class Style(BaseValue):
    class Entry(object):
        def __init__(self, key=None, value=None):
            super(Style.Entry, self).__init__()
            self.key = key
            self.value = value

        def __str__(self):
            tostring = self.key.name if self.key.name else '???'
            tostring += ' = '
            tostring += self.value.toString()
            return tostring

    def __init__(self):
        super(Style, self).__init__()
        self.parent = None
        self.parentInferred = False
        self.entries = []

    def clone(self, newStringPool):
        style = Style()
        style.parent = self.parent
        style.parentInferred = self.parentInferred
        style.entries = map(lambda x: x.value.clone(newStringPool), self.entries)
        return style

    def toString(self):
        tostring = '(style) '
        if self.parent and self.parent.value().name:
            tostring += self.parent.value().name
        if self.entries:
            tostring += ' [' + ', '.join([str(entry) for entry in self.entries]) + ']'
        return tostring


class Array(BaseValue):

    def __init__(self):
        super(Array, self).__init__()
        self.items = []

    def clone(self, newStringPool):
        array = Array()
        array.items = map(op.methodcaller('clone', newStringPool), self.items)
        return array

    def toString(self):
        return '(array) [' + ', '.join(self.items) + ']'

class Plural(BaseValue):

    Zero = 1
    One = 1
    Dos = 2
    Few = 3
    Many = 4
    Other = 5
    Count = 6

    def __init__(self):
        super(Plural, self).__init__()
        self.count = 0
        self.values = {}

    def clone(self, newStringPool):
        p = Plural()
        p.count = len(self.values)
        p.values = map(lambda x: x.clone(newStringPool), self.values)
        return p

    def toString(self):
        return '(plural)'


class Styleable(BaseValue):

    def __init__(self):
        super(Styleable, self).__init__()
        self.entries = []

    def clone(self, newStringPool):
        styleable = Styleable()
        styleable.entries = self.entries[:]

    def toString(self):
        tostring = '(styleable) ['
        tostring += ', '.join(self.entries)
        tostring = ']'
        return tostring