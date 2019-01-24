# -*- coding: utf-8 -*-
import os
import copy

import Android
from Android.content.pm.PackageManager import PackageManager
from Android.interface.IContext import IContext
from Android.reference.File import File


class Context(IContext):

    def __init__(self):
        super(Context, self).__init__()
        self.mMainThread = None
        self.mActivityToken = None
        self.mFlags = None
        self.mUser = None
        self.mPackageInfo = None
        self.mResourcesManager = None
        self.mResources = None
        self.mDisplay = None
        self.mBasePackageName = None
        self.mOpPackageName = None
        self.mContentResolver = None
        pass

    def createConfigurationContext(self, overrideConfiguration):
        super(Context, self).createConfigurationContext(overrideConfiguration)

    def createContextForSplit(self, splitName):
        super(Context, self).createContextForSplit(splitName)

    def createDeviceProtectedStorageContext(self):
        super(Context, self).createDeviceProtectedStorageContext()

    def createDisplayContext(self, display):
        super(Context, self).createDisplayContext(display)

    def createPackageContext(self, packageName, flags):
        super(Context, self).createPackageContext(packageName, flags)
        pm = PackageManager()
        pmFlags = pm.GET_META_DATA | pm.GET_SHARED_LIBRARY_FILES
        pi = pm.getPackageInfo(packageName, pmFlags)
        context = copy.deepcopy(self)
        context.mPackageInfo = pi
        return context

    def databaseList(self):
        super(Context, self).databaseList()

    def deleteDatabase(self, name):
        super(Context, self).deleteDatabase(name)

    def deleteFile(self, name):
        super(Context, self).deleteFile(name)

    def deleteSharedPreferences(self, name):
        super(Context, self).deleteSharedPreferences(name)

    def fileList(self):
        super(Context, self).fileList()

    def getApplicationInfo(self):
        super(Context, self).getApplicationInfo()
        if not self.mPackageInfo:
            raise Exception('RuntimeException: "Not supported in system context"')
        return self.mPackageInfo.applicationInfo

    def getCacheDir(self):
        super(Context, self).getCacheDir()
        return self._createPrivateDir("cache")

    def getCodeCacheDir(self):
        super(Context, self).getCodeCacheDir()
        return self._createPrivateDir("code_cache")

    def getDataDir(self):
        super(Context, self).getDataDir()
        if not self.mPackageInfo:
            raise Exception('RuntimeException: "No package details found for package "' + self.getPackageName())
        res = None
        if self.isDeviceProtectedStorage():
            res = None
        else:
            ai = self.getApplicationInfo()
            res = File(ai.dataDir)
        if res:
            return res
        raise Exception(
            'RuntimeException: "No data directory found for package %s"' % self.getPackageName()
        )

    def getDatabasePath(self, name):
        super(Context, self).getDatabasePath(name)
        f = File(name)
        if f.isAbsolute():
            parent = f.getParentFile()
            if not parent.isDirectory(): parent.mkdir()
        else:
            dir = self._createPrivateDir('databases')
            if File.separatorChar in name:
                raise Exception('IllegalArgumentException: File %s contains a path separator' % name)
            f = File(dir, name)
        return f

    def getDir(self, name, mode):
        super(Context, self).getDir(name, mode)
        if File.separatorChar in name:
            raise Exception('IllegalArgumentException: File %s contains a path separator' % name)
        name = "app_" + name
        file = File(self.getDataDir(), name)
        if not file.exists():
            file.mkdir()

    def getExternalCacheDir(self):
        super(Context, self).getExternalCacheDir()

    def getExternalCacheDirs(self):
        super(Context, self).getExternalCacheDirs()

    def getExternalFilesDir(self, type):
        super(Context, self).getExternalFilesDir(type)

    def getExternalFilesDirs(self, type):
        super(Context, self).getExternalFilesDirs(type)

    def getExternalMediaDirs(self):
        super(Context, self).getExternalMediaDirs()

    def getFileStreamPath(self, name):
        super(Context, self).getFileStreamPath(name)

    def getFilesDir(self):
        super(Context, self).getFilesDir()
        return self._createPrivateDir("files")

    def getNoBackupFilesDir(self):
        super(Context, self).getNoBackupFilesDir()
        return self._createPrivateDir("no_backup")

    def getObbDir(self):
        super(Context, self).getObbDir()

    def getObbDirs(self):
        super(Context, self).getObbDirs()

    def getPackageName(self):
        super(Context, self).getPackageName()
        if self.mPackageInfo:
            return self.mPackageInfo.packageName
        return 'android'

    def getPackageResourcePath(self):
        super(Context, self).getPackageResourcePath()
        if not self.mPackageInfo:
            raise Exception('RuntimeException: "Not supported in system context"')
        baseFile = File(os.path.dirname(Android.__file__)).getParentFile()
        packagename = self.getPackageName().rsplit('.', 1)[-1]
        baseFile = File(baseFile, packagename)
        return File(baseFile, 'res')

    def getSharedPreferences(self, name, mode):
        super(Context, self).getSharedPreferences(name, mode)

    def bindService(self, service, conn, flags):
        super(Context, self).bindService(service, conn, flags)

    def openOrCreateDatabase(self, name, mode, factory, errorHandler):
        return super(Context, self).openOrCreateDatabase(name, mode, factory, errorHandler)

    def _createPrivateDir(self, name):
        filesDir = File(self.getDataDir(), name)
        if not filesDir.exists():
            with File.sync:
                try:
                    filesDir.mkdirs()
                except Exception as e:
                    raise Exception('SecurityException: "%s%' % e.message)
        return filesDir




