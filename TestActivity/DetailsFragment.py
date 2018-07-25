from Android import Activity, BasicViews
import xml.etree.ElementTree as ET


class DetailsFragment(object):
    def __init__(self, master):
        self.master = master

    def onCreateView(self):
        layoutfile = r'/media/amontesb/HITACHI/AndroidApps/TestActivity/res/layout/detailsfragment.xml'
        with open(layoutfile, 'rb') as f:
            xmlstr = f.read()
        root = ET.XML(xmlstr)

        selPanel = root.find('category')
        form = BasicViews.formFrameGen(self.master, {}, selPanel)
        return form