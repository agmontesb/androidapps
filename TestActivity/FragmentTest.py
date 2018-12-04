# -*- coding: utf-8 -*-
from Android import Activity
from Android.app.FragmentActivity import FragmentActivity
from TestActivityManager import R
from DetailsFragment import DetailsFragment

TITLES = ['frgmt1', 'frgmt2', 'frgmt3', 'frgmt4', 'frgmt5', ]
KEYS = ['details_nombre', 'details_apellido1', 'details_apellido2',
        'details_edad', 'details_celular']
DETAILS = [('Alex1', 'Montes1', 'Barrios1', 55, '301-8049930',),
           ('Alex2', 'Montes2', 'Barrios2', 56, '302-8049930',),
           ('Alex3', 'Montes3', 'Barrios3', 57, '303-8049930',),
           ('Alex4', 'Montes4', 'Barrios4', 58, '304-8049930',),
           ('Alex5', 'Montes5', 'Barrios5', 59, '305-8049930',),]

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
        ipos = TITLES.index(fname)
        detailMap = dict(zip(KEYS, DETAILS[ipos]))
        detFragment = DetailsFragment()
        detFragment.setArguments(detailMap)
        ft = self.getSupportFragmentManager().beginTransaction()
        ft.replace(R.id.f_details, detFragment)
        ft.commit()
        pass

    def getTreeData(self):
        return TITLES
