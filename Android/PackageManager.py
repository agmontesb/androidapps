# -*- coding: utf-8 -*-


class PackageManager(object):
    def addPackageToPreferred(self, packageName):
        """This method was deprecated in API level 7. This function no longer does anything; it was an old approach to managing preferred activities, which has been superseded by (and conflicts with) the modern activity-based preferences.                                            abstract                                        boolean                      addPermission(PermissionInfo info) Add a new dynamic permission to the system."""
        pass

    def addPermissionAsync(self, info):
        """Like addPermission(PermissionInfo) but asynchronously persists the package manager state after returning from the call, allowing it to return quicker and batch a series of adds at the expense of no guarantee the added permission will be retained if the device is rebooted before it is written."""
        pass

    def addPreferredActivity(self, filter, match, set, activity):
        """This method was deprecated in API level 8.
        This is a protected API that should not have been available to third party
        applications.
        It is the platform's responsibility for assigning preferred activities and
        this cannot be directly modified.
        Add a new preferred activity mapping to the system.
        This will be used to automatically select the given activity component when
        Context.startActivity() finds multiple matching activities and also matches
        the given filter. abstract                                        boolean                      canRequestPackageInstalls()                    Checks whether the calling package is allowed to request package installs through package installer."""
        pass

    def canonicalToCurrentPackageNames(self, names):
        """Map from a packages canonical name to the current name in use on the
        device."""
        pass

    def checkPermission(self, permName, pkgName):
        """Check whether a particular package has been granted a particular
        permission."""
        pass

    def checkSignatures(self, pkg1, pkg2):
        """Compare the signatures of two packages to determine if the same
        signature appears in both of them."""
        pass

    def checkSignatures(self, uid1, uid2):
        """Like checkSignatures(String, String), but takes UIDs of the two packages
        to be checked."""
        pass

    def clearInstantAppCookie(self):
        """Clears the instant application cookie for the calling app."""
        pass

    def clearPackagePreferredActivities(self, packageName):
        """Remove all preferred activity mappings, previously added with
        addPreferredActivity(IntentFilter, int, ComponentName[], ComponentName),
        from the system whose activities are implemented in the given package name."""
        pass

    def currentToCanonicalPackageNames(self, names):
        """Map from the current package names in use on the device to whatever the
        current canonical name of that package is."""
        pass

    def extendVerificationTimeout(self, id, verificationCodeAtTimeout, millisecondsToDelay):
        """Allows a package listening to the package verification broadcast to extend
        the default timeout for a response and declare what action to perform after
        the timeout occurs."""
        pass

    def getActivityBanner(self, activityName):
        """Retrieve the banner associated with an activity."""
        pass

    def getActivityBanner(self, intent):
        """Retrieve the banner associated with an Intent."""
        pass

    def getActivityIcon(self, intent):
        """Retrieve the icon associated with an Intent."""
        pass

    def getActivityIcon(self, activityName):
        """Retrieve the icon associated with an activity."""
        pass

    def getActivityInfo(self, component, flags):
        """Retrieve all of the information we know about a particular activity class."""
        pass

    def getActivityLogo(self, intent):
        """Retrieve the logo associated with an Intent."""
        pass

    def getActivityLogo(self, activityName):
        """Retrieve the logo associated with an activity."""
        pass

    def getAllPermissionGroups(self, flags):
        """Retrieve all of the known permission groups in the system."""
        pass

    def getApplicationBanner(self, packageName):
        """Retrieve the banner associated with an application."""
        pass

    def getApplicationBanner(self, info):
        """Retrieve the banner associated with an application."""
        pass

    def getApplicationEnabledSetting(self, packageName):
        """Return the enabled setting for an application."""
        pass

    def getApplicationIcon(self, info):
        """Retrieve the icon associated with an application."""
        pass

    def getApplicationIcon(self, packageName):
        """Retrieve the icon associated with an application."""
        pass

    def getApplicationInfo(self, packageName, flags):
        """Retrieve all of the information we know about a particular package/application."""
        pass

    def getApplicationLabel(self, info):
        """Return the label to use for this application."""
        pass

    def getApplicationLogo(self, packageName):
        """Retrieve the logo associated with an application."""
        pass

    def getApplicationLogo(self, info):
        """Retrieve the logo associated with an application."""
        pass

    def getChangedPackages(self, sequenceNumber):
        """Returns the names of the packages that have been changed [eg."""
        pass

    def getComponentEnabledSetting(self, componentName):
        """Return the enabled setting for a package component
        (activity, receiver, service, provider)."""
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

    def getInstantAppCookie(self):
        """Gets the instant application cookie for this app."""
        pass

    def getInstantAppCookieMaxBytes(self):
        """Gets the maximum size in bytes of the cookie data an instant app can store
        on the device."""
        pass

    def getInstrumentationInfo(self, className, flags):
        """Retrieve all of the information we know about a particular instrumentation
        class."""
        pass

    def getLaunchIntentForPackage(self, packageName):
        """Returns a "good" intent to launch a front-door activity in a package."""
        pass

    def getLeanbackLaunchIntentForPackage(self, packageName):
        """Return a "good" intent to launch a front-door Leanback activity in a
        package, for use for example to implement an "open" button when browsing
        through packages."""
        pass

    def getNameForUid(self, uid):
        """Retrieve the official name associated with a uid."""
        pass

    def getPackageArchiveInfo(self, archiveFilePath, flags):
        """Retrieve overall information about an application package defined in a
        package archive file """
        pass

    def getPackageGids(self, packageName, flags):
        """Return an array of all of the POSIX secondary group IDs that have
        been assigned to the given package."""
        pass

    def getPackageInfo(self, packageName, flags):
        """Retrieve overall information about an application package that is
        installed on the system."""
        pass

    def getPackageInfo(self, versionedPackage, flags):
        """Retrieve overall information about an application package that is
        installed on the system."""
        pass

    def getPackageInstaller(self):
        """Return interface that offers the ability to install, upgrade, and remove applications on the device."""
        pass

    def getPackageUid(self, packageName, flags):
        """Return the UID associated with the given package name."""
        pass

    def getPackagesForUid(self, uid):
        """Retrieve the names of all packages that are associated with a particular user id."""
        pass

    def getPackagesHoldingPermissions(self, permissions, flags):
        """Return a List of all installed packages that are currently holding any of the given permissions."""
        pass

    def getPermissionGroupInfo(self, name, flags):
        """Retrieve all of the information we know about a particular group of permissions."""
        pass

    def getPermissionInfo(self, name, flags):
        """Retrieve all of the information we know about a particular permission."""
        pass

    def getPreferredActivities(self, outFilters, outActivities, packageName):
        """Retrieve all preferred activities, previously added with
        addPreferredActivity(IntentFilter, int, ComponentName[], ComponentName),
        that are currently registered with the system."""
        pass

    def getPreferredPackages(self, flags):
        """Retrieve the list of all currently configured preferred packages."""
        pass

    def getProviderInfo(self, component, flags):
        """Retrieve all of the information we know about a particular content
        provider class."""
        pass

    def getReceiverInfo(self, component, flags):
        """Retrieve all of the information we know about a particular receiver class."""
        pass

    def getResourcesForActivity(self, activityName):
        """Retrieve the resources associated with an activity."""
        pass

    def getResourcesForApplication(self, app):
        """Retrieve the resources for an application."""
        pass

    def getResourcesForApplication(self, appPackageName):
        """Retrieve the resources associated with an application."""
        pass

    def getServiceInfo(self, component, flags):
        """Retrieve all of the information we know about a particular service class."""
        pass

    def getSharedLibraries(self, flags):
        """Get a list of shared libraries on the device."""
        pass

    def getSuspendedPackageAppExtras(self):
        """Returns a Bundle of extras that was meant to be sent to the calling app when it was suspended."""
        pass

    def getSystemAvailableFeatures(self):
        """Get a list of features that are available on the system."""
        pass
    def getSystemSharedLibraryNames(self):
        """Get a list of shared libraries that are available on the system."""
        pass

    def getText(self, packageName, resid, appInfo):
        """Retrieve text from a package."""
        pass

    def getUserBadgedDrawableForDensity(self, drawable, user, badgeLocation, badgeDensity):
        """If the target user is a managed profile of the calling user or the caller is itself a managed profile, then this returns a badged copy of the given drawable allowing the user to distinguish it from the original drawable."""
        pass

    def getUserBadgedIcon(self, icon, user):
        """If the target user is a managed profile, then this returns a badged copy of the given icon to be able to distinguish it from the original icon."""
        pass

    def getUserBadgedLabel(self, label, user):
        """If the target user is a managed profile of the calling user or the caller is itself a managed profile, then this returns a copy of the label with badging for accessibility services like talkback."""
        pass

    def getXml(self, packageName, resid, appInfo):
        """Retrieve an XML file from a package."""
        pass

    def hasSigningCertificate(self, uid, certificate, type):
        """Searches the set of signing certificates by which the package(s) for the given uid has proven to have been signed."""
        pass

    def hasSigningCertificate(self, packageName, certificate, type):
        """Searches the set of signing certificates by which the given package has proven to have been signed."""
        pass

    def hasSystemFeature(self, name):
        """Check whether the given feature name is one of the available features as returned by getSystemAvailableFeatures()."""
        pass

    def hasSystemFeature(self, name, version):
        """Check whether the given feature name and version is one of the available features as returned by getSystemAvailableFeatures()."""
        pass

    def isInstantApp(self):
        """Gets whether this application is an instant app."""
        pass

    def isInstantApp(self, packageName):
        """Gets whether the given package is an instant app."""
        pass

    def isPackageSuspended(self):
        """Apps can query this to know if they have been suspended."""
        pass

    def isPermissionRevokedByPolicy(self, permName, pkgName):
        """Checks whether a particular permissions has been revoked for a package by policy."""
        pass

    def isSafeMode(self):
        """Return whether the device has been booted into safe mode."""
        pass

    def queryBroadcastReceivers(self, intent, flags):
        """Retrieve all receivers that can handle a broadcast of the given intent."""
        pass

    def queryContentProviders(self, processName, uid, flags):
        """Retrieve content provider information."""
        pass

    def queryInstrumentation(self, targetPackage, flags):
        """Retrieve information about available instrumentation code."""
        pass

    def queryIntentActivities(self, intent, flags):
        """Retrieve all activities that can be performed for the given intent."""
        pass

    def queryIntentActivityOptions(self, caller, specifics, intent, flags):
        """Retrieve a set of activities that should be presented to the user
        as similar options."""
        pass

    def queryIntentContentProviders(self, intent, flags):
        """Retrieve all providers that can match the given intent."""
        pass

    def queryIntentServices(self, intent, flags):
        """Retrieve all services that can match the given intent."""
        pass

    def queryPermissionsByGroup(self, group, flags):
        """Query for all of the permissions associated with a particular group."""
        pass

    def removePackageFromPreferred(self, packageName):
        """      This method was deprecated      in API level 7.    This function no longer does anything; it was an old approach to managing preferred activities, which has been superseded by (and conflicts with) the modern activity-based preferences.                                            abstract                                        void                      removePermission(String name)                    Removes a permission that was previously added with addPermission(PermissionInfo)."""
        pass

    def resolveActivity(self, intent, flags):
        """Determine the best action to perform for a given Intent."""
        pass

    def resolveContentProvider(self, name, flags):
        """Find a single content provider by its base path name."""
        pass

    def resolveService(self, intent, flags):
        """Determine the best service to handle for a given Intent."""
        pass

    def setApplicationCategoryHint(self, packageName, categoryHint):
        """Provide a hint of what the ApplicationInfo.category value should be for the given package."""
        pass

    def setApplicationEnabledSetting(self, packageName, newState, flags):
        """Set the enabled setting for an application This setting will override any enabled state which may have been set by the application in its manifest."""
        pass

    def setComponentEnabledSetting(self, componentName, newState, flags):
        """Set the enabled setting for a package component (activity, receiver, service, provider)."""
        pass

    def setInstallerPackageName(self, targetPackage, installerPackageName):
        """Change the installer associated with a given package."""
        pass

    def updateInstantAppCookie(self, cookie):
        """Updates the instant application cookie for the calling app."""
        pass

    def verifyPendingInstall(self, id, verificationCode):
        """Allows a package listening to the package verification broadcast to respond to the package manager."""
        pass
