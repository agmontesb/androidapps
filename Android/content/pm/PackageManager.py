# -*- coding: utf-8 -*-
from Android.content import IntentFilter
from Android.content.Intent import Intent
from Android.interface.IPackageManager import IPackageManager
from SystemManager import SystemTablesContract as contract
from SystemManager.SystemTablesProvider import SystemTablesProvider


class PackageManager(IPackageManager):

    def __init__(self):
        self._sysprovider = SystemTablesProvider()

    def getActivityBanner(self, activity_or_intent):
        """Retrieve the banner associated with an activity."""
        dummy = activity_or_intent
        if isinstance(dummy, tuple):
            component_info = self.getActivityInfo(dummy, 0)
        elif isinstance(dummy, Intent):
            component_info = self.queryIntentActivities(dummy, 0)[0]
        else:
            raise TypeError('PackageManager.TypeError: Not the required parameters type')

    def getActivityIcon(self, intent_or_activityName):
        """Retrieve the icon associated with an Intent."""
        pass

    def getActivityInfo(self, component, flags):
        """Retrieve all of the information we know about a particular activity class."""
        return self._getComponentInfo(component)

    def getActivityLogo(self, intent_or_activityName):
        """Retrieve the logo associated with an Intent."""
        pass

    def getApplicationBanner(self, intent_or_packageName):
        """Retrieve the banner associated with an application."""
        pass

    def getApplicationIcon(self, info_or_packageName):
        """Retrieve the icon associated with an application."""
        pass

    def getApplicationInfo(self, packageName, flags):
        """Retrieve all of the information we know about a particular package/application."""
        pass

    def getApplicationLabel(self, info):
        """Return the label to use for this application."""
        pass

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
        pass

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
        pass

    def getResourcesForActivity(self, activityName):
        """Retrieve the resources associated with an activity."""
        pass

    def getResourcesForApplication(self, app_or_appPackageName):
        """Retrieve the resources for an application."""
        pass

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
        return self._getComponentsInfoForIntent('activity', intent)

    def queryIntentActivityOptions(self, caller, specifics, intent, flags):
        """Retrieve a set of activities that should be presented to the user
        as similar options."""
        pass

    def queryIntentContentProviders(self, intent, flags):
        """Retrieve all providers that can match the given intent."""
        pass

    def resolveActivity(self, intent, flags):
        """Determine the best action to perform for a given Intent."""
        pass

    def resolveContentProvider(self, name, flags):
        """Find a single content provider by its base path name."""
        pass

    def setInstallerPackageName(self, targetPackage, installerPackageName):
        """Change the installer associated with a given package."""
        pass

    def _getPackageInfo(self, package_name):
        table_class = contract.InstalledPackages
        sel_string = '%s=?' % table_class.COLUMN_NAME
        sel_args = (package_name,)
        kwargs = dict(uri=table_class.CONTENT_URI, selection=sel_string, selectionArgs=sel_args)
        try:
            cursor = self._sysprovider.query(**kwargs)
            package_info = cursor.fetchone()
        except:
            raise Exception('PackageManager.NameNotFoundException')
        else:
            cursor.close()
        return package_info

    def _getComponentInfo(self, component):
        package_name, activity_name = component
        package_info = self._getPackageInfo(package_name)
        table_class = contract.SystemComponents
        sel_string = '%s=? AND %s=?' % (table_class.COLUMN_PACKAGE_ID, table_class.COLUMN_PARENT)
        sel_args = (package_info[0], activity_name)
        kwargs = dict(uri=table_class.CONTENT_URI, selection=sel_string, selectionArgs=sel_args)
        try:
            cursor = self._sysprovider.query(**kwargs)
            component_info = cursor.fetchall()
        except:
            raise Exception('PackageManager.NameNotFoundException')
        else:
            cursor.close()
        return component_info

    def _getComponentsInfoForIntent(self, component_type, intent):
        table_class = contract.SystemComponents
        table_name = table_class.TABLE_NAME
        sel_string = '%s=?' % table_class.COLUMN_TYPE
        sel_args = (component_type, )
        kwargs = dict(table=table_name, selection=sel_string, selectionArgs=sel_args)
        cursor = self._sysprovider.query(**kwargs)
        try:
            component_info = zip(*cursor.fetchall())[0]
        except:
            raise Exception('PackageManager.NameNotFoundException')
        component_type = 'intent-filter'
        component_ids = map(lambda x: x[0], component_info)
        sel_string = '%s=? AND %s IN %s' % (table_class.COLUMN_TYPE, table_class.COLUMN_PARENT, component_ids)
        sel_args = (component_type, )
        kwargs = dict(table=table_name, selection=sel_string, selectionArgs=sel_args)
        cursor = self._sysprovider.query(**kwargs)
        try:
            intent_filters = cursor.fetchall()
        except:
            raise Exception('PackageManager.NameNotFoundException')

        answ = []
        SUCCESS = (IntentFilter.MATCH_CATEGORY_MASK | IntentFilter.MATCH_ADJUSTMENT_MASK)
        for item in intent_filters:
            ifilter = item[-1]
            imatch = ifilter.matchIntent(None, intent, False, '')
            if imatch & SUCCESS:
                answ.append(item)
        return filter(lambda x: x[0] in answ, component_info)

