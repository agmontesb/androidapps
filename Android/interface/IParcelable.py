# -*- coding: utf-8 -*-
import abc
import ctypes

from Android import Object, AndroidArray

"""
public static final int CONTENTS_FILE_DESCRIPTOR:
Descriptor bit used with describeContents(): indicates that
the Parcelable object's flattened representation includes a file descriptor.
See also: describeContents()
"""
CONTENTS_FILE_DESCRIPTOR = 0x00000001

"""
public static final int PARCELABLE_WRITE_RETURN_VALUE:
Flag for use with writeToParcel(Parcel, int): the object being written
is a return value, that is the result of a function such as
"Parcelable someFunction()",
"void someFunction(out Parcelable)", or
"void someFunction(inout Parcelable)".  Some implementations
may want to release resources at this point.
"""
PARCELABLE_WRITE_RETURN_VALUE = 0x00000001


class IParcelableType(abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super(IParcelableType, self).__init__(*args, **kwargs)

    def __rmul__(self, size):
        class_str = self.__name__ + 'AndroidArray'
        print class_str
        return type(class_str, (AndroidArray,),
                    {'__init__': lambda x1, *args: AndroidArray.__init__(x1, self, size, args)})


class IParcelable(Object):
    __metaclass__ = IParcelableType

    @abc.abstractmethod
    def describeContents(self):
        """
        Describe the kinds of special objects contained in this Parcelable
        instance's marshaled representation.
        """
        pass

    @abc.abstractmethod
    def writeToParcel(self, dest, flags):
        """
        Flatten this object in to a Parcel.
        """
        pass


    class ICreator(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def createFromParcel(self, source):
            """
            Create a new instance of the Parcelable class, instantiating it
            from the given Parcel whose data had previously been written by
            Parcelable.writeToParcel().
            """
            pass

        @abc.abstractmethod
        def newArray(self, size):
            """
            Create a new array of the Parcelable class.
            """
            pass


    class IClassLoaderCreator(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def createFromParcel(self, source, loader):
            """
            Create a new instance of the Parcelable class, instantiating it
            from the given Parcel whose data had previously been written by
            Parcelable.writeToParcel() and
            using the given ClassLoader.
            """
            pass


