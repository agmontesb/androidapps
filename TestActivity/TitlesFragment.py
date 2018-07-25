# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from Android.Fragment import Fragment
from Android import BasicViews
from TestActivityManager import R
import inspect

class TitlesFragment(Fragment):

    class OnItemSelectedListener(object):
        __metaclass__ = ABCMeta
        @abstractmethod
        def onTreeSel(self, event):
            pass
        @abstractmethod
        def getTreeData(self):
            pass

    mListener = None

    def onCreateView(self, context, container, savedInstanceState):
        selPanel = self.getResources().getLayout(R.layout.listfragment).find('category')
        form = BasicViews.formFrameGen(container, savedInstanceState, selPanel)
        return form

    def onAttach(self, context):
        super(TitlesFragment, self).onAttach(context)
        bFlag = Fragment._implementsInterface(context, self.OnItemSelectedListener)
        if bFlag:
            self.mListener = context
        else:
            raise Exception('Not implements the interface')

    def onCreate(self, savedInstanceState):
        pass

    def onViewCreated(self, view, savedInstanceState):
        super(TitlesFragment, self).onViewCreated(view, savedInstanceState)
        wdg = view.scrolledlist
        wdg.setSelectListener(self.selectListener)
        thevalues = self.getListData()
        wdg.setValue(thevalues)
        pass

    def onActivityCreated(self, savedInstanceState):
        pass

    def selectListener(self, event):
        return self.mListener.onTreeSel(event)

    def getListData(self):
        return self.mListener.getTreeData()


