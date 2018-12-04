# -*- coding: utf-8 -*-
from Android.content.ComponentName import ComponentName
from Android.Os.Parcel import Parcel

pck = 'este.es.el.package'
cls = 'este.es.el.package.esta.es.la.clase'
cname = ComponentName(pck, cls)

def test_getters():
    assert pck == cname.getPackageName(), 'ERROR: getPackageName'
    assert cls == cname.getClassName(), 'ERROR: getClassName'
    assert cname.getShortClassName() == '.esta.es.la.clase', 'ERROR: getShortClassName'

def test_info():
    assert cname.equals(cname), 'ERROR: equals'
    assert cname.flattenToString() == '%s/%s' % (pck, cls), 'ERROR: flattenToString'
    assert cname.flattenToShortString() == '%s/%s' % (pck, '.esta.es.la.clase'), 'ERROR: flattenToShortString'

def test_classmethods():
    acname = ComponentName.createRelative(pck, cname.getShortClassName())
    assert cname.equals(acname), 'ERROR: createRelative'

    parcel = Parcel()
    parcel.writeString(pck)
    parcel.writeString(cls)

    parcel.setDataPosition(0)
    acname = ComponentName.readFromParcel(parcel)
    assert cname.equals(acname), 'ERROR: readFromParcel'

    astring = cname.flattenToShortString()
    acname = ComponentName.unflattenFromString(astring)
    assert cname.equals(acname), 'ERROR: unflattenFromString'

def test_parcelable():
    parcel = Parcel()

    cname.writeToParcel(parcel,0)
    parcel.setDataPosition(0)
    acname = ComponentName.readFromParcel(parcel)
    assert cname.equals(acname), 'ERROR: No correspondence between ' \
                                 'writeToParcel and readToParcel'
    npos = parcel.dataPosition()
    parcel.writeParcelable(cname, 0)
    parcel.setDataPosition(npos)
    fparcel = parcel.readParcelable(None)

    assert cname.equals(fparcel), 'ERROR: parcelable'
