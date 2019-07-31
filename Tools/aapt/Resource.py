# -*- coding: utf-8 -*-
from Tools.aapt.ConfigDescription import ConfigDescription


class ResourceType(object):
    types = (
        'anim',
        'animator',
        'array',
        'attr',
        'attrPrivate',
        'bool',
        'color',
        'dimen',
        'drawable',
        'fraction',
        'id',
        'integer',
        'integerarray',
        'interpolator',
        'layout',
        'menu',
        'mipmap',
        'plurals',
        'raw',
        'string',
        'style',
        'styleable',
        'transition',
        'xml',
    )

    def __init__(self, value):
        super(ResourceType, self).__init__()
        self.value = value

    @classmethod
    def toString(cls, resourceType):
        if 0 <= resourceType.value < len(cls.types):
            return cls.types[resourceType.value]

    @classmethod
    def parseResourceType(cls, aStr):
        if aStr in cls.types:
            return getattr(cls, 'k' + aStr.title())

    def __ne__(self, other):
        return self.value != other.value

    def __eq__(self, other):
        return self.value == other.value


map(lambda x: setattr(ResourceType, 'k' + x[1].title(), ResourceType(x[0])), enumerate(ResourceType.types))


class ResourceName(object):
    def __init__(self, strPackage=None, resType=None, strEntry=None):
        super(ResourceName, self).__init__()
        self.package = strPackage
        self.type = resType
        self.entry = strEntry

    def isValid(self):
        return not (self.package or self.entry)

    def toString(self):
        result = ''
        if self.package:
            result += self.package + ':'
        return result + ResourceType.toString(self.type) + '/' + self.entry

    def __lt__(self, other):
        return (self.package, self.type, self.entry) < (other.package, other.type, other.entry)

    def __eq__(self, other):
        return (self.package, self.type, self.entry) == (other.package, other.type, other.entry)

    def __ne__(self, other):
        return (self.package, self.type, self.entry) != (other.package, other.type, other.entry)


class ResourceNameRef(object):
    def __init__(self, frstArg=None, resType=None, strEntry=None):
        super(ResourceNameRef, self).__init__()
        self.type = resType
        self.entry = strEntry
        if frstArg is None or isinstance(frstArg, basestring):
            self.package = frstArg
        elif isinstance(frstArg, ResourceName):
            self.package = frstArg.package
            self.type = frstArg.type
            self.entry = frstArg.entry

    def toResourceName(self):
        return ResourceName(self.package or '', self.type, self.entry)

    def isValid(self):
        return not (self.package or self.entry)

    def __lt__(self, other):
        return (self.package, self.type, self.entry) < (other.package, other.type, other.entry)

    def __eq__(self, other):
        return (self.package, self.type, self.entry) == (other.package, other.type, other.entry)

    def __ne__(self, other):
        return (self.package, self.type, self.entry) != (other.package, other.type, other.entry)

    def toString(self):
        result = ''
        if self.package:
            result += self.package + ':'
        return result + ResourceType.toString(self.type) + '/' + self.entry

class ResourceId(object):

    def __init__(self, p=None, t=None, e=None):
        super(ResourceId, self).__init__()
        self.id = 0
        if p and isinstance(p, ResourceId):
            self.id = p.id
        elif p is not None and t is not None and e is not None:
            self.id = ((p<<24) | ((t&0xFF)<<16) | (e&0xFFFF))
        elif p and isinstance(p, int) and (0xff000000 & p):
            self.id = p

    def isValid(self):
        return (0xff000000 & self.id != 0) and (0x00ff0000 & self.id != 0)

    def packageId(self):
        return self.id >> 24

    def typeId(self):
        return (self.id>>16)&0xFF

    def entryId(self):
        return self.id&0xFFFF

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def toString(self):
        return '0x{:0>8x}'.format(self.id)


class SourcedResourceName(object):
    def __init__(self, resourceName=None, line=None):
        super(SourcedResourceName, self).__init__()
        self.name = resourceName
        self.line = line

    def __eq__(self, other):
        return self.name == other.name and self.line == other.line

class ResourceFile(object):
    def __init__(self, resourceName=None, configDescription=None, source=None, arrSourcedResourceName=None):
        super(ResourceFile, self).__init__()
        self.name = resourceName
        self.config = configDescription or ConfigDescription()
        self.source = source
        self.exportedSymbols = arrSourcedResourceName or []