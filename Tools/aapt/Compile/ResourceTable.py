# -*- coding: utf-8 -*-

from collections import namedtuple
import itertools


Public = namedtuple('Public', 'isPublic source comment')
ResourceConfigValue = namedtuple(('ResourceConfigValue', 'config source comment value'))
ResourceEntry = namedtuple('ResourceEntry', 'name id publicStatus values')


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
        pass

    def addResource(self, resourceName, configDescription, source, value, resourceId=None):
        pass

    def addFileReference(self, resourceName, configDescription, source, path):
        pass

    def addResourceAllowMangled(self, resourceName, configDescription, source, value):
        pass

    def markPublic(self, resourceName, resourceId, source):
        pass

    def markPublicAllowMangled(self, resourceName, resourceId, source):
        pass

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

    def _addResourceImpl(self, resourceName, resourceId, configDescription, source, value, validChars):
        pass

    def _markPublicImpl(self, resourceName, resourceId, source, validChars):
        pass