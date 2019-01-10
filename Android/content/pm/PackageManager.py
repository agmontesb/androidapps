# -*- coding: utf-8 -*-
import Android
from Android import overload
from Android.content.Intent import Intent
from Android.interface.IPackageManager import IPackageManager
from SystemManager.SystemTablesProvider import SystemTablesProvider


class PackageManager(IPackageManager):

    def __init__(self):
        super(PackageManager, self).__init__()
        self._sysprovider = SystemTablesProvider()

    @overload('ComponentName')
    def getActivityBanner(self, activityName):
        ai = self.getActivityInfo(activityName, 0)
        return ai.loadBanner(self)

    @getActivityBanner.adddef('Intent')
    def getActivityBanner(self, intent):
        componentname = Intent.resolveActivity(self)
        if not componentname:
            raise  Exception('PackageManager.NameNotFoundException')
        return self.getActivityBanner(componentname)

    @overload('ComponentName')
    def getActivityIcon(self, activityName):
        ai = self.getActivityInfo(activityName, 0)
        return ai.loadIcon(self)

    @getActivityIcon.adddef('Intent')
    def getActivityIcon(self, intent):
        componentname = Intent.resolveActivity(self)
        if not componentname:
            raise  Exception('PackageManager.NameNotFoundException')
        return self.getActivityIcon(componentname)

    def getActivityInfo(self, component, flags):
        """Retrieve all of the information we know about a particular activity class."""
        return self._sysprovider.getComponentInfo(component, flags)

    @overload('ComponentName')
    def getActivityLogo(self, activityName):
        ai = self.getActivityInfo(activityName, 0)
        return ai.loadLogo(self)

    @getActivityLogo.adddef('Intent')
    def getActivityLogo(self, intent):
        componentname = Intent.resolveActivity(self)
        if not componentname:
            raise  Exception('PackageManager.NameNotFoundException')
        return self.getActivityLogo(componentname)

    def getApplicationBanner(self, intent_or_packageName):
        """Retrieve the banner associated with an application."""
        pass

    @overload('ApplicationInfo')
    def getApplicationIcon(self, info):
        iconres = info.icon or Android.R.drawable.ic_launcher_android
        return iconres

    @getApplicationIcon.adddef('str')
    def getApplicationIcon(self, packageName):
        info = self.getApplicationInfo(packageName, 0)
        return self.getApplicationIcon(info)

    def getApplicationInfo(self, packageName, flags):
        """Retrieve all of the information we know about a particular package/application."""
        packageinfo = self.getPackageInfo(packageName, flags)
        return packageinfo.applicationInfo

    def getApplicationLabel(self, info):
        return info.name

    def getApplicationLogo(self, info_or_packageName):
        """Retrieve the logo associated with an application."""
        pass

    def getDefaultActivityIcon(self):
        """Return the generic icon for an activity that is used when no specific icon is defined."""
        pass

    def getDrawable(self, packageName, resid, appInfo):
        """Retrieve an image from a package."""
        pass

    def getInstalledApplications(self, flags):
        """Return a List of all application packages that are installed for the current user."""
        pass

    def getInstalledPackages(self, flags):
        """Return a List of all packages that are installed for the current user."""
        pass

    def getInstallerPackageName(self, packageName):
        """Retrieve the package name of the application that installed a package."""
        pass

    def getLaunchIntentForPackage(self, packageName):
        """Returns a "good" intent to launch a front-door activity in a package."""
        pass

    def getNameForUid(self, uid):
        """Retrieve the official name associated with a uid."""
        pass

    def getPackageInfo(self, packageName, flags):
        """Retrieve overall information about an application package that is
        installed on the system."""
        return self._sysprovider.getPackageInfo(packageName, flags)

    def getPackageInstaller(self):
        """Return interface that offers the ability to install, upgrade,
        and remove applications on the device."""
        pass

    def getPackageUid(self, packageName, flags):
        """Return the UID associated with the given package name."""
        pass

    def getPackagesForUid(self, uid):
        """Retrieve the names of all packages that are associated with a
        particular user id."""
        pass

    def getProviderInfo(self, component, flags):
        """Retrieve all of the information we know about a particular content
        provider class."""
        return self._sysprovider.getComponentInfo(component, flags)

    def getResourcesForActivity(self, activityName):
        """Retrieve the resources associated with an activity."""
        ai = self.getActivityInfo(activityName, 0)
        return self.getResourcesForApplication(ai.applicationInfo)

    @overload('ApplicationInfo')
    def getResourcesForApplication(self, app):

        pass

    @getResourcesForApplication.adddef('str')
    def getResourcesForApplication(self, appPackageName):
        ai = self.getApplicationInfo(appPackageName)
        return self.getResourcesForApplication(ai)

    def getText(self, packageName, resid, appInfo):
        """Retrieve text from a package."""
        pass

    def getXml(self, packageName, resid, appInfo):
        """Retrieve an XML file from a package."""
        pass

    def queryContentProviders(self, processName, uid, flags):
        """Retrieve content provider information."""
        pass

    def queryIntentActivities(self, intent, flags):
        """Retrieve all activities that can be performed for the given intent."""
        return self._sysprovider.getComponentsInfoForIntent('activity', intent, flags)

    def queryIntentActivityOptions(self, caller, specifics, intent, flags):
        """Retrieve a set of activities that should be presented to the user
        as similar options."""
        pass

    def queryIntentContentProviders(self, intent, flags):
        """Retrieve all providers that can match the given intent."""
        return self._sysprovider.getComponentsInfoForIntent('provider', intent, flags)

    def resolveActivity(self, intent, flags):
        """Determine the best action to perform for a given Intent."""
        resolveinfos = self.queryIntentActivities(intent, flags)
        return resolveinfos[0] if resolveinfos else None

    def resolveContentProvider(self, name, flags):
        """Find a single content provider by its base path name."""
        return self._sysprovider.getComponentInfo(name, flags)

    def setInstallerPackageName(self, targetPackage, installerPackageName):
        """Change the installer associated with a given package."""
        pass

    def getLaunchIntentForPackage(self, packageName):
        pass