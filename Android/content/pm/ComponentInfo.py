# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/ComponentInfo"""
from Android import overload
from Android.Os.Parcel import Parcel
from PackageItemInfo import PackageItemInfo


class ComponentInfo(PackageItemInfo):
    """
    Base class containing information common to all application components ( 
    ActivityInfo , ServiceInfo ). This class is not intended to be used by 
    itself; it is simply here to share common definitions between all 
    application components. As such, it does not itself implement Parcelable, 
    but does provide convenience methods to assist in the implementation of 
    Parcelable in subclasses.
    """

    @overload
    def __init__(self):
        super(ComponentInfo, self).__init__()
        """
        public ApplicationInfo applicationInfo:
        Global information about the application/package this component is a
        part of.
        """
        self.applicationInfo = None

        """
        public int descriptionRes:
        A string resource identifier (in the package's resources) containing
        a user-readable description of the component.  From the "description"
        attribute or, if not set, 0.
        """
        self.descriptionRes = 0

        """
        public boolean directBootAware:
        Indicates if this component is aware of direct boot lifecycle, and can be
        safely run before the user has entered their credentials (such as a lock
        pattern or PIN).
        """
        self.directBootAware = False

        """
        public boolean enabled:
        Indicates whether or not this component may be instantiated.  Note that 
        this value can be
        overridden by the one in its parent ApplicationInfo.
        """
        self.enabled = True

        """
        public boolean exported:
        Set to true if this component is available for use by other applications.
        Comes from android:exported of the
        <activity>, <receiver>, <service>, or
        <provider> tag.
        """
        self.exported = False

        """
        public String processName:
        The name of the process this component should run in.
        From the "android:process" attribute or, if not set, the same
        as applicationInfo.processName.
        """
        self.processName = ''

        """
        public String splitName:
        The name of the split in which this component is declared.
        Null if the component was declared in the base APK.
        """
        self.splitName = ''

    @__init__.adddef('ComponentInfo')
    def ComponentInfo(self, orig):
        """
        :param orig: ComponentInfo.
        """
        parcel = Parcel()
        orig.writeToParcel(parcel, 0)
        parcel.setDataPosition(0)
        self.__init__()
        self._readFromParcel(parcel)

    @__init__.adddef('Parcel')
    def ComponentInfo(self, source):
        """
        :param source: Parcel.
        """
        self.__init__()
        self._readFromParcel(source)

    def _getCommonResource(self, attrname):
        try:
            return getattr(self, attrname) or getattr(self.applicationInfo, attrname)
        except:
            pass
        
    def getBannerResource(self):
        """
        Return the banner resource identifier to use for this component. If 
        the component defines a banner, that is used; else, the application 
        banner is used.
        :return: int. The banner associated with this component.
        """
        return self._getCommonResource('banner')

    def getIconResource(self):
        """
        Return the icon resource identifier to use for this component.  If the 
        component defines an icon, that is used; else, the application icon is 
        used.
        :return: int. The icon associated with this component.
        """
        return self._getCommonResource('icon')

    def getLogoResource(self):
        """
        Return the logo resource identifier to use for this component.  If the 
        component defines a logo, that is used; else, the application logo is 
        used.
        :return: int. The logo associated with this component.
        """
        return self._getCommonResource('logo')

    def isEnabled(self):
        """
        Return whether this component and its enclosing application are 
        enabled.
        :return: boolean.
        """
        answ = self.applicationInfo.enabled if self.applicationInfo else True
        return answ and self.enabled

    def writeToParcel(self, dest, parcelableFlags):
        """
        :param dest: Parcel
        :param parcelableFlags: int
        """
        super(ComponentInfo, self).writeToParcel(dest, parcelableFlags)
        dest.writeParcelable(self.applicationInfo, 0)
        dest.writeInt(self.descriptionRes)
        dest.writeInt(self.directBootAware)
        dest.writeInt(self.enabled)
        dest.writeInt(self.exported)
        dest.writeString(self.processName)
        dest.writeString(self.splitName)
        
    def _readFromParcel(self, src):
        '''
        :param src: Parcel: The Parcel in which the object is written.
        :return ComponentInfo:
        '''
        super(ComponentInfo, self)._readFromParcel(src)
        self.applicationInfo = src.readParcelable(None)
        self.descriptionRes = src.readInt()
        self.directBootAware = src.readInt()
        self.enabled = src.readInt()
        self.exported = src.readInt()
        self.processName = src.readString()
        self.splitName = src.readString()
        return self

    def dumpBack(self, pw, prefix):
        """
        :param pw: Printer
        :param prefix: String
        """
        pass

    def dumpFront(self, pw, prefix):
        """
        :param pw: Printer
        :param prefix: String
        """
        pass
