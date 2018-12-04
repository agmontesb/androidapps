# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/os/BaseBundle"""
import Android
from Parcel import Parcel

class BaseBundle(Android.Object):
    """
    A mapping from String keys to values of various types. In most cases, you 
    should work directly with either the Bundle or PersistableBundle subclass.
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
                    }

    def __init__(self, *args):
        super(BaseBundle, self).__init__(*args)
        self._keys = []
        self._format = ''
        self._itemsize = []
        self._parcel = Parcel()

    def _readtype(self, key, dtype, defaulvalue=None):
        try:
            npos = self._keys.index(key)
        except:
            pass
        else:
            vtype = self._format[npos]
            if dtype is None or vtype == dtype:
                fname = 'read' + self._fsuffixmap[vtype]
                func = getattr(self._parcel, fname)
                offset = sum(self._itemsize[:npos])
                self._parcel.setDataPosition(offset)
                if vtype == 'p':
                    return func(None)
                return func()
        return defaulvalue

    def _writetype(self, key, dtype, *value):
        if key is None: return
        self.remove(key)
        offset = self._parcel.dataSize()
        if value is None and dtype != 'p':
            if dtype.isdigit():
                dtype = 'n'
            else:
                raise Exception('None type not allowed')
        else:
            fname = 'write' + self._fsuffixmap[dtype]
            func = getattr(self._parcel, fname)
            self._parcel.setDataPosition(offset)
            func(*value)
        self._keys.append(key)
        self._itemsize.append(self._parcel.dataSize() - offset)
        self._format += dtype

    def clear(self):
        """
        Removes all elements from the mapping of this Bundle.
        """
        self._keys = []
        self._format = ''
        self._itemsize = []
        self._parcel = Parcel()
        pass

    def containsKey(self, key):
        """
        Returns true if the given key is contained in the mapping of this
        Bundle.
        :param key: String: a String key
        :return: boolean. true if the key is part of the mapping, false
        otherwise
        """
        return key in self._keys

    def get(self, key):
        """
        Returns the entry with the given key as an object.
        :param key: String: a String key
        :return: Object. an Object, or null
        """
        return self._readtype(key, None)

    def getBoolean(self, key, defaultValue=False):
        """
        Returns the value associated with the given key, or defaultValue if no
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: boolean: Value to return if key does not exist
        :return: boolean. a boolean value
        """
        return self._readtype(key, 'b', defaultValue)

    def getBooleanArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping
        of the desired type exists for the given key or a null value is
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: boolean[]. a boolean[] value, or null
        """
        return self._readtype(key, '1')

    def getDouble(self, key, defaultValue=0.0):
        """
        Returns the value associated with the given key, or defaultValue if no
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: double: Value to return if key does not exist
        :return: double. a double value
        """
        return self._readtype(key, 'd', defaultValue)

    def getDoubleArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping
        of the desired type exists for the given key or a null value is
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: double[]. a double[] value, or null
        """
        return self._readtype(key, '2')

    def getInt(self, key, defaultValue=0):
        """
        Returns the value associated with the given key, or defaultValue if no
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: int: Value to return if key does not exist
        :return: int. an int value
        """
        return self._readtype(key, 'i', defaultValue)

    def getIntArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping
        of the desired type exists for the given key or a null value is
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: int[]. an int[] value, or null
        """
        return self._readtype(key, '3')

    def getLong(self, key, defaultValue=0L):
        """
        Returns the value associated with the given key, or defaultValue if no
        mapping of the desired type exists for the given key.
        :param key: String: a String
        :param defaultValue: long: Value to return if key does not exist
        :return: long. a long value
        """
        return self._readtype(key, 'l', defaultValue)

    def getLongArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping
        of the desired type exists for the given key or a null value is
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: long[]. a long[] value, or null
        """
        return self._readtype(key, '4')

    def getString(self, key, defaultValue=None):
        """
        Returns the value associated with the given key, or defaultValue if no
        mapping of the desired type exists for the given key or if a null
        value is explicitly associated with the given key.
        :param key: String: a String, or null
        :param defaultValue: String: Value to return if key does not exist or
        if a null value is associated with the given key.
        :return: String. the String value associated with the given key, or
        defaultValue if no valid String object is currently mapped to that key.
        """
        return self._readtype(key, 's', defaultValue)

    def getStringArray(self, key):
        """
        Returns the value associated with the given key, or null if no mapping
        of the desired type exists for the given key or a null value is
        explicitly associated with the key.
        :param key: String: a String, or null
        :return: String[]. a String[] value, or null
        """
        return self._readtype(key, '5')

    def isEmpty(self):
        """
        Returns true if the mapping of this Bundle is empty, false otherwise.
        :return: boolean.
        """
        return not bool(self.size())

    def keySet(self):
        """
        Returns a Set containing the Strings used as keys in this Bundle.
        :return: Set<String>. a Set of String keys
        """
        return set(self._keys)

    def putAll(self, bundle):
        """
        Inserts all mappings from the given PersistableBundle into this
        BaseBundle.
        :param bundle: PersistableBundle: a PersistableBundle
        """
        for k, key in enumerate(bundle._keys):
            self._writetype(key, bundle._format[k], bundle.get(key))

    def putBoolean(self, key, value):
        """
        Inserts a Boolean value into the mapping of this Bundle, replacing any
        existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: boolean: a boolean
        """
        self._writetype(key, 'b', value)

    def putBooleanArray(self, key, value):
        """
        Inserts a boolean array value into the mapping of this Bundle,
        replacing any existing value for the given key.  Either key or value
        may be null.
        :param key: String: a String, or null
        :param value: boolean: a boolean array object, or null
        """
        self._writetype(key, '1', value)

    def putDouble(self, key, value):
        """
        Inserts a double value into the mapping of this Bundle, replacing any
        existing value for the given key.
        :param key: String: a String, or null
        :param value: double: a double
        """
        self._writetype(key, 'd', value)

    def putDoubleArray(self, key, value):
        """
        Inserts a double array value into the mapping of this Bundle,
        replacing any existing value for the given key.  Either key or value
        may be null.
        :param key: String: a String, or null
        :param value: double: a double array object, or null
        """
        self._writetype(key, '2', value)

    def putInt(self, key, value):
        """
        Inserts an int value into the mapping of this Bundle, replacing any
        existing value for the given key.
        :param key: String: a String, or null
        :param value: int: an int
        """
        self._writetype(key, 'i', value)

    def putIntArray(self, key, value):
        """
        Inserts an int array value into the mapping of this Bundle, replacing
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: int: an int array object, or null
        """
        self._writetype(key, '3', value)

    def putLong(self, key, value):
        """
        Inserts a long value into the mapping of this Bundle, replacing any
        existing value for the given key.
        :param key: String: a String, or null
        :param value: long: a long
        """
        self._writetype(key, 'l', value)

    def putLongArray(self, key, value):
        """
        Inserts a long array value into the mapping of this Bundle, replacing
        any existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: long: a long array object, or null
        """
        self._writetype(key, '4', value)

    def putString(self, key, value):
        """
        Inserts a String value into the mapping of this Bundle, replacing any
        existing value for the given key.  Either key or value may be null.
        :param key: String: a String, or null
        :param value: String: a String, or null
        """
        self._writetype(key, 's', value)

    def putStringArray(self, key, value):
        """
        Inserts a String array value into the mapping of this Bundle,
        replacing any existing value for the given key.  Either key or value
        may be null.
        :param key: String: a String, or null
        :param value: String: a String array object, or null
        """
        self._writetype(key, '5', value)

    def remove(self, key):
        """
        Removes any entry with the given key from the mapping of this Bundle.
        :param key: String: a String key
        """
        if not self.containsKey(key): return
        npos = self._keys.index(key)
        buffer = self._parcel.marshall()
        offset = sum(self._itemsize[:npos])
        size = self._itemsize[npos]
        length = self._parcel.dataSize() - offset - size
        self._parcel.setDataPosition(offset)
        self._parcel.appendFrom(self._parcel, offset + size, length)
        self._format = self._format[:npos] + self._format[npos+1:]
        self._keys = self._keys[:npos] + self._keys[npos+1:]
        self._itemsize = self._itemsize[:npos] + self._itemsize[npos+1:]

    def size(self):
        """
        Returns the number of mappings contained in this Bundle.
        :return: int. the number of mappings as an int.
        """
        return len(self._keys)

    def equals(self, obj):
        npos = self._parcel.dataSize()
        return self._keys == obj._keys and \
               self._format == obj._format and \
               self._itemsize == obj._itemsize and \
               self._parcel._buffer[:npos] == obj._parcel._buffer[:npos]

