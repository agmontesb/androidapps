# -*- coding: utf-8 -*-
import random
import pytest

from Android import Object, overload
from Android.Os.Parcel import Parcel
from Android.interface.IParcelable import IParcelable, ICreator
from Android.Os.PersistableBundle import PersistableBundle
from Android.Os.Bundle import Bundle


class MyParcelable(Object, IParcelable):
    CREATOR = type(
        'MyParcelableCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: MyParcelable(inparcel),
            'newArray': lambda self, size: (size * MyParcelable)()
        })()

    @overload
    def __init__(self):
        super(MyParcelable, self).__init__()
        self.uno = -1
        self.dos = ''

    @__init__.adddef('int', 'str')
    def __init__(self, uno, dos):
        super(MyParcelable, self).__init__()
        self.uno = uno
        self.dos = dos

    @__init__.adddef('Parcel')
    def MyParcelable(self, parcel):
        super(MyParcelable, self).__init__()
        self.uno = parcel.readInt()
        self.dos = parcel.readString()

    def writeToParcel(self, dest, flags):
        dest.writeInt(self.uno)
        dest.writeString(self.dos)

    def equals(self, obj):
        return self.uno == obj.uno and self.dos == obj.dos


primitives = [('byte', 2),
              ('double', 22.54),
              ('float', 22.54),
              ('int', 40),
              ('long', 2348),
              ('string', 'prueba y error para completar un bloque de datos'),
              ]
random.shuffle(primitives)

@pytest.fixture
def parcel():
    p = Parcel()
    for datatype, value in primitives:
        datatype = datatype.title()
        writemethod = 'write' + datatype
        writemethod = getattr(p, writemethod)
        writemethod(value)
    p.setDataPosition(0)
    return p

@pytest.fixture
def parcelofarray():
    p = Parcel()
    for datatype, value in primitives:
        datatype = datatype.title()
        value = 5*[value]
        writemethod = 'write%sArray' % datatype
        writemethod = getattr(p, writemethod)
        writemethod(value)
    p.setDataPosition(0)
    return p


def test_primitives(parcel):
    for datatype, value in primitives:
        datatype = datatype.title()
        readmethod = 'read' + datatype
        readmethod = getattr(parcel, readmethod)
        ret = readmethod()
        if datatype in ['Double', 'Float']:
            bFlag = ret - value < 0.01
        else:
            bFlag = ret == value
        assert bFlag, 'Error primitives: %s' % datatype


def test_marshallunmarshall(parcel):
    marshall = parcel.marshall()
    q = Parcel()
    q.unmarshall(marshall, 0, len(marshall))
    q.setDataPosition(0)
    test_primitives(q)
    pass

def test_appendFrom(parcel):
    q = Parcel()
    q.appendFrom(parcel, 0, parcel.dataSize())
    q.setDataPosition(0)
    test_primitives(q)
    pass


def test_primitivesArray(parcelofarray):
    for datatype, value in primitives:
        datatype = datatype.title()
        value = 5*[value]
        answ = 5*[0]
        readmethod = 'read%sArray' % datatype
        readmethod = getattr(parcelofarray, readmethod)
        readmethod(answ)
        if datatype in ['Double', 'Float']:
            trnf = lambda x: abs(x[0] - x[1]) < 0.01
        else:
            trnf = lambda x: x[0] == x[1]
        assert all(map(trnf, zip(answ, value))), 'Error primitives: %s' % readmethod.__name__


def test_parcelables():
    strVars = ['zero', 'one', 'two', 'three']
    parcelableList = map(lambda x: MyParcelable(*x), enumerate(strVars))
    aparcelable = parcelableList[0]
    p = Parcel()
    p.writeTypedObject(aparcelable, 0)
    p.writeTypedArray(parcelableList, 0)
    p.writeTypedList(parcelableList)
    p.setDataPosition(0)
    q = p.readTypedObject(MyParcelable.CREATOR)
    qa = p.createTypedArray(MyParcelable.CREATOR)
    ql = p.createTypedArrayList(MyParcelable.CREATOR)
    assert aparcelable.equals(q), "Error TypedObject: Read and write Typed object"
    assert all(map(lambda x: x[0].equals(x[1]), zip(parcelableList, ql))), "ERROR createTypedArrayList"
    assert all(map(lambda x: x[0].equals(x[1]), zip(parcelableList, qa))), "ERROR createTypedArray"

    p = Parcel()
    p.writeParcelable(aparcelable, 0)
    p.writeParcelable(aparcelable, 0)
    p.writeParcelableArray(parcelableList, 0)
    p.setDataPosition(0)

    q = p.readParcelable(None)
    w = p.readParcelable('test_parcel.MyParcelable')
    qa = p.readParcelableArray(None)
    assert aparcelable.equals(q), "ERROR write/readParcelable"
    assert aparcelable.equals(w), "ERROR write/readParcelable"
    assert all(map(lambda x: x[0].equals(x[1]), zip(parcelableList, qa))), "ERROR createTypedArrayList"
    pass

def test_bundles():
    pBundle = PersistableBundle()
    pBundle.putBoolean('boolean', True)
    pBundle.putInt('integer', 234)
    pBundle.putString('string', 'esta es una string')

    p = Parcel()
    p.writePersistableBundle(pBundle)
    p.setDataPosition(0)
    qBundle = p.readPersistableBundle()
    assert pBundle.equals(qBundle), "ERROR: read/writePersistableBundle"

def test_untypedcontainers(parcel):
    p = Parcel()
    keys, values = zip(*primitives)
    map(lambda x: p.writeValue(x), values)
    p.writeArray(values)
    p.writeList(values)
    p.setDataPosition(0)
    q = map(lambda x: p.readValue(None), range(len(keys)))
    qa = p.readArray(None)
    ql = len(values)*[0]
    p.readList(ql, None)
    for anArray in [q, qa, ql]:
        for k, key in enumerate(keys):
            if key in ['double', 'float']:
                bFlag = abs(values[k] - anArray[k]) < 0.01
            else:
                bFlag = values[k] == anArray[k]
            assert bFlag, 'Error read/writeArray: %s' % key

    aMap = dict(uno=1, dos=2.5, tres='parejas cruzadas')
    p = Parcel()
    p.writeMap(aMap)
    p.setDataPosition(0)
    q = {}
    p.readMap(q, None)
    assert aMap == q, "ERROR read/writeMap"

