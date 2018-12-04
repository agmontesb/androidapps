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

    class id(object):
        actualizarBD = 0x06100000
        analisisDiario = 0x06100001
        aniofecha = 0x06100002
        copiaTexto = 0x06100003
        datosProcesar = 0x06100004
        diafecha = 0x06100005
        eodtable = 0x06100006
        fechaProceso = 0x06100007
        fuenteDatos = 0x06100008
        getData = 0x06100009
        intradiatable = 0x0610000a
        mesfecha = 0x0610000b
        messageBoard = 0x0610000c

    class layout(object):
        DatosEod = 0x06040000
        MainActivity = 0x06040001
        datosIntradia = 0x06040002

    _fext_ = ['xml']



R = ResourcePointers()
R.rid = 0x06
