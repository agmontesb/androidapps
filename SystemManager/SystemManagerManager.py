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

    class drawable(object):
        ic_launcher = 0x07031000
        ic_menu_mylocation = 0x07031001
        ic_menu_send = 0x07031002

    class id(object):
        installed_applications = 0x07100000
        sys_install = 0x07100001
        sys_uninstall = 0x07100002
        system = 0x07100003

    class layout(object):
        SystemLauncher = 0x07040000

    class menu(object):
        system = 0x07050000

    class string(object):
        appname = 0x07180000
        menu_system = 0x07180001
        sys_install = 0x07180002
        sys_uninstall = 0x07180003

    _valueids = {
                 0x07180000: (0x07080000, 1),
                 0x07180001: (0x07080000, 1),
                 0x07180002: (0x07080000, 1),
                 0x07180003: (0x07080000, 1),
                }

    _values_ = {
                0x07080000: 'strings',
                }

    _fext_ = ['xml', 'png']



R = ResourcePointers()
R.rid = 0x07
