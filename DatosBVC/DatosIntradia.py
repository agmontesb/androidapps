# -*- coding: utf-8 -*-

import Android as android
from Android import Activity
from AppCompat import AppCompatResources as appcompat
from DatosBVCManager import R
import Tkinter as tk
from Android.content.Intent import Intent


class DatosIntradia(Activity):

    def onCreate(self):
        Activity.onCreate(self)
        self.setContentView(R.layout.datosIntradia)
        anIntent = self.getIntent()
        self.extras = anIntent.getExtras()
        lstwdg = self.findViewById(R.id.intradiatable)
        lstwdg.setValue(self.extras['datosMnemo'])


    def onClickAction(self, resourceEntry):
        pass

