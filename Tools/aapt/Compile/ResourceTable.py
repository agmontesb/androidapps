# -*- coding: utf-8 -*-
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceTable.cpp
#

from collections import namedtuple
import itertools

from Tools.aapt.Resource import ResourceId
from Tools.aapt.ResourcesValues import Attribute
from Tools.aapt.ResourcesTypes import ResTable_map

Public = namedtuple('Public', 'isPublic source comment')
ResourceConfigValue = namedtuple(('ResourceConfigValue', 'config source comment value'))
ResourceEntry = namedtuple('ResourceEntry', 'name id publicStatus values')
ResourceEntry.packageId = lambda self: ((self.id>>24)-1)
ResourceEntry.typeId = lambda self: (((self.id>>16)&0xFF)-1)
ResourceEntry.entryId = lambda self: (self.id&0xFFFF)


class ResourceTableType(object):
    def __init__(self, resType):
        super(ResourceTableType, self).__init__()
        self.resourceType = resType
        self.id = None
        self.publicStatus = None
        self.entries = None

    def findEntry(self, name):
        try:
            it = itertools.dropwhile(lambda x: x.name != name, self.entries)
            return it.next()
        except:
            pass

    def findOrCreateEntry(self, name):
        entry = self.findEntry(name)
        if entry is None:
            entry = ResourceEntry(name, None, None, None)
            self.entries.append(entry)
        return entry


class PackageType(object):
    System = 1
    Vendor = 2
    App = 3
    Dynamic = 4


class ResourceTablePackage(object):
    def __init__(self):
        super(ResourceTablePackage, self).__init__()
        self.type = None
        self.id = None
        self.name = None
        self.types = []

    def findType(self, resourceType):
        try:
            it = itertools.dropwhile(lambda x: x.type != resourceType, self.types)
            return it.next()
        except:
            pass

    def findOrCreateType(self, resourceType):
        atype = self.findType(resourceType)
        if atype is None:
            atype = ResourceTableType(resourceType)
            self.types.append(atype)
        return atype

