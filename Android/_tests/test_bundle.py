# -*- coding: utf-8 -*-
from Android.Os.BaseBundle import BaseBundle
from Android.Os.PersistableBundle import PersistableBundle
from Android.Os.Bundle import Bundle
from Android.Os.Parcel import Parcel
bundle = None

def test_BaseBundle_put_get():
    global bundle
    bundle = BaseBundle()
    bundle.putBoolean('abool', True)
    bundle.putDouble('adouble', 2.5)
    bundle.putInt('anint', 72)
    bundle.putLong('along', 3L)
    bundle.putString('astring', 'esta es una string')
    assert bundle.getBoolean('abool') == True, 'ERROR: put/get boolean'
    assert bundle.getDouble('adouble') == 2.5, 'ERROR: put/get double'
    assert bundle.getInt('anint') == 72, 'ERROR: put/get int'
    assert bundle.getLong('along') == 3L, 'ERROR: put/get long'
    assert bundle.getString('astring') == 'esta es una string', \
        'ERROR: put/get string'
    assert bundle.get('adouble') == 2.5, 'ERROR: put/get generic get'
    assert bundle.get('madouble') is None, 'ERROR: put/get generic get'
    pass

def test_BaseBundle_information():
    keys = ['abool', 'adouble', 'anint', 'along', 'astring']
    assert bundle.containsKey('anint'), 'ERROR: containsKey, key in bundle'
    assert not bundle.containsKey('otherkey'), 'ERROR: containsKey, key not in bundle'
    assert not bundle.isEmpty(), 'ERROR: isEmpty, bundle not empty'
    assert not bundle.keySet().difference(keys) and not set(keys).difference(bundle.keySet()), \
        'ERROR: keySet, not all keys present'
    assert bundle.size() == len(keys), 'ERROR: size, not right size'

def test_BaseBundle_modification():
    bundle.remove('adouble')
    assert bundle.getInt('anint') == 72, 'ERROR: put/get int'
    other = BaseBundle()
    assert other.isEmpty(), 'ERROR: isEmpty'
    other.putAll(bundle)
    assert other.size() == bundle.size(), 'ERROR: putAll'
    pass

def test_PersistableBundle_iparcelable():
    abundle = PersistableBundle()
    abundle.putBoolean('abool', True)
    abundle.putDouble('adouble', 2.5)

    p = Parcel()
    abundle.writeToParcel(p, 0)
    p.setDataPosition(0)
    obj = PersistableBundle(p)
    assert abundle.equals(obj), 'ERROR: parcelable interface'

def test_PersistableBundle_put_get():
    abundle = PersistableBundle()
    abundle.putBoolean('abool', True)
    abundle.putDouble('adouble', 2.5)

    obundle = PersistableBundle()
    obundle.putInt('anint', 72)
    obundle.putLong('along', 3L)
    obundle.putString('astring', 'esta es una string')

    abundle.putPersistableBundle('abundle', obundle)
    obj = abundle.getPersistableBundle('abundle')
    assert obundle.equals(obj), 'ERROR: put/get Persistable Bundle'
    pass

def test_Bundle_iparcelable():
    abundle = Bundle()
    abundle.putBoolean('abool', True)
    abundle.putDouble('adouble', 2.5)

    p = Parcel()
    abundle.writeToParcel(p, 0)
    p.setDataPosition(0)
    obj = Bundle()
    obj.readFromParcel(p)
    assert abundle.equals(obj), 'ERROR: parcelable interface'

def test_PBundle_put_get():
    abundle = Bundle()
    abundle.putBoolean('abool', True)
    abundle.putDouble('adouble', 2.5)

    obundle = Bundle()
    obundle.putInt('anint', 72)
    obundle.putLong('along', 3L)
    obundle.putString('astring', 'esta es una string')

    abundle.putBundle('abundle', obundle)
    obj = abundle.getBundle('abundle')
    assert obundle.equals(obj), 'ERROR: put/get Persistable Bundle'
    pass

