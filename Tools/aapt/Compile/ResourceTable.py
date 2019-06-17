# -*- coding: utf-8 -*-
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceTable.cpp
#

from collections import namedtuple
import itertools

from Tools.aapt.ConfigDescription import ConfigDescription
from Tools.aapt.Resource import ResourceId
from Tools.aapt.ResourcesValues import Attribute
from Tools.aapt.ResourcesTypes import ResTable_map
from Tools.aapt.StringPool import StringPool

Public = namedtuple('Public', 'isPublic source comment')
ResourceConfigValue = namedtuple('ResourceConfigValue', 'config source comment value')
ResourceConfigValue.__getattr__ = lambda x, item: getattr(x[3],item)
ResourceEntry = namedtuple('ResourceEntry', 'name id publicStatus values')
ResourceEntry.packageId = lambda self: ((self.id>>24)-1)
ResourceEntry.typeId = lambda self: (((self.id>>16)&0xFF)-1)
ResourceEntry.entryId = lambda self: (self.id&0xFFFF)


class ResourceTableType(object):
    def __init__(self, resType):
        super(ResourceTableType, self).__init__()
        self.type = resType
        self.id = None
        self.publicStatus = Public(False, '', '')
        self.entries = []

    def findEntry(self, name):
        try:
            it = itertools.dropwhile(lambda x: x.name != name, self.entries)
            return it.next()
        except:
            pass

    def findOrCreateEntry(self, name):
        entry = self.findEntry(name)
        if entry is None:
            entry = ResourceEntry(name, None, Public(False, '', ''), [])
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
        self.type = PackageType.App
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
        self.stringPool = StringPool()
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
        if existing.isWeak() and existing.typeMask == ResTable_map.TYPE_ANY:
            return 1
        if incomming.isWeak() and incomming.typeMask == ResTable_map.TYPE_ANY:
            return -1
        return 0

    def addResource(self, resourceName, configDescription, source, value, resourceId=None, diag=None):
        resourceId = resourceId or ResourceId()
        return self._addResourceImpl(resourceName, resourceId, configDescription, source, value, '.-_', diag)

    def addFileReference(self, resourceName, configDescription, source, path, diag):
        return self._addResourceImpl(resourceName, None, configDescription, source,
                                     self.stringPool.makeRef(path), '.-_', diag)

    def addResourceAllowMangled(self, resourceName, configDescription, source, value, diag):
        return self._addResourceImpl(resourceName, None, configDescription, source, value, "._-$", diag)

    def _addResourceImpl(self, resourceName, resourceId, configDescription, source, value, validChars, diag):
        configDescription = configDescription or ConfigDescription()
        it = itertools.dropwhile(lambda x: x.isalnum() or x in validChars, resourceName.entry)
        try:
            aChar = it.next()
            errMessage = source + ' resource "%s" has invalid entry name "%s". Invalid character "%s"'
            diag.error = errMessage % (resourceName.toString(), resourceName.entry, aChar)
            return False
        except:
            pass
        package = self.findOrCreatePackage(resourceName.package)
        if resourceId.isValid() and package.id and package.id != resourceId.packageId():
            errMessage = source + ' trying to add resource "%s" ' \
                         'with ID %s but package "%s" already has ID {:0>8x}'
            diag.error = errMessage.format(resourceName, resourceId, package.name, package.id)
            return False
        atype = package.findOrCreateType(resourceName.type)
        if resourceId.isValid() and atype.id and atype.id != resourceId.typeId():
            errMessage = source + ' trying to add resource "%s" ' \
                         'with ID %s but type "%s" already has ID {:0>8x}'
            diag.error = errMessage.format(resourceName, resourceId, atype.type, atype.id)
            return False
        entry = atype.findOrCreateEntry(resourceName.entry)
        if resourceId.isValid() and entry.id and entry.id != resourceId.entryId():
            errMessage = source + ' trying to add resource "%s" ' \
                         'with ID %s but resource already has ID {:0>8x}'
            diag.error = errMessage.format(resourceName, resourceId, ResourceId(package.id, atype.id, entry.id))
            return False
        it = itertools.dropwhile(lambda x: x[1].config < configDescription, enumerate(entry.values))
        try:
            pos, it_value = it.next()
            bFlag = it_value.config != configDescription
        except:
            pos = -1
            bFlag = True
        if bFlag:
            rcv = ResourceConfigValue(configDescription, source, '', value)
            entry.values.insert(pos, rcv) if pos > 0 else entry.values.append(rcv)
        else:
            collisionResult = self.resolveValueCollision(it_value.value, value)
            if collisionResult > 0:
                entry.values[pos] = ResourceConfigValue(configDescription, source, '', value)
            elif collisionResult == 0:
                errMessage = source + ' duplicate value for resource "%s" with config "%s" resource previously defined here'
                diag.error = errMessage % (resourceName, it_value.config)
                return False
        if resourceId.isValid():
            package.id = resourceId.packageId()
            atype.id = resourceId.typeId()
            ndx = atype.entries.index(entry)
            atype.entries[ndx] = entry._replace(id=resourceId.entryId())
        return True

    SearchResult = namedtuple('SearchResult', 'package type entry')
    SearchResult.__nonzero__ = lambda x, y=SearchResult('', None, ''): x != y

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

    def _getValueForConfig(self, entry, config):
        config = config or ConfigDescription()
        pos = -1
        if entry:
            it = itertools.dropwhile(lambda x: x[1].config < config, enumerate(entry.values))
            try:
                pos, it_value = it.next()
                bFlag = it_value.config == config
            except:
                bFlag = False
            pos = pos if bFlag else -1
        return pos

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
        package = self.findOrCreatePackage(name)
        if package.id is None or package.id == id:
            package.id = id
            return package

    def findOrCreatePackage(self, name):
        package = self.findPackage(name)
        if not package:
            package = ResourceTablePackage()
            package.name = name or ''
            self.packages.append(package)
        return package

    def markPublic(self, resourceName, resourceId, source, diag):
        return self._markPublicImpl(resourceName, resourceId, source, '._-', diag)

    def markPublicAllowMangled(self, resourceName, resourceId, source, diag):
        return self._markPublicImpl(resourceName, resourceId, source, '._-$', diag)

    def _markPublicImpl(self, resourceName, resourceId, source, validChars, diag):
        it = itertools.dropwhile(lambda x: x.isalnum() or x in validChars, resourceName.entry)
        try:
            wPos = it.next()
            errMessage = source + ' resource %s has invalid entry name "%s". Invalid character "%s"'
            diag.error = errMessage % (resourceName, resourceName.entry, wPos)
            return False
        except:
            pass
        package = self.findOrCreatePackage(resourceName.package)
        if resourceId.isValid() and package.id and package.id != resourceId.packageId():
            errMessage = source + ' trying to add resource "%s" ' \
                         'with ID %s but package "%s" already has ID {:0>8x}'
            diag.error = errMessage.format(resourceName, resourceId, package.name, package.id)
            return False

        atype = package.findOrCreateType(resourceName.type)
        if resourceId.isValid() and atype.id and atype.id != resourceId.typeId():
            errMessage = source + ' trying to add resource "%s" ' \
                         'with ID %s but type "%s" already has ID {:0>8x}'
            diag.error = errMessage.format(resourceName, resourceId, atype.type, atype.id)
            return False
        entry = atype.findOrCreateEntry(resourceName.entry)
        if resourceId.isValid() and entry.id and entry.id != resourceId.entryId():
            errMessage = source + ' trying to add resource "%s" ' \
                         'with ID %s but resource already has ID {:0>8x}'
            diag.error = errMessage.format(resourceName, resourceId,
                                           ResourceId(package.id, atype.id, entry.id))
            return False
        atype.publicStatus = atype.publicStatus._replace(isPublic=True)
        ps = entry.publicStatus._replace(isPublic=True, source=source)
        entry = entry._replace(publicStatus=ps)

        if resourceId.isValid():
            package.id = resourceId.packageId()
            atype.id = resourceId.typeId()
            entry.id = resourceId.entryId()
        return True

