# -*- coding: utf-8 -*-
from Android import Activity, BasicViews
from Android.Intent import Intent
from Android.FragmentActivity import FragmentActivity
from TestActivityManager import R


class FragmentTest(FragmentActivity):
    def onCreate(self):
        Activity.onCreate(self)
        self.setContentView(R.layout.fragment_layout)
        pass

    def onTreeSel(self, event):
        treew = event.widget
        selId = treew.selection()[0]
        fname = treew.set(selId, column = 'Fragment Name')
        print fname
        # datosMnemo =  filter(lambda x: x[0] == mnemo, self.extras['datosIntradia'])
        # anIntent = Intent(component=('DatosBVC', 'DatosIntradia'))
        # extras = dict(datosMnemo=datosMnemo)
        # anIntent.putExtras(extras)
        # self.startActivity(anIntent)

    def getTreeData(self):
        return ['frgmt1', 'frgmt2', 'frgmt3', 'frgmt4', 'frgmt5', ]
