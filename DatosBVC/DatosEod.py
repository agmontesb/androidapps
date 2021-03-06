# -*- coding: utf-8 -*-

import Android as android
from Android import Activity
from AppCompat import AppCompatResources as appcompat
from DatosBVCManager import R
import Tkinter as tk
from Android.content.Intent import Intent


class DatosEod(Activity):

    def onCreate(self):
        Activity.onCreate(self)
        self.setContentView(R.layout.DatosEod)
        anIntent = self.getIntent()
        self.extras = anIntent.getExtras()
        lstwdg = self.findViewById(R.id.eodtable)
        lstwdg.tree.bind('<<TreeviewSelect>>', self.onTreeSel)
        lstwdg.setValue(self.extras['datosEOD'])


    def onClickAction(self, resourceEntry):
        pass

    def onTreeSel(self, event):
        treew = event.widget
        selId = treew.selection()[0]
        mnemo = treew.set(selId, column = 'Mnemo')
        datosMnemo =  filter(lambda x: x[0] == mnemo, self.extras['datosIntradia'])
        anIntent = Intent().setComponent(*('DatosBVC', '.DatosIntradia'))
        extras = dict(datosMnemo=datosMnemo)
        anIntent.putExtras(extras)
        self.startActivity(anIntent)
