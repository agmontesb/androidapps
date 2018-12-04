# -*- coding: utf-8 -*-

import ctypes
from Android.Os.Parcel import Parcel
from Android.interface.IParcelable import IParcelable, ICreator


class MyParcelable(IParcelable):
    CREATOR = type('MyParcelableCreator', (ICreator,), {
        'createFromParcel': lambda self, inparcel: MyParcelable.readFromParcel(inparcel),
        'newArray': lambda self, size: (size * MyParcelable)()
    })()

    _fields_ = ("_mData", ctypes.c_int),

    def describeContents(self):
        return 0

    def writeToParcel(self, out, flags):
        out.writeInt(self._mData)

    @classmethod
    def readFromParcel(cls, inparcel):
        p = cls()
        p.setData(inparcel.readInt())
        return p

    def getData(self):
        return self._mData

    def setData(self, ival):
        self._mData = ival

hopi = MyParcelable()
hopi.setData(256)

parcel = Parcel()

parcel.writeParcelable(hopi, 0)

parcel.setDataPosition(0)
anazazi = parcel.readParcelable(None)


print hopi.getData(), anazazi.getData()
pass