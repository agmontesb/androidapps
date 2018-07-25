# -*- coding: utf-8 -*-
import os
import Android as android
import TestActivity
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from PIL import Image
import pytest

R = TestActivity.R
context = dict(android=android.R, R=R)
res = android.Resources.Resources(context)


class TestResourceManager:
    def test_creation(self):
        packageR = res.packageR
        assert len(packageR) == 2, "packageR: Not the require size"
        assert packageR[0][0] == 'R', "packageR: The head isn't R"
        assert packageR[-1][0] == 'android', "packageR: The tail isn't android"

    def test_unpack_pointer(self):
        answ = res._unpack_pointer(R.id.create_new)
        assert isinstance(answ, tuple), "unpack_pointer: Bad response type"
        assert answ[0] == '@id/create_new', "unpack_pointer: Bad Id resource name"

        answ = res._unpack_pointer(R.layout.BasicViewsShowcase)
        assert isinstance(answ, basestring), "unpack_pointer: Bad response type"
        assert os.path.dirname(answ) == os.path.join(R.basepath, 'layout'), "unpack_pointer: Bad resource directtory"
        assert os.path.basename(answ) == 'BasicViewsShowcase.xml', "unpack_pointer: Bad resource filename"

        answ = res._unpack_pointer(R.string.file)
        assert isinstance(answ, Element), "unpack_pointer: Bad response type"
        assert answ.tag == 'string', "unpack_pointer: Bad group resource"
        assert answ.get('name') == 'file', "unpack_pointer: Bad entry resource"

    def test_reference_methods(self):
        assert res.getResourceName(R.layout.BasicViewsShowcase) == '@layout/BasicViewsShowcase', \
            "reference_methods: Bad resource name resolution"

        resid = android.R.layout.action_menu_layout
        assert res.getResourceName(resid) == '@android:layout/action_menu_layout', \
            "reference_methods: Bad resource name resolution"

        assert res.getResourcePackageName(resid) == 'android', \
            "reference_methods: Bad package name resolution"

        assert res.getResourceTypeName(resid) == 'layout', \
            "reference_methods: Bad type name resolution"

        assert res.getResourceEntryName(resid) == 'action_menu_layout', \
            "reference_methods: Bad entry name resolution"

        resid = android.R.layout.action_menu_layout
        assert res.getIdentifier('@android:layout/action_menu_layout') == resid, \
            "getIdentifier: Bad full label resolution"

        assert res.getIdentifier('@layout/action_menu_layout', defPackage='android') == resid, \
            "getIdentifier: Bad defPackage label resolution"

        resid = android.R.layout.action_menu_layout
        assert res.getIdentifier('action_menu_layout',
                                 defType='layout',
                                 defPackage='android') == resid, \
            "getIdentifier: Bad defType label resolution"

        pointer1 = res.getIdentifier('@android:style/TextAppearance.WindowTitle')
        pointer2 = android.R.style.TextAppearance__WindowTitle
        assert pointer1 == pointer2, "getIdentifier: Bad dot reference resolution"
        assert '@android:style/TextAppearance.WindowTitle' == res.getResourceName(pointer2), \
            "getIdentifier: Bad defType label resolution"

    def test_constants(self):
        resid = android.R.bool.kg_center_small_widgets_vertically
        assert res.getBoolean(resid) == False, "bool: Bad bool resolution"
        assert res.getValue(resid, None, False) == res.getBoolean(resid), \
            "getValue: Bad boolean resolution"

        resid = android.R.color.input_method_navigation_guard
        assert res.getColor(resid) == 'ff000000', "color: Bad color resolution"
        assert res.getValue(resid, None, False) == res.getColor(resid), \
            "getValue: Bad color resolution"

        with pytest.raises(LookupError) as excinfo:
            resid = android.R.color.btn_colored_text_material
            res.getColor(resid)
        assert 'Identifier not the require type' in str(excinfo.value), "color: colorstatelist id"

        resid = android.R.color.btn_colored_text_material
        assert res.getColorStateList(resid) == os.path.join(android.R.basepath, 'color', 'btn_colored_text_material.xml'), \
            "ColorStateList: Not a ColorStateList response"
        assert res.getValue(resid, None, False) == res.getColorStateList(resid), \
            "getValue: Bad color resolution"

        with pytest.raises(LookupError) as excinfo:
            resid = android.R.color.input_method_navigation_guard
            res.getColorStateList(resid)
        assert 'Identifier not the require type' in str(excinfo.value), \
            "ColorStateList: color id require"

        resid = android.R.dimen.status_bar_icon_size
        assert res.getDimension(resid) == 24, "getDimension: Bad response"
        assert res.getValue(resid, None, False) == res.getDimension(resid), \
            "getValue: Bad getDimension resolution"

        resid = android.R.fraction.config_dimBehindFadeDuration
        assert res.getFraction(resid, 6, 1) == 6.0, "getFraction: Bad response"
        assert res.getValue(resid, None, False) == res.getFraction(resid), \
            "getValue: Bad getFraction resolution"

        resid = android.R.integer.kg_carousel_angle
        assert res.getInteger(resid) == 75, "getInteger: Bad response"
        assert res.getValue(resid, None, False) == res.getInteger(resid), \
            "getValue: Bad getInteger resolution"

        resid = android.R.plurals.duration_days_relative
        assert res.getQuantityString(resid) == res.getQuantityString(resid), \
            "getQuantityString: Bad response"

        resid = android.R.string.emptyPhoneNumber
        assert res.getString(resid) == '(No phone number)', "string: Bad string resolution"
        assert res.getValue(resid, None, False) == res.getString(resid), \
            "getValue: Bad getString resolution"

    def test_arrays(self):
        resid = android.R.array.preloaded_freeform_multi_window_drawables
        assert res.obtainTypedArray(resid) == ['@drawable/decor_maximize_button_dark',
                                               '@drawable/decor_maximize_button_light'], \
            "obtainTypedArray: Bad resid resolution"
        assert res.getValue(resid, None, False) == res.obtainTypedArray(resid), \
            "getValue: Bad obtainTypedArray resolution"

        resid = android.R.array.special_locale_codes
        assert res.getStringArray(resid) == ['ar_EG', 'zh_CN', 'zh_TW'], \
            "getStringArray: Bad resid resolution"
        assert res.getValue(resid, None, False) == res.getStringArray(resid), \
            "getValue: Bad getStringArray resolution"

        resid = android.R.array.config_protectedNetworks
        assert res.getIntArray(resid) == [10, 11, 12, 14, 15], \
            "getIntArray: Bad resid resolution"
        assert res.getValue(resid, None, False) == res.getIntArray(resid), \
            "getValue: Bad getIntArray resolution"

        resid = android.R.string.alwaysUse
        answ1 = res.getString(resid)
        answ2 = res.getValueForDensity(resid, 'es', None)
        assert answ1 != answ2, "Directory Resources: resid en values/string.xml y en" \
                               "values-es/strings.xml"
        resid = android.R.string.alternate_eri_file
        answ1 = res.getString(resid)
        answ2 = res.getValueForDensity(resid, 'es', None)
        assert answ1 == answ2, "Directory Resources: resid en values/string.xml " \
                               "pero no en values-es/strings.xml"

    def test_objects(self):
        resid = android.R.drawable.ab_solid_light_holo
        gdraw = res.getDrawable(resid)
        assert isinstance(gdraw, Image.Image), \
            "getDrawable: Not an Image instance"
        vdraw = res.getValue(resid, None, False)
        assert vdraw.filename == gdraw.filename, \
            "getValue: Bad getDrawable resolution"

        resid = android.R.drawable.ab_solid_shadow_material
        gdraw = res.getDrawable(resid)
        assert isinstance(gdraw, Element), \
            "getDrawable: Not an Element instance"
        vdraw = res.getValue(resid, None, False)
        assert  vdraw.tag == gdraw.tag, \
            "getValue: Bad getDrawable resolution"

        resid = android.R.drawable.alert_dark_frame
        gdraw = res.getDrawable(resid)
        assert isinstance(gdraw, Element), \
            "getDrawable: Not an Element instance"
        assert gdraw.tag == 'drawable', "getDrawable: Not a drawable Element"
        vdraw = res.getValue(resid, None, False)
        assert  vdraw.tag == gdraw.tag, \
            "getValue: Bad getDrawable resolution"

        resid = android.R.layout.activity_list
        layout = res.getLayout(resid)
        assert isinstance(layout, Element), "getLayout: Not a layout xml file"

        resid = android.R.xml.audio_assets
        xml = res.getXml(resid)
        assert isinstance(xml, Element), "getXml: Not a xml file"

    def test_ids(self):
        resid = android.R.layout.activity_list
        layout = res.getLayout(resid)
        xmlns = dict(android='http://schemas.android.com/apk/res/android')
        idtag = '{%s}id' % xmlns['android']
        idelem = map(lambda x: res.getIdentifier(x.get(idtag)), layout.findall('./*[@android:id]', xmlns))
        assert idelem == [android.R.id.list, android.R.id.empty], \
            "test_ids: Ids in layout not defined"

    def test_obtainAtributes(self):
        resid = R.menu.file
        filename = res._unpack_pointer(resid)
        root = ET.parse(filename).getroot()
        xpath = ".//item[@id='@+id/file']"
        elem_set = root.find(xpath).attrib
        elem_arr = android.R.styleable.MenuItem
        answ = res.obtainAtributes(elem_set, elem_arr)
        answ = [x for x in answ if x is not None]
        assert answ == [R.id.file, 'File', '0', 2], "obtainAtributes: Bad resolution"
        pass


