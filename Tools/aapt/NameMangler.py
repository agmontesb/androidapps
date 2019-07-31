# -*- coding: utf-8 -*-
from Tools.aapt.Resource import ResourceName


class NameManglerPolicy(object):

    def __init__(self, packageName, packagesToMangle=None):
        super(NameManglerPolicy, self).__init__()

        #
        # Represents the package we are trying to build. References pointing
        # to this package are not mangled, and mangled references inherit this package name.
        #
        self.targetPackageName = packageName
        #
        # We must know which references to mangle, and which to keep (android vs. com.android.support).
        #
        self.packagesToMangle = packagesToMangle or set()


class NameMangler(object):

    def __init__(self, policy):
        super(NameMangler, self).__init__()
        self.mPolicy = policy

    def mangleName(self, name):
        if self.mPolicy.targetPackageName == name.package or \
                name.package not in self.mPolicy.packagesToMangle:
            return None
        return ResourceName(
            self.mPolicy.targetPackageName,
            name.type,
            self.mangleEntry(name.package, name.entry)
        )

    def shouldMangle(self, package):
        if not package or self.mPolicy.targetPackageName == package:
            return False
        return package in self.mPolicy.packagesToMangle

    # /**
    #  * Returns a mangled name that is a combination of `name` and `package`.
    #  * The mangled name should contain symbols that are illegal to define in XML,
    #  * so that there will never be name mangling collisions.
    #  */
    @staticmethod
    def mangleEntry(package, name):
        return package + "$" + name

    mangle = mangleEntry

    # /**
    #  * Unmangles the name in `outName`, storing the correct name back in `outName`
    #  * and the package in `outPackage`. Returns true if the name was unmangled or
    #  * false if the name was never mangled to begin with.
    #  */
    @staticmethod
    def unmangle(mangledName):
        try:
            return mangledName.split('$')
        except:
            pass

