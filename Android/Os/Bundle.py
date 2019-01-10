# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/os/Bundle"""
import copy

from Android.interface.IParcelable import IParcelable
from Android.Os.Parcel import Parcel
from BaseBundle import BaseBundle
from Android import overload, Object


class Bundle(BaseBundle, IParcelable):
    """
    A mapping from String keys to various Parcelable values.
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
                    'f': 'Float',
                    '6': 'FloatArray',
                    'n': '',
                    'c': 'Bundle',
                    'p': 'Parcelable'
                    }
    """
    public static final Creator<Bundle> CREATOR:
    
    """
    CREATOR = type(
        'PersistableBundleCreator',
        (IParcelable.ICreator,), {
            'createFromParcel': lambda self, inparcel: Bundle().readFromParcel(inparcel),
            'newArray': lambda self, size: (size * Bundle)()
        })()

    """
    public static final Bundle EMPTY:
    
    """
    EMPTY = None

    @overload
    def __init__(self):
        super(Bundle, self).__init__()
        pass

    @__init__.adddef('ClassLoader')
    def Bundle(self, loader):
        """
        :param loader: ClassLoader.
        """
        pass

    @__init__.adddef('int')
    def Bundle(self, capacity):
        """
        :param capacity: int.
        """
        super(Bundle, self).__init__()
        self._parcel.setDataCapacity(capacity)


    @__init__.adddef('Bundle')
    def Bundle(self, b):
        """
        :param b: Bundle.
        """
        super(Bundle, self).__init__()
        self.putAll(b)

    @__init__.adddef('PersistableBundle')
    def Bundle(self, b):
        """
        :param b: PersistableBundle.
        """
        super(Bundle, self).__init__()
        self.putAll(b)

    def clear(self):
        """
        Removes all elements from the mapping of this Bundle.
        """
        super(Bundle, self).clear()
        pass

    def clone(self):
        """
        Clones the current Bundle. The internal map is cloned, but the keys 
        and values to which it refers are copied by reference.
        :return: Object. a clone of this instance.
        """
        copy.copy(self)

    def deepCopy(self):
        """
        Make a deep copy of the given bundle.  Traverses into inner containers 
        and copies them as well, so they are not shared across bundles.  Will 
        traverse in to Bundle, PersistableBundle, ArrayList, and all types of 
        primitive arrays.  Other types of objects (such as Parcelable or 
        Serializable) are referenced as-is and not copied in any way.
        :return: Bundle.
        """
        copy.deepcopy(self)

    def describeContents(self):
        """
        Report the nature of this Parcelable's contents
        :return: int. a bitmask indicating the set of special object types 
        marshaled by this Parcelable object instance.
        """
        return 0

    def getBinder(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: IBinder. an IBinder value, or null
        """
        pass

    def getBundle(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: Bundle. a Bundle value, or null
        """
        return self._readtype(key, 'c')

    def getByte(self, key, defaultValue=0):
        """
        Returns the value associated with the given key, or defaultValue if no 
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: byte: Value to return if key does not exist
        :return: Byte. a byte value
        """
        return self._readtype(key, 'b', defaultValue)

    def getByteArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: byte[]. a byte[] value, or null
        """
        return self._readtype(key, '1')

    def getChar(self, key, defaultValue=0):
        """
        Returns the value associated with the given key, or defaultValue if no 
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: char: Value to return if key does not exist
        :return: char. a char value
        """
        pass

    def getCharArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: char[]. a char[] value, or null
        """
        pass

    def getCharSequence(self, key, defaultValue=None):
        """
        Returns the value associated with the given key, or defaultValue if no 
        mapping of the desired type exists for the given key or if a null 
        value is explicitly associatd with the given key.
        :param key: String: a String, or null
        :param defaultValue: CharSequence: Value to return if key does not 
        exist or if a null value is associated with the given key.
        :return: CharSequence. the CharSequence value associated with the 
        given key, or defaultValue if no valid CharSequence object is 
        currently mapped to that key.
        """
        pass

    def getCharSequenceArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: CharSequence[]. a CharSequence[] value, or null
        """
        pass

    def getCharSequenceArrayList(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: ArrayList<CharSequence>. an ArrayList value, or null
        """
        pass

    def getClassLoader(self):
        """
        Return the ClassLoader currently associated with this Bundle.
        :return: ClassLoader.
        """
        pass

    def getFloat(self, key, defaultValue=0.0):
        """
        Returns the value associated with the given key, or defaultValue if no 
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: float: Value to return if key does not exist
        :return: float. a float value
        """
        return self._readtype(key, 'f', defaultValue)

    def getFloatArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: float[]. a float[] value, or null
        """
        return self._readtype(key, '6')

    def getIntegerArrayList(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: ArrayList<Integer>. an ArrayList value, or null
        """
        pass

    def getParcelable(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: T. a Parcelable value, or null
        """
        return self._readtype(key, 'p')

    def getParcelableArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: Parcelable[]. a Parcelable[] value, or null
        """
        pass

    def getParcelableArrayList(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: ArrayList<T>. an ArrayList value, or null
        """
        pass

    def getSerializable(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: Serializable. a Serializable value, or null
        """
        pass

    def getShort(self, key):
        """
        Returns the value associated with the given key, or (short) 0 if no 
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :return: short. a short value
        """
        pass

    def getShort(self, key, defaultValue):
        """
        Returns the value associated with the given key, or defaultValue if no 
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: short: Value to return if key does not exist
        :return: short. a short value
        """
        pass

    def getShortArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: short[]. a short[] value, or null
        """
        pass

    def getSize(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: Size. a Size value, or null
        """
        pass

    def getSizeF(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: SizeF. a Size value, or null
        """
        pass

    def getSparseParcelableArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: SparseArray<T>. a SparseArray of T values, or null
        """
        pass

    def getStringArrayList(self, key):
        """
        Returns the value associated with the given key, or null if no mapping 
        of the desired type exists for the given key or a null value is 
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: ArrayList<String>. an ArrayList value, or null
        """
        pass

    def hasFileDescriptors(self):
        """
        Reports whether the bundle contains any parcelled file descriptors.
        :return: boolean.
        """
        pass

    def putAll(self, bundle):
        """
        Inserts all mappings from the given Bundle into this Bundle.
        :param bundle: Bundle: a Bundle
        """
        super(Bundle, self).putAll(bundle)

    def putBinder(self, key, value):
        """
        Inserts an IBinder value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be 
        null.  You should be very careful when using this function.  In many 
        places where Bundles are used (such as inside of Intent objects), the 
        Bundle can live longer inside of another process than the process that 
        had originally created it.  In that case, the IBinder you supply here 
        will become invalid when your process goes away, and no longer usable, 
        even if a new process is created for you later on.
        :param key: String: a String, or null
        :param value: IBinder: an IBinder object, or null
        """
        pass

    def putBundle(self, key, value):
        """
        Inserts a Bundle value into the mapping of this Bundle, replacing any 
        existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: Bundle: a Bundle object, or null
        """
        if not isinstance(value, self.getClass()):
            raise TypeError('Not an %s instance' % self.getClass().__name__)
        self._writetype(key, 'c', value)

    def putByte(self, key, value):
        """
        Inserts a byte value into the mapping of this Bundle, replacing any 
        existing value for the given key.
        :param key: String: a String, or null
        :param value: byte: a byte
        """
        self._writetype(key, 'b', value)

    def putByteArray(self, key, value):
        """
        Inserts a byte array value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: byte: a byte array object, or null
        """
        self._writetype(key, '1', value)

    def putChar(self, key, value):
        """
        Inserts a char value into the mapping of this Bundle, replacing any 
        existing value for the given key.
        :param key: String: a String, or null
        :param value: char: a char
        """
        pass

    def putCharArray(self, key, value):
        """
        Inserts a char array value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: char: a char array object, or null
        """
        pass

    def putCharSequence(self, key, value):
        """
        Inserts a CharSequence value into the mapping of this Bundle, 
        replacing any existing value for the given key.  Either key or value 
        may be null.
        :param key: String: a String, or null
        :param value: CharSequence: a CharSequence, or null
        """
        pass

    def putCharSequenceArray(self, key, value):
        """
        Inserts a CharSequence array value into the mapping of this Bundle, 
        replacing any existing value for the given key.  Either key or value 
        may be null.
        :param key: String: a String, or null
        :param value: CharSequence: a CharSequence array object, or null
        """
        pass

    def putCharSequenceArrayList(self, key, value):
        """
        Inserts an ArrayList value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: ArrayList: an ArrayList object, or null
        """
        pass

    def putFloat(self, key, value):
        """
        Inserts a float value into the mapping of this Bundle, replacing any 
        existing value for the given key.
        :param key: String: a String, or null
        :param value: float: a float
        """
        pass

    def putFloatArray(self, key, value):
        """
        Inserts a float array value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: float: a float array object, or null
        """
        pass

    def putIntegerArrayList(self, key, value):
        """
        Inserts an ArrayList value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: ArrayList: an ArrayList object, or null
        """
        pass

    def putParcelable(self, key, value):
        """
        Inserts a Parcelable value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: Parcelable: a Parcelable object, or null
        """
        self._writetype(key, 'p', value, 0)

    def putParcelableArray(self, key, value):
        """
        Inserts an array of Parcelable values into the mapping of this Bundle, 
        replacing any existing value for the given key.  Either key or value 
        may be null.
        :param key: String: a String, or null
        :param value: Parcelable: an array of Parcelable objects, or null
        """
        pass

    def putParcelableArrayList(self, key, value):
        """
        Inserts a List of Parcelable values into the mapping of this Bundle, 
        replacing any existing value for the given key.  Either key or value 
        may be null.
        :param key: String: a String, or null
        :param value: ArrayList: an ArrayList of Parcelable objects, or null
        """
        pass

    def putSerializable(self, key, value):
        """
        Inserts a Serializable value into the mapping of this Bundle, 
        replacing any existing value for the given key.  Either key or value 
        may be null.
        :param key: String: a String, or null
        :param value: Serializable: a Serializable object, or null
        """
        pass

    def putShort(self, key, value):
        """
        Inserts a short value into the mapping of this Bundle, replacing any 
        existing value for the given key.
        :param key: String: a String, or null
        :param value: short: a short
        """
        pass

    def putShortArray(self, key, value):
        """
        Inserts a short array value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: short: a short array object, or null
        """
        pass

    def putSize(self, key, value):
        """
        Inserts a Size value into the mapping of this Bundle, replacing any 
        existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: Size: a Size object, or null
        """
        pass

    def putSizeF(self, key, value):
        """
        Inserts a SizeF value into the mapping of this Bundle, replacing any 
        existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: SizeF: a SizeF object, or null
        """
        pass

    def putSparseParcelableArray(self, key, value):
        """
        Inserts a SparceArray of Parcelable values into the mapping of this 
        Bundle, replacing any existing value for the given key.  Either key or 
        value may be null.
        :param key: String: a String, or null
        :param value: SparseArray: a SparseArray of Parcelable objects, or null
        """
        pass

    def putStringArrayList(self, key, value):
        """
        Inserts an ArrayList value into the mapping of this Bundle, replacing 
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: ArrayList: an ArrayList object, or null
        """
        pass

    def readFromParcel(self, parcel):
        """
        Reads the Parcel contents into this Bundle, typically in order for it 
        to be passed through an IBinder connection.
        :param parcel: Parcel: The parcel to overwrite this bundle from.
        """
        self._keys = parcel.createStringArrayList()
        self._format = parcel.readString()
        self._itemsize = list(parcel.createIntArray())
        aparcel = bytearray(parcel.createByteArray())
        self._parcel.unmarshall(aparcel, 0, len(aparcel))
        return self

    def remove(self, key):
        """
        Removes any entry with the given key from the mapping of this Bundle.
        :param key: String: a String key
        """
        pass

    def setClassLoader(self, loader):
        """
        Changes the ClassLoader this Bundle uses when instantiating objects.
        :param loader: ClassLoader: An explicit ClassLoader to use when 
        instantiating objects inside of the Bundle.
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

    def writeToParcel(self, parcel, flags):
        """
        Writes the Bundle contents to a Parcel, typically in order for it to 
        be passed through an IBinder connection.
        :param parcel: Parcel: The parcel to copy this bundle to.
        :param flags: int: Additional flags about how the object should be 
        written. May be 0 or Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        parcel.writeStringList(self._keys)
        parcel.writeString(self._format)
        parcel.writeIntArray(self._itemsize)
        bytes = bytearray(self._parcel.marshall())
        parcel.writeByteArray(bytes, 0, self._parcel.dataSize())


Bundle.EMPTY = Bundle()