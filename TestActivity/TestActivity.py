# -*- coding: utf-8 -*-
from Android import Activity, BasicViews
from Android.content.ComponentName import ComponentName
from Android.content.Intent import Intent
from TestActivityManager import R


class TestActivity(Activity):
    def onCreate(self):
        Activity.onCreate(self)
        self.setContentView(R.layout.basicWidets)
        pass

    def onCreateOptionsMenu(self, menuframe):
        Activity.onCreateOptionsMenu(self, menuframe)
        inflater = self.getMenuInflater()
        inflater.inflate(R.menu.file, menuframe)
        return True

    def onOptionsItemSelected(self, menuitem):
        itemId = menuitem.getItemId()
        if itemId == R.id.create_new:
            component = ComponentName('TestActivity', '.ActivityNumber2')
            anIntent = Intent().setComponent(component)
            self.startActivity(anIntent)
        print self.getResources().getResourceName(itemId)

    def onClickEvent(self, resourceEntry):
        res = self.getResources()
        resid = res.getIdentifier(resourceEntry, defType='id')
        bgbool = (R.id.bgbool1, R.id.bgbool2, R.id.bgbool3)
        if resid in bgbool:
            opAdd = [('*boollbl.foreground', 'red'), ('*boollbl.foreground', 'green'),
                     ('*boollbl.foreground', 'blue')]
            master = self.findViewById(R.id.tcontainer)
            indx = bgbool.index(resid)
            boolwdgid = bgbool[indx]
            boolwdg = self.findViewById(boolwdgid)
            if boolwdg.getValue():
                sitem, scomm = opAdd[indx]
                self.option_add(sitem, scomm)
                wdg = BasicViews.settBool(master, label='created bool')
                master.applyGeoManager(wdg)
