# -*- coding: utf-8 -*-
from Tools.aapt import ResourcesTypes
from Tools.aapt.Resources import ResourceNameRef, ResourceId
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

class Reference(BaseItem):

    class Type(object):
        def __init__(self, value):
            super(Reference.Type, self).__init__()
            self.value = value
    map(lambda x: setattr(Reference.Type, 'k' + x[1].title(), x[0]), enumerate(('resource', 'attribute')))

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
        super(Reference, self).toString()
        outStr = '(reference) '
        if self.referenceType == Reference.Type.kResource:
            outStr += '@'
        else:
            outStr += '?'
        if self.name:
            outStr += self.name.value()
        if self.id and not Res_INTERNALID(self.id.value().id):
            outStr += ' ' + self.id.value()

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
        return '(raw string) ' + self.value


class String(BaseItem):

    def __init__(self, stringPool_ref):
        super(String, self).__init__()
        self.value = stringPool_ref

    def flatten(self, res_Value):
        super(String, self).flatten(res_Value)

