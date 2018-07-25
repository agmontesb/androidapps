# -*- coding: utf-8 -*-
import pytest
import Android.Intent as Intent


def test_parseUri():
    flags = Intent.URI_ANDROID_APP_SCHEME
    uri = 'android-app://com.example.app/'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'android.intent.action.MAIN', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == None, \
        "parseUri: Bad data resolution"

    uri = 'android-app://com.example.app/http/example.com'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'android.intent.action.VIEW', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == 'http://example.com', \
        "parseUri: Bad data resolution"

    uri = 'android-app://com.example.app/http/example.com/foo?1234'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'android.intent.action.VIEW', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == 'http://example.com/foo?1234', \
        "parseUri: Bad data resolution"

    uri = 'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;end'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'com.example.MY_ACTION', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == None, \
        "parseUri: Bad data resolution"

    uri = 'android-app://com.example.app/http/example.com/foo?1234#Intent;action=com.example.MY_ACTION;end'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'com.example.MY_ACTION', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == 'http://example.com/foo?1234', \
        "parseUri: Bad data resolution"

    uri = 'android-app://com.example.app/#Intent;action=com.example.MY_ACTION;' \
          'i.some_int=100;S.some_str=hello;end'
    intent = Intent.Intent.parseUri(uri, flags)
    assert intent.getAction() == 'com.example.MY_ACTION', \
        "parseUri: Bad action resolution"
    assert intent.getPackage() == 'com.example.app', \
        "parseUri: Bad package resolution"
    assert intent.getData() == None, \
        "parseUri: Bad data resolution"
    assert intent.getExtras() == {'some_int':100, 'some_str':'hello'}, \
        "parseUri: Bad extras resolution"
    # Acá la igualdad se da por chiripa porque los extras son un diccionario
    assert uri == intent.toURI(flags), "toURI: Bad URI resolution"
