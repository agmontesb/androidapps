# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/ResolveInfo"""
from Android import overload
from Android.Os.Parcel import Parcel
from Android.content.ComponentName import ComponentName
from Android.content.IntentFilter import IntentFilter
from Android.content.pm.ActivityInfo import ActivityInfo
from Android.content.pm.ProviderInfo import ProviderInfo
from Android.interface.IParcelable import IParcelable


class ResolveInfo(IParcelable):
    """
    Information that is returned from resolving an intent against an IntentFilter.
    This partially corresponds to information collected from the
    AndroidManifest.xml's <intent> tags.
    """

    """
    public static final Creator<ResolveInfo> CREATOR:
    
    """
    CREATOR = type(
        'ResolveInfoCreator',
        (IParcelable.ICreator,), {
            'createFromParcel': lambda self, inparcel: ResolveInfo()._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * ResolveInfo)()
        })()


    @overload
    def __init__(self):
        """"""
        super(ResolveInfo, self).__init__()
        """
        public ActivityInfo activityInfo:
        The activity or broadcast receiver that corresponds to this resolution
        match, if this resolution is for an activity or broadcast receiver.
        Exactly one of activityInfo, serviceInfo, or
        providerInfo will be non-null.
        """
        self.activityInfo = None

        """
        public IntentFilter filter:
        The IntentFilter that was matched for this ResolveInfo.
        """
        self.filter = None

        """
        public int icon:
        A drawable resource identifier (in the package's resources) of this
        match's icon.  From the "icon" attribute or, if not set, 0. It is
        set only if the icon can be obtained by resource id alone.
        """
        self.icon = None

        """
        public boolean isDefault:
        This filter has specified the Intent.CATEGORY_DEFAULT, meaning it
        would like to be considered a default action that the user can
        perform on this data.
        """
        self.isDefault = None

        """
        public boolean isInstantAppAvailable:
        Whether or not an instant app is available for the resolved intent.
        """
        self.isInstantAppAvailable = None

        """
        public int labelRes:
        A string resource identifier (in the package's resources) of this
        match's label.  From the "label" attribute or, if not set, 0.
        """
        self.labelRes = None

        """
        public int match:
        The system's evaluation of how well the activity matches the
        IntentFilter.  This is a match constant, a combination of
        IntentFilter.MATCH_CATEGORY_MASK
        and IntentFiler.MATCH_ADJUSTMENT_MASK.
        """
        self.match = None

        """
        public CharSequence nonLocalizedLabel:
        The actual string retrieve from labelRes or null if none
        was provided.
        """
        self.nonLocalizedLabel = None

        """
        public int preferredOrder:
        Order of result according to the user's preference.  If the user
        has not set a preference for this result, the value is 0; higher
        values are a higher priority.
        """
        self.preferredOrder = None

        """
        public int priority:
        The declared priority of this match.  Comes from the "priority"
        attribute or, if not set, defaults to 0.  Higher values are a higher
        priority.
        """
        self.priority = None

        """
        public ProviderInfo providerInfo:
        The provider that corresponds to this resolution match, if this
        resolution is for a provider. Exactly one of activityInfo,
        serviceInfo, or providerInfo will be non-null.
        """
        self.providerInfo = None

        """
        public String resolvePackageName:
        Optional -- if non-null, the labelRes and icon
        resources will be loaded from this package, rather than the one
        containing the resolved component.
        """
        self.resolvePackageName = None

        """
        public ServiceInfo serviceInfo:
        The service that corresponds to this resolution match, if this resolution
        is for a service. Exactly one of activityInfo,
        serviceInfo, or providerInfo will be non-null.
        """
        self.serviceInfo = None

        """
        public int specificIndex:
        Only set when returned by
        PackageManager.queryIntentActivityOptions(ComponentName, Intent[], Intent, 
        int), this tells you
        which of the given specific intents this result came from.  0 is the
        first in the list, < 0 means it came from the generic Intent query.
        """
        self.specificIndex = None
        pass

    @__init__.adddef('ResolveInfo')
    def __init__(self, orig):
        """
        :param orig: ResolveInfo.
        """
        parcel = Parcel()
        orig.writeToParcel(parcel, 0)
        parcel.setDataPosition(0)
        self.__init__()
        self._readFromParcel(parcel)
        pass

    def describeContents(self):
        """
        Describe the kinds of special objects contained in this Parcelable 
        instance's marshaled representation. For example, if the object will 
        include a file descriptor in the output of writeToParcel(Parcel, int), 
        the return value of this method must include the 
        CONTENTS_FILE_DESCRIPTOR bit.
        :return: int. a bitmask indicating the set of special object types 
        marshaled by this Parcelable object instance.
        """
        return 0

    def dump(self, pw, prefix):
        """
        :param pw: Printer
        :param prefix: String
        """
        pass

    def getIconResource(self):
        """
        Return the icon resource identifier to use for this match.  If the 
        match defines an icon, that is used; else if the activity defines an 
        icon, that is used; else, the application icon is used.
        :return: int. The icon associated with this match.
        """
        if self.icon: return self.icon
        ci = self._getComponentInfo()
        if ci.icon: return ci.icon
        return ci.applicationInfo.icon

    def loadIcon(self, pm):
        """
        Retrieve the current graphical icon associated with this resolution.  
        This will call back on the given PackageManager to load the icon from 
        the application.
        :param pm: PackageManager: A PackageManager from which the icon can be 
        loaded; usually the PackageManager from which you originally retrieved 
        this item.
        :return: Drawable. Returns a Drawable containing the resolution's 
        icon.  If the item does not have an icon, the default activity icon is 
        returned.
        """
        dr = None
        if self.resolvePackageName and self.getIconResource():
            dr = pm.getDrawable(self.resolvePackageName, self.getIconResource(), None)
        ci = self._getComponentInfo()
        if dr is None and self.getIconResource():
            ai = ci.applicationInfo
            dr = pm.getDrawable(ci.packageName, self.getIconResource(), ai)
        if dr is not None:
            return pm.getUserBadgedIcon(dr, pm.getUserId())
        return ci.loadIcon(pm)

    def loadLabel(self, pm):
        """
        Retrieve the current textual label associated with this resolution.  
        This will call back on the given PackageManager to load the label from 
        the application.
        :param pm: PackageManager: A PackageManager from which the label can 
        be loaded; usually the PackageManager from which you originally 
        retrieved this item.
        :return: CharSequence. Returns a CharSequence containing the 
        resolutions's label.  If the item does not have a label, its name is 
        returned.
        """
        if self.nonLocalizedLabel:
            return self.nonLocalizedLabel
        if self.resolvePackageName and self.labelRes:
            label = pm.getText(self.resolvePackageName, self.labelRes, None)
            if label: return label.strip()
        ci = self._getComponentInfo()
        ai = ci.applicationInfo
        if self.labelRes:
            label = pm.getText(ci.packageName, self.labelRes, ai)
            if label: return label.strip()
        data = ci.loadLabel(pm)
        return data.strip()

    def toString(self):
        """
        Returns a string representation of the object. In general, the 
        toString method returns a string that "textually represents" this 
        object. The result should be a concise but informative representation 
        that is easy for a person to read. It is recommended that all 
        subclasses override this method.  The toString method for class Object 
        returns a string consisting of the name of the class of which the 
        object is an instance, the at-sign character `@', and the unsigned 
        hexadecimal representation of the hash code of the object. In other 
        words, this method returns a string equal to the value of:  
        getClass().getName() + '@' + Integer.toHexString(hashCode())
        :return: String. a string representation of the object.
        """
        ci = self._getComponentInfo()
        items = []
        items.append(ComponentName(ci.packageName, ci.name).toShortString())
        if self.priority: items.append('p=%s' % self.priority)
        if self.preferredOrder: items.append('o=%s' % self.preferredOrder)
        items.append('m=0x{:0>8x}'.format(self.match))
        return 'ResolveInfo{' + ' '.join(items) + '}'

    def writeToParcel(self, dest, parcelableFlags):
        """
        Flatten this object in to a Parcel.
        :param dest: Parcel: The Parcel in which the object should be written.
        :param parcelableFlags: int: Additional flags about how the object 
        should be written. May be 0 or 
        Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        if self.activityInfo:
            dest.writeInt(1)
            self.activityInfo.writeToParcel(dest, parcelableFlags)
        elif self.serviceInfo:
            dest.writeInt(2)
            self.serviceInfo.writeToParcel(dest, parcelableFlags)
        elif self.providerInfo:
            dest.writeInt(3)
            self.providerInfo.writeToParcel(dest, parcelableFlags)
        else:
            dest.writeInt(0)

        if self.filter:
            dest.writeInt(1)
            self.filter.writeToParcel(dest, parcelableFlags)
        else:
            dest.writeInt(0)
        
        dest.writeInt(self.priority)
        dest.writeInt(self.preferredOrder)
        dest.writeInt(self.match)
        dest.writeInt(self.specificIndex)
        dest.writeInt(self.labelRes)
        # TextUtils.writeToParcel(nonLocalizedLabel, dest, parcelableFlags)
        dest.writeInt(self.icon)
        dest.writeString(self.resolvePackageName)
        # dest.writeInt(self.targetUserId)
        # dest.writeInt(self.system ? 1: 0)
        # dest.writeInt(noResourceId ? 1: 0)
        # dest.writeInt(iconResourceId)
        # dest.writeInt(self.handleAllWebDataURI ? 1: 0)
        dest.writeInt(1*bool(self.isInstantAppAvailable))

    def _readFromParcel(self, src):
        '''
        :param src: Parcel: The Parcel in which the object is written.
        :return ActivityInfo:
        '''
        info = src.readInt()
        if info == 1:
            self.activityInfo = ActivityInfo.CREATOR.createFromParcel(src)
        elif info == 2:
            # self.serviceInfo = ServiceInfo.CREATOR.createFromParcel(src)
            pass
        elif info == 3:
            self.providerInfo = ProviderInfo.CREATOR.createFromParcel(src)
            pass

        if src.readInt():
            self.filter = IntentFilter.CREATOR.createFromParcel(src)

        self.priority = src.readInt()
        self.preferredOrder = src.readInt()
        self.match = src.readInt()
        self.specificIndex = src.readInt()
        self.labelRes = src.readInt()
        # nonLocalizedLabel = TextUtils.CHAR_SEQUENCE_CREATOR.createFromParcel(source)

        self.icon = src.readInt()
        self.resolvePackageName = src.readString()
        # targetUserId = source.readInt()
        # system = source.readInt() != 0
        # noResourceId = source.readInt() != 0
        # iconResourceId = source.readInt()
        # handleAllWebDataURI = source.readInt() != 0
        self.isInstantAppAvailable = bool(src.readInt())


    def _getComponentInfo(self):
        component_info = self.activityInfo or self.providerInfo or self.providerInfo
        return component_info

