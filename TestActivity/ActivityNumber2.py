# -*- coding: utf-8 -*-
import Android as android
import AppCompat as appcompat
from Android import Activity, BasicViews
from TestActivityManager import R


class ActivityNumber2(Activity):
    def onCreate(self):
        Activity.onCreate(self)
        self.frame.config(width=500, height=700)
        self.frame.pack_propagate(0)
        self.setContentView(R.layout.BasicViewsShowcase)
        pass

    def onCreateOptionsMenu(self, menuframe):
        Activity.onCreateOptionsMenu(self, menuframe)
        inflater = self.getMenuInflater()
        inflater.inflate(R.menu.file, menuframe)
        return True

    def onOptionsItemSelected(self, menuitem):
        itemId = menuitem.getItemId()
        print self.getResources().getResourceName(itemId)

    def onClickAction(self, resourceEntry):
        print resourceEntry