class ResourceTable(object):

    def __init__(self, resourceTable=None):
        super(ResourceTable, self).__init__()
        self.stringPool = None
        self.packages = []
        pass

    def resolveValueCollision(self, existing, incomming):
        incommingAttr = isinstance(incomming, Attribute)
        existingAttr = isinstance(existing, Attribute)
        if not incommingAttr:
            if incomming.isWeak():
                return -1
            if existing.isWeak():
                return 1
            return 0
        if not existingAttr:
            if existing.isWeak():
                return 1
            return 0
        assert incommingAttr and existingAttr
        if existing.typeMask == incomming.typeMask:
            return 1 if existing.isWeak() else -1
        if incomming.isWeak() and incomming.typeMask == ResTable_map.TYPE_ANY:
            return -1
        return 0

    def addResource(self, resourceName, configDescription, source, value, resourceId=None):
        return self.addResourceImpl(resourceName, resourceId, configDescription, source, value, '.-_')

    def addFileReference(self, resourceName, configDescription, source, path):
        return self._addResourceImpl(resourceName, None, configDescription, source, self.stringPool.makeRef(path), '.-_')

    def addResourceAllowMangled(self, resourceName, configDescription, source, value):
        return self._addResourceImpl(resourceName, None, configDescription, source, value, "._-$")

    def _addResourceImpl(self, resourceName, resourceId, configDescription, source, value, validChars):
        w = range(len(resourceName.entry))
        it = itertools.dropwhile(lambda x, y=resourceName.entry: y[x].isalnum() or y[x] in validChars, w)
        try:
            wPos = it.next()
            errMessage = 'resource %s has invalid entry name "%s". Invalid character "%s"'
            raise Exception(errMessage % (resourceName, resourceName.entry, resourceName.entry[wPos]))
        except:
            pass
        package = self._findOrCreatePackage(resourceName.package)
        if resourceId.isValid() and package.id and package.id.value() != resourceId.packageId():
            errMessage = 'trying to add resource "%s" ' \
                         'with ID %s but package "%s" already has ID {:0>8x}'
            raise Exception(errMessage.format(resourceName, resourceId, package.name, package.id.value()))

        atype = package._findOrCreateType(resourceName.type)
        if resourceId.isValid() and atype.id and atype.id.value() != resourceId.typeId():
            errMessage = 'trying to add resource "%s" ' \
                         'with ID %s but type "%s" already has ID {:0>8x}'
            raise Exception(errMessage.format(resourceName, resourceId, atype.type, atype.id.value()))
        entry = atype._findOrCreateEntry(resourceName.entry)
        if resourceId.isValid() and entry.id and entry.id.value() != resourceId.entryId():
            errMessage = 'trying to add resource "%s" ' \
                         'with ID %s but resource already has ID {:0>8x}'
            raise Exception(errMessage.format(resourceName, resourceId, ResourceId(package.id.value(), atype.id.value(), entry.id.value())))

        it = itertools.dropwhile(lambda x: x[1].config < configDescription, enumerate(entry.values))
        try:
            pos, it_value = it.next()
            bFlag = it_value.config != configDescription
        except:
            pos = -1
            bFlag = True
        if bFlag:
            entry.values.insert(pos, configDescription) if pos > 0 else entry.values.append(configDescription)
        else:
            collisionResult = self.resolveValueCollision(it_value.value, value)
            if collisionResult > 0:
                entry.values[pos] = ResourceConfigValue(configDescription, source, '', value)
            elif collisionResult == 0:
                errMessage = 'duplicate value for resource "%s" with config "%s" resource previously defined here'
                raise Exception(errMessage % (resourceName, it_value.config))
        if resourceId.isValid():
            package.id = resourceId.packageId()
            atype.id = resourceId.typeId()
            entry.id = resourceId.entryId()

    SearchResult = namedtuple('SearchResult', 'package type entry')

    def findResource(self, resourceName):
        resTablePackage = self.findPackage(resourceName.package)
        if not resTablePackage:
            return self.SearchResult('', None, '')
        resTableType = resTablePackage.findType(resourceName.type)
        if not resTableType:
            return self.SearchResult('', None, '')
        resEntry = resTableType.findEntry(resourceName.entry)
        if not resEntry:
            return self.SearchResult('', None, '')
        return self.SearchResult(resTablePackage, resTableType, resEntry)

    def findPackage(self, name):
        try:
            it = itertools.dropwhile(lambda x: x.name != name, self.packages)
            return it.next()
        except:
            pass

    def findPackageById(self, id):
        try:
            it = itertools.dropwhile(lambda x: x.id != id, self.packages)
            return it.next()
        except:
            pass

    def createPackage(self, name, id):
        package = self._findOrCreatePackage(name)
        if package.id is None or package.id == id:
            package.id = id
            return package

    def _findOrCreatePackage(self, name):
        package = self.findPackage(name)
        if not package:
            package = ResourceTablePackage()
            package.name = name
            self.packages.append(package)
        return package

    def markPublic(self, resourceName, resourceId, source):
        return self._markPublicImpl(resourceName, resourceId, source, '._-')

    def markPublicAllowMangled(self, resourceName, resourceId, source):
        return self._markPublicImpl(resourceName, resourceId, source, '._-$')

    def _markPublicImpl(self, resourceName, resourceId, source, validChars):
        w = range(len(resourceName.entry))
        it = itertools.dropwhile(lambda x, y=resourceName.entry: y[x].isalnum() or y[x] in validChars, w)
        try:
            wPos = it.next()
            errMessage = 'resource %s has invalid entry name "%s". Invalid character "%s"'
            raise Exception(errMessage % (resourceName, resourceName.entry, resourceName.entry[wPos]))
        except:
            pass
        package = self._findOrCreatePackage(resourceName.package)
        if resourceId.isValid() and package.id and package.id.value() != resourceId.packageId():
            errMessage = 'trying to add resource "%s" ' \
                         'with ID %s but package "%s" already has ID {:0>8x}'
            raise Exception(errMessage.format(resourceName, resourceId, package.name, package.id.value()))

        atype = package._findOrCreateType(resourceName.type)
        if resourceId.isValid() and atype.id and atype.id.value() != resourceId.typeId():
            errMessage = 'trying to add resource "%s" ' \
                         'with ID %s but type "%s" already has ID {:0>8x}'
            raise Exception(errMessage.format(resourceName, resourceId, atype.type, atype.id.value()))
        entry = atype._findOrCreateEntry(resourceName.entry)
        if resourceId.isValid() and entry.id and entry.id.value() != resourceId.entryId():
            errMessage = 'trying to add resource "%s" ' \
                         'with ID %s but resource already has ID {:0>8x}'
            raise Exception(errMessage.format(resourceName, resourceId,
                                              ResourceId(package.id.value(), atype.id.value(), entry.id.value())))
        atype.publicStatus.isPublic = True
        entry.publicStatus.isPublic = True
        entry.publicStatus.source = source

        if resourceId.isValid():
            package.id = resourceId.packageId()
            atype.id = resourceId.typeId()
            entry.id = resourceId.entryId()


