# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/ProviderInfo"""
from Android import overload
from Android.Os.Parcel import Parcel
from Android.content.pm.ComponentInfo import ComponentInfo
from Android.interface.IParcelable import IParcelable, ICreator


"""
public static final int FLAG_SINGLE_USER:
Bit in flags: If set, a single instance of the provider will
run for all users on the device.  Set from the
R.attr.singleUser attribute.
"""
FLAG_SINGLE_USER = 0x40000000


class ProviderInfo(ComponentInfo, IParcelable):
    """
    Holds information about a specific content provider . This is returned by 
    PackageManager.resolveContentProvider() .
    """

    """
    public static final Creator<ProviderInfo> CREATOR:
    
    """
    CREATOR = type(
        'ProviderInfoCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: ProviderInfo()._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * ProviderInfo)()
        })()

    @overload
    def __init__(self):
        super(ProviderInfo, self).__init__()
        """
        public String authority:
        The name provider is published under content://
        """
        self.authority = ''

        """
        public int flags:
        Options that have been set in the provider declaration in the
        manifest.
        These include: FLAG_SINGLE_USER.
        """
        self.flags = 0

        """
        public boolean grantUriPermissions:
        If true, additional permissions to specific Uris in this content
        provider can be granted, as per the grantUriPermissions attribute.
        """
        self.grantUriPermissions = False

        """
        public int initOrder:
        Used to control initialization order of single-process providers
        running in the same process.  Higher goes first.
        """
        self.initOrder = 0

        """
        public boolean isSyncable:

        This field was deprecated
        in API level 5.
        This flag is now being ignored. The current way to make a provider
        syncable is to provide a SyncAdapter service for a given provider/account 
        type.

        Whether or not this provider is syncable.
        """
        self.isSyncable = False

        """
        public boolean multiprocess:
        If true, this content provider allows multiple instances of itself
        to run in different process.  If false, a single instances is always
        run in ComponentInfo.processName.
        """
        self.multiprocess = True

        """
        public PathPermission[] pathPermissions:
        If non-null, these are path-specific permissions that are allowed for
        accessing the provider.  Any permissions listed here will allow a
        holding client to access the provider, and the provider will check
        the URI it provides when making calls against the patterns here.
        """
        self.pathPermissions = []

        """
        public String readPermission:
        Optional permission required for read-only access this content
        provider.
        """
        self.readPermission = ''

        """
        public PatternMatcher[] uriPermissionPatterns:
        If non-null, these are the patterns that are allowed for granting URI
        permissions.  Any URI that does not match one of these patterns will not
        allowed to be granted.  If null, all URIs are allowed.  The
        PackageManager.GET_URI_PERMISSION_PATTERNS flag must be specified for
        this field to be filled in.
        """
        self.uriPermissionPatterns = []

        """
        public String writePermission:
        Optional permission required for read/write access this content
        provider.
        """
        self.writePermission = ''

        pass

    @__init__.adddef('ProviderInfo')
    def ProviderInfo(self, orig):
        """
        :param orig: ProviderInfo.
        """
        parcel = Parcel()
        orig.writeToParcel(parcel, 0)
        parcel.setDataPosition(0)
        self.__init__()
        self._readFromParcel(parcel)

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
        return self.__str__()

    def writeToParcel(self, out, parcelableFlags):
        """
        :param out: Parcel
        :param parcelableFlags: int
        """
        super(ProviderInfo, self).writeToParcel(out, parcelableFlags)
        out.writeString(self.authority)
        out.writeInt(self.flags)
        out.writeByte(self.grantUriPermissions)
        out.writeInt(self.initOrder)
        out.writeByte(self.isSyncable)
        out.writeByte(self.multiprocess)
        out.writeParcelableArray(self.pathPermissions, 0)
        out.writeString(self.readPermission)
        out.writeParcelableArray(self.uriPermissionPatterns, 0)
        out.writeString(self.writePermission)
        
    def _readFromParcel(self, src):
        '''
        :param src: Parcel: The Parcel in which the object is written.
        :return ProviderInfo:
        '''
        super(ProviderInfo, self)._readFromParcel(src)
        self.authority = src.readString()
        self.flags = src.readInt()
        self.grantUriPermissions = bool(src.readByte())
        self.initOrder = src.readInt()
        self.isSyncable = bool(src.readByte())
        self.multiprocess = bool(src.readByte())
        self.pathPermissions = src.readParcelableArray(None)
        self.readPermission = src.readString()
        self.uriPermissionPatterns = src.readParcelableArray(None)
        self.writePermission = src.readString()
        return self