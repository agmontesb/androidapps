# -*- coding: utf-8 -*-
import os
from Android.content.res.Resources import Pointers


class ResourcePointers(Pointers):    
    @property
    def basepath(cls):
        basepath = os.path.dirname(__file__)
        relPathToResDirectory = r'res'
        respath = os.path.join(basepath, relPathToResDirectory)
        return os.path.realpath(respath)

    class attr(object):
        default = 0x04150003
        enable = 0x04150004
        group = 0x04150007
        label = 0x04150003
        lib = 0x04150001
        lvalues = 0x04150008
        scrolled = 0x04150006
        side = 0x04150005
        type = 0x04150002
        values = 0x04150009

    class color(object):
        black = 0x040e0001
        green = 0x040e0000

    class drawable(object):
        ic_menu_mylocation = 0x04031000
        ic_menu_send = 0x04031001

    class id(object):
        addon_action = 0x04100000
        addon_audio = 0x04100001
        addon_bool = 0x04100002
        addon_dropdown = 0x04100003
        addon_enum = 0x04100004
        addon_executable = 0x04100005
        addon_file = 0x04100006
        addon_fileenum = 0x04100007
        addon_folder = 0x04100008
        addon_image = 0x04100009
        addon_ipaddress = 0x0410000a
        addon_labelenum = 0x0410000b
        addon_number = 0x0410000c
        addon_optionlst = 0x0410000d
        addon_slider = 0x0410000e
        addon_text = 0x0410000f
        addon_video = 0x04100010
        bgbool1 = 0x04100011
        bgbool2 = 0x04100012
        bgbool3 = 0x04100013
        cascade = 0x04100014
        cascade1 = 0x04100015
        cascade2 = 0x04100016
        cascade21 = 0x04100017
        cascade22 = 0x04100018
        cascade3 = 0x04100019
        create_new = 0x0410001a
        details_apellido1 = 0x0410001b
        details_apellido2 = 0x0410001c
        details_celular = 0x0410001d
        details_edad = 0x0410001e
        details_nombre = 0x0410001f
        f_details = 0x04100020
        f_titles = 0x04100021
        file = 0x04100022
        grp1 = 0x04100023
        grp2 = 0x04100024
        open = 0x04100025
        save = 0x04100026
        save_as = 0x04100027
        scrolledlist = 0x04100028
        tcontainer = 0x04100029
        ttbool1 = 0x0410002a
        ttbool2 = 0x0410002b
        tttexto1 = 0x0410002c
        tttexto2 = 0x0410002d

    class layout(object):
        BasicViewsShowcase = 0x04040000
        basicWidets = 0x04040001
        detailsfragment = 0x04040002
        fragment_layout = 0x04040003
        listfragment = 0x04040004
        titlesfragment = 0x04040005

    class menu(object):
        file = 0x04050000

    class mipmap(object):
        ic_launcher = 0x04061000
        ic_launcher_foreground = 0x04061001
        ic_launcher_round = 0x04061002

    class string(object):
        cascade = 0x04180005
        cascade1 = 0x04180006
        cascade2 = 0x04180007
        cascade21 = 0x04180009
        cascade22 = 0x0418000a
        cascade3 = 0x04180008
        create_new = 0x04180001
        file = 0x04180000
        open = 0x04180002
        save = 0x04180003
        save_as = 0x04180004

    class style(object):
        submitButton = 0x04160000

    class styleable(object):
        category = [0x04150003, 0x04150001]
        category_label = 0
        category_lib = 1
        setting = ['@android:attr/id', 0x04150002, 0x04150003, 0x04150003, 0x04150004, 0x04150005, 0x04150006, 0x04150007, 0x04150008, 0x04150009]
        setting_android_id = 0
        setting_type = 1
        setting_label = 2
        setting_default = 3
        setting_enable = 4
        setting_side = 5
        setting_scrolled = 6
        setting_group = 7
        setting_lvalues = 8
        setting_values = 9

    _valueids = {
                 0x040e0000: (0x04080001, 1),
                 0x040e0001: (0x04080001, 1),
                 0x04150000: (0x04080000, 0),
                 0x04150001: (0x04080000, 1),
                 0x04150002: (0x04080000, 3),
                 0x04150003: (0x04080000, 5),
                 0x04150004: (0x04080000, 6),
                 0x04150005: (0x04080000, 7),
                 0x04150006: (0x04080000, 8),
                 0x04150007: (0x04080000, 9),
                 0x04150008: (0x04080000, 10),
                 0x04150009: (0x04080000, 11),
                 0x04160000: (0x04080003, 1),
                 0x04180000: (0x04080002, 1),
                 0x04180001: (0x04080002, 1),
                 0x04180002: (0x04080002, 1),
                 0x04180003: (0x04080002, 1),
                 0x04180004: (0x04080002, 1),
                 0x04180005: (0x04080002, 1),
                 0x04180006: (0x04080002, 1),
                 0x04180007: (0x04080002, 1),
                 0x04180008: (0x04080002, 1),
                 0x04180009: (0x04080002, 1),
                 0x0418000a: (0x04080002, 1),
                }

    _values_ = {
                0x04080000: 'attrs',
                0x04080001: 'colors',
                0x04080002: 'strings',
                0x04080003: 'styles',
                }

    _fext_ = ['xml', 'png']



R = ResourcePointers()
R.rid = 0x04
