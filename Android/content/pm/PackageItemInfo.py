# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/PackageItemInfo"""
from Android import Object, overload
from Android.Os.Bundle import Bundle
from Android.Os.Parcel import Parcel

class PackageItemInfo(Object):
    """
    Base class containing information common to all package items held by the 
    package manager. This provides a very common basic set of attributes: a 
    label, icon, and meta-data. This class is not intended to be used by 
    itself; it is simply here to share common definitions between all items 
    returned by the package manager. As such, it does not itself implement 
    Parcelable, but does provide convenience methods to assist in the 
    implementation of Parcelable in subclasses.
    """

    @overload
    def __init__(self):
        super(PackageItemInfo, self).__init__()
        """
        public int banner:
        A drawable resource identifier (in the package's resources) of this
        component's banner.  From the "banner" attribute or, if not set, 0.
        """
        self.banner = 0

        """
        public int icon:
        A drawable resource identifier (in the package's resources) of this
        component's icon.  From the "icon" attribute or, if not set, 0.
        """
        self.icon = 0

        """
        public int labelRes:
        A string resource identifier (in the package's resources) of this
        component's label.  From the "label" attribute or, if not set, 0.
        """
        self.labelRes = 0

        """
        public int logo:
        A drawable resource identifier (in the package's resources) of this
        component's logo. Logos may be larger/wider than icons and are
        displayed by certain UI elements in place of a name or name/icon
        combination. From the "logo" attribute or, if not set, 0.
        """
        self.logo = 0

        """
        public Bundle metaData:
        Additional meta-data associated with this component.  This field
        will only be filled in if you set the PackageManager.GET_META_DATA 
        flag when requesting the info.
        """
        self.metaData = Bundle.EMPTY

        """
        public String name:
        Public name of this item. From the "android:name" attribute.
        """
        self.name = ''

        """
        public CharSequence nonLocalizedLabel:
        The string provided in the AndroidManifest file, if any.  You
        probably don't want to use this.  You probably want
        PackageManager.getApplicationLabel(ApplicationInfo)
        """
        self.nonLocalizedLabel = ''

        """
        public String packageName:
        Name of the package that this item is in.
        """
        self.packageName = ''

        """
        private PersistableBundle _unclasifiedFields:
        The fields declare in manifest TAG that are not asociated to a flag or
        an attribute
        """
        self._unclassifiedFields = None

    @__init__.adddef('PackageItemInfo')
    def PackageItemInfo(self, orig):
        """
        :param orig: PackageItemInfo.
        """
        self.__init__()
        parcel = Parcel()
        orig.writeToParcel(parcel, 0)
        parcel.setDataPosition(0)
        self.PackageItemInfo(parcel)

    @__init__.adddef('Parcel')
    def PackageItemInfo(self, source):
        """
        :param source: Parcel.
        """
        self.__init__()
        self._readFromParcel(source)
        pass

    def loadBanner(self, pm):
        """
        Retrieve the current graphical banner associated with this item.  This 
        will call back on the given PackageManager to load the banner from the 
        application.
        :param pm: PackageManager: A PackageManager from which the banner can 
        be loaded; usually the PackageManager from which you originally 
        retrieved this item.
        :return: Drawable. Returns a Drawable containing the item's banner.  
        If the item does not have a banner, this method will return null.
        """
        return pm.getDrawable(self.packageName, self.banner, self.applicationInfo)

    def loadIcon(self, pm):
        """
        Retrieve the current graphical icon associated with this item.  This 
        will call back on the given PackageManager to load the icon from the 
        application.
        :param pm: PackageManager: A PackageManager from which the icon can be 
        loaded; usually the PackageManager from which you originally retrieved 
        this item.
        :return: Drawable. Returns a Drawable containing the item's icon.  If 
        the item does not have an icon, the item's default icon is returned 
        such as the default activity icon.
        """
        return pm.getDrawable(self.packageName, self.icon, self.applicationInfo)

    def loadLabel(self, pm):
        """
        Retrieve the current textual label associated with this item.  This 
        will call back on the given PackageManager to load the label from the 
        application.
        :param pm: PackageManager: A PackageManager from which the label can 
        be loaded; usually the PackageManager from which you originally 
        retrieved this item.This value must never be null.
        :return: CharSequence. Returns a CharSequence containing the item's 
        label.  If the item does not have a label, its name is returned. This 
        value will never be null.
        """
        return pm.getText(self.packageName, self.labelRes, self.applicationInfo)

    def loadLogo(self, pm):
        """
        Retrieve the current graphical logo associated with this item. This 
        will call back on the given PackageManager to load the logo from the 
        application.
        :param pm: PackageManager: A PackageManager from which the logo can be 
        loaded; usually the PackageManager from which you originally retrieved 
        this item.
        :return: Drawable. Returns a Drawable containing the item's logo. If 
        the item does not have a logo, this method will return null.
        """
        return pm.getDrawable(self.packageName, self.logo, self.applicationInfo)

    def loadUnbadgedIcon(self, pm):
        """
        Retrieve the current graphical icon associated with this item without 
        the addition of a work badge if applicable. This will call back on the 
        given PackageManager to load the icon from the application.
        :param pm: PackageManager: A PackageManager from which the icon can be 
        loaded; usually the PackageManager from which you originally retrieved 
        this item.
        :return: Drawable. Returns a Drawable containing the item's icon.  If 
        the item does not have an icon, the item's default icon is returned 
        such as the default activity icon.
        """
        pass

    def loadXmlMetaData(self, pm, name):
        """
        Load an XML resource attached to the meta-data of this item.  This 
        will retrieved the name meta-data entry, and if defined call back on 
        the given PackageManager to load its XML file from the application.
        :param pm: PackageManager: A PackageManager from which the XML can be 
        loaded; usually the PackageManager from which you originally retrieved 
        this item.
        :param name: String: Name of the meta-date you would like to load.
        :return: XmlResourceParser. Returns an XmlPullParser you can use to 
        parse the XML file assigned as the given meta-data.  If the meta-data 
        name is not defined or the XML resource could not be found, null is 
        returned.
        """
        pass

    def writeToParcel(self, dest, parcelableFlags):
        """
        :param dest: Parcel
        :param parcelableFlags: int
        """
        dest.writeInt(self.banner)
        dest.writeInt(self.icon)
        dest.writeInt(self.labelRes)
        dest.writeInt(self.logo)
        dest.writeBundle(self.metaData)
        dest.writeString(self.name)
        dest.writeString(self.nonLocalizedLabel)
        dest.writeString(self.packageName)
        pass
    
    def _readFromParcel(self, src):
        '''
        :param src: Parcel: The Parcel in which the object is written.
        :return PackageItemInfo:
        '''
        self.banner = src.readInt()
        self.icon = src.readInt()
        self.labelRes = src.readInt()
        self.logo = src.readInt()
        self.metaData = src.readBundle()
        self.name = src.readString()
        self.nonLocalizedLabel = src.readString()
        self.packageName = src.readString()
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
