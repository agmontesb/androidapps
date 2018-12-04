# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/os/PersistableBundle"""
import copy

from Android.interface.IParcelable import IParcelable, ICreator
from Android.Os.Parcel import Parcel
from BaseBundle import BaseBundle
from Android import overload


class PersistableBundle(BaseBundle, IParcelable):
    """
    A mapping from String keys to values of various types. The set of types 
    supported by this class is purposefully restricted to simple objects that 
    can safely be persisted to and restored from disk.
    """
    _fsuffixmap = { 'b': 'Byte',
                    '1': 'BooleanArray',
                    'd': 'Double',
                    '2': 'DoubleArray',
                    'i': 'Int',
                    '3': 'IntArray',
                    'l': 'Long',
                    '4': 'LongArray',
                    's': 'String',
                    '5': 'StringArray',
                    'n': '',
                    'c': 'Bundle'
                    }

    """
    public static final Creator<PersistableBundle> CREATOR:
    
    """
    CREATOR = type(
        'PersistableBundleCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: PersistableBundle(inparcel),
            'newArray': lambda self, size: (size * PersistableBundle)()
        })()

    """
    public static final PersistableBundle EMPTY:
    
    """
    EMPTY = None

    @overload
    def __init__(self):
        """
        PersistableBundle(self)
        """
        super(PersistableBundle, self).__init__()
        pass

    @__init__.adddef('int')
    def PersistableBundle(self, capacity):
        """
        PersistableBundle(self, capacity)
        :param capacity: int.
        """
        super(PersistableBundle, self).__init__()
        self._parcel.setDataCapacity(capacity)

    @__init__.adddef('PersistableBundle')
    def PersistableBundle(self, b):
        """
        PersistableBundle(self, b)
        :param b: PersistableBundle.
        """
        super(PersistableBundle, self).__init__()
        self.putAll(b)

    @__init__.adddef('Parcel')
    def PersistableBundle(self, source):
        """
        PersistableBundle(self, source)
        :param source: Parcel.
        """
        super(PersistableBundle, self).__init__()
        self._keys = source.createStringArrayList()
        self._format = source.readString()
        source.readIntArray(self._itemsize)
        parcel = bytearray(source.createByteArray())
        self._parcel.unmarshall(parcel, 0, len(parcel))

    def clone(self):
        """
        Clones the current PersistableBundle. The internal map is cloned, but 
        the keys and values to which it refers are copied by reference.
        :return: Object. a clone of this instance.
        """
        return copy.copy(self)

    def deepCopy(self):
        """
        Make a deep copy of the given bundle.  Traverses into inner containers 
        and copies them as well, so they are not shared across bundles.  Will 
        traverse in to Bundle, PersistableBundle, ArrayList, and all types of 
        primitive arrays.  Other types of objects (such as Parcelable or 
        Serializable) are referenced as-is and not copied in any way.
        :return: PersistableBundle.
        """
        return copy.deepcopy(self)

    def describeContents(self):
        """
        Report the nature of this Parcelable's contents
        :return: int. a bitmask indicating the set of special object types 
        marshaled by this Parcelable object instance.
        """
        return 0

    def getPersistableBundle(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: PersistableBundle. a Bundle value, or null
        """
        return self._readtype(key, 'c')

    def putPersistableBundle(self, key, value):
        """
        Inserts a PersistableBundle value into the mapping of this Bundle, 
        replacing any existing value for the given key.  Either key or value 
        may be null.
        :param key: String: a String, or null
        :param value: PersistableBundle: a Bundle object, or null
        """
        if not isinstance(value, self.getClass()):
            raise TypeError('Not an %s instance' % self.getClass().__name__)
        self._writetype(key, 'c', value)

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

    def writeToParcel(self, parcel, flags):
        """
        Writes the PersistableBundle contents to a Parcel, typically in order 
        for it to be passed through an IBinder connection.
        :param parcel: Parcel: The parcel to copy this bundle to.
        :param flags: int: Additional flags about how the object should be 
        written. May be 0 or Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        parcel.writeStringList(self._keys)
        parcel.writeString(self._format)
        parcel.writeIntArray(self._itemsize)
        bytes = list(self._parcel.marshall())
        parcel.writeByteArray(bytes)
