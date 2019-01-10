# -*- coding: utf-8 -*-
from Android import AndroidArray
from Android.Os.Parcel import Parcel
from Android.interface.IParcelable import IParcelable



class MyParcelable(IParcelable):
    CREATOR = type('MyParcelableCreator', (IParcelable.ICreator,), {
        'createFromParcel': lambda self, inparcel: MyParcelable.readFromParcel(inparcel),
        'newArray': lambda self, size: (size * MyParcelable)()
    })()

    def __init__(self, ival=25):
        super(MyParcelable, self).__init__(ival)
        self.setData(ival)

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


def test_instantiation():
    hopi = MyParcelable()
    hopi.setData(256)

    assert isinstance(hopi, IParcelable)
    assert hopi.getData() == 256

    arrayObj = 5*MyParcelable
    assert issubclass(arrayObj, AndroidArray)
    assert arrayObj.__name__ == 'MyParcelableAndroidArray'

    arrayObj1 = arrayObj()
    initparams = [(1,), (2,), (3,), (4,), (5,)]
    arrayObj2 = arrayObj(*initparams)

    assert arrayObj1[0].getData() == arrayObj1[-1].getData() == 25
    assert all(map(lambda x: arrayObj2[x].getData() == initparams[x][0], range(5)))

def test_ReadWriteParcelable():
    hopi = MyParcelable()
    hopi.setData(256)

    parcel = Parcel()
    parcel.writeParcelable(hopi, 0)
    parcel.setDataPosition(0)

    anazazi = parcel.readParcelable(None)
    assert hopi.getData() == anazazi.getData()
    pass