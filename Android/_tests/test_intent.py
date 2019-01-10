# -*- coding: utf-8 -*-
from Android.Os.Parcel import Parcel
from Android.Uri import Uri
import Android.content.Intent as Intent
from Android.content.ComponentName import ComponentName


def test_GettersAndSetters():
    categories = set([Intent.CATEGORY_DEFAULT, Intent.CATEGORY_LAUNCHER])
    intent = Intent.Intent(Intent.ACTION_MAIN)
    intent.setPackage('com.example.app')
    map(intent.addCategory, categories)
    intent.setDataAndTypeAndNormalize(
        Uri.parse('content://com.example.app/users/1'),
        "text/x-vCard"
    )
    intent.setComponent(ComponentName('package.name', 'class.name'))
    intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY)
    intent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
    assert intent.getAction() == Intent.ACTION_MAIN
    assert intent.getPackage() == 'com.example.app'
    assert all(map(intent.hasCategory, categories))
    assert intent.getCategories() == categories
    assert intent.getData() == Uri.parse('content://com.example.app/users/1')
    assert intent.getDataString() == 'content://com.example.app/users/1'
    assert intent.getType() == 'text/x-vcard'
    assert intent.getComponent().equals(ComponentName('package.name', 'class.name'))
    assert intent.getScheme() == 'content'
    flags = (Intent.FLAG_ACTIVITY_CLEAR_TASK, Intent.FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY,
             Intent.FLAG_ACTIVITY_SINGLE_TOP)
    iflags = intent.getFlags()
    assert all(map(lambda x: bool(x & iflags), flags))


def test_toUri():
    packageName = 'com.example.app'
    data1 = Uri.parse('http://example.com')
    data2 = Uri.parse('http://example.com/foo?1234')
    intent = Intent.Intent(Intent.ACTION_MAIN).setPackage(packageName)
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == 'android-app://com.example.app/'

    intent = Intent\
        .Intent(Intent.ACTION_VIEW)\
        .setPackage(packageName)\
        .setData(data1)
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == \
           'android-app://com.example.app/http/example.com'

    intent = Intent\
        .Intent(Intent.ACTION_VIEW)\
        .setPackage(packageName)\
        .setData(data2)
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == \
           'android-app://com.example.app/http/example.com/foo?1234'

    intent = Intent \
        .Intent('com.example.MY_ACTION') \
        .setPackage(packageName)
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == \
           'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;end'

    intent = Intent\
        .Intent('com.example.MY_ACTION')\
        .setPackage(packageName)\
        .setData(data2)
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == \
           'android-app://com.example.app/http/example.com/foo?1234#Intent;action=com.example.MY_ACTION;end'

    intent = Intent\
        .Intent('com.example.MY_ACTION')\
        .setPackage(packageName)\
        .putExtra('some_int', 100)\
        .putExtra('some_str', 'hello')
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == \
           'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;' \
          'i.some_int=100;S.some_str=hello;end'


def test_parseUri():
    flags = Intent.URI_ANDROID_APP_SCHEME
    uri = 'android-app://com.example.app/'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == Intent.ACTION_MAIN, \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == None, \
        "parseUri: Bad data resolution"
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == uri

    uri = 'android-app://com.example.app/http/example.com'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == Intent.ACTION_VIEW, \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == Uri.parse('http://example.com'), \
        "parseUri: Bad data resolution"
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == uri

    uri = 'android-app://com.example.app/http/example.com/foo?1234'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == Intent.ACTION_VIEW, \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == Uri.parse('http://example.com/foo?1234'), \
        "parseUri: Bad data resolution"
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == uri

    uri = 'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;end'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'com.example.MY_ACTION', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == None, \
        "parseUri: Bad data resolution"
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == uri

    uri = 'android-app://com.example.app/http/example.com/foo?1234#Intent;action=com.example.MY_ACTION;end'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'com.example.MY_ACTION', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == Uri.parse('http://example.com/foo?1234'), \
        "parseUri: Bad data resolution"
    assert intent.toUri(Intent.URI_ANDROID_APP_SCHEME) == uri

    uri = 'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;' \
          'i.some_int=100;S.some_str=hello;end'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'com.example.MY_ACTION', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == None, \
        "parseUri: Bad data resolution"
    required = {'some_int':100, 'some_str':'hello'}.items()
    extras = intent.getExtras()
    assert all(map(lambda x: extras.get(x[0]) == x[1], required)), \
        "parseUri: Bad extras resolution"


def test_ClassMethods():
    normalizeMimeType = Intent.Intent.normalizeMimeType
    assert normalizeMimeType("text/plain; charset=utf-8") == "text/plain"
    assert normalizeMimeType("text/x-vCard") == "text/x-vcard"

    intent = Intent.Intent.makeMainActivity(ComponentName('com.android.exanmple', '.MainActivity'))
    assert intent.getAction() == Intent.ACTION_MAIN
    assert intent.getCategories() == set([Intent.CATEGORY_LAUNCHER])
    assert intent.getComponent().equals(ComponentName('com.android.exanmple', '.MainActivity'))

    intent = Intent.Intent.makeMainSelectorActivity('com.android.example', Intent.CATEGORY_APP_MAPS)
    assert intent.getSelector()


def test_ParcelAndUnparcel():
    uri = 'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;' \
          'i.some_int=100;S.some_str=hello;end'
    intent = Intent.Intent.parseUri(uri, Intent.URI_ANDROID_APP_SCHEME)
    intent.setData(Uri.parse('content://com.example.app/users/1'))
    p = Parcel()
    intent.writeToParcel(p, 0)
    p.setDataPosition(0)
    other = Intent.Intent.CREATOR.createFromParcel(p)
    assert intent.getAction() == other.getAction()
    assert intent.getData() == other.getData()
    assert intent.getType() == other.getType()
    assert intent.getFlags() == other.getFlags()
    assert intent.getComponent() == other.getComponent()
    assert intent.getSourceBounds() == other.getSourceBounds()
    assert intent.getCategories() == other.getCategories()
    assert intent.getClipData() == other.getClipData()

def test_selector():
    uri = 'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;' \
          'i.some_int=100;S.some_str=hello;end'
    intent = Intent.Intent.parseUri(uri, Intent.URI_ANDROID_APP_SCHEME)
    intent.setDataAndTypeAndNormalize(
        Uri.parse('content://com.example.app/users/1'),
        "text/x-vCard"
    )
    clone = intent.clone()
    filter = intent.cloneFilter()

    assert intent.filterEquals(clone)
    assert intent.filterEquals(filter)
    assert clone.filterEquals(filter)

    other = Intent.Intent(Intent.ACTION_VIEW)\
        .setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP|Intent.FLAG_ACTIVITY_CLEAR_TASK)

    assert filter.getFlags() == 0
    filter.fillIn(other, 0)
    assert filter.getFlags() == other.getFlags()
    filter.fillIn(other, Intent.FILL_IN_ACTION)
    assert filter.getAction() == other.getAction()







