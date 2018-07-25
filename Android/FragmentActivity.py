# -*- coding: utf-8 -*-
import Tkinter as tk

from Android import BasicViews
from Android.Activity import Activity
from Android.Activity import ON_CREATE, ON_START, ON_RESUME
from Android.Activity import ON_PAUSE, ON_STOP, ON_DESTROY
from Android.Fragment import Fragment
from Android.FragmentManager import FragmentManager


# class FragmentManager(object):
#     _fragmentManager = []
#
#     def add(self, fragment):
#         self._fragmentManager.append(fragment)
#
#     def getFragments(self):
#         return self._fragmentManager


class FragmentActivity(Activity):
    _fragmentManager = None

    def dump(self, prefix, fd, writer, args):
        """Print the Activity's state into the given stream."""
        pass

    def getLastCustomNonConfigurationInstance(self):
        """Return the value previously returned from
        onRetainCustomNonConfigurationInstance()."""
        pass

    def getLifecycle(self):
        """Returns the Lifecycle of the provider."""
        pass

    def getSupportFragmentManager(self):
        """Return the FragmentManager for interacting with fragments associated
        with this activity."""
        fm = FragmentManager()
        fm._setFragmentActivity(self)
        return fm

    def getSupportLoaderManager(self):
        pass

    def getViewModelStore(self):
        """Returns the ViewModelStore associated with this activity"""

    def onAttachFragment(self, fragment):
        """. Called when a fragment is attached to the activity."""
        pass

    def onBackPressed(self):
        """Take care of popping the fragment back stack or finishing the activity
        as appropriate."""
        pass

    def onConfigurationChanged(self, newConfig):
        """Dispatch configuration change to all fragments."""
        pass

    def onCreatePanelMenu(self, featureId, menu):
        """Dispatch to Fragment.onCreateOptionsMenu()."""
        pass

    def onCreateView(self, parent, name, context, attrs):
        pass

    def onLowMEmory(self):
        """Dispatch onLowMemory() to all fragments."""
        pass

    def onMenuItemSelected(self, featureId, item):
        """Dispatch context and options menu to fragments."""
        pass

    def onMultiWindowModeChanged(self, isInMultiWindowMode):
        """ Note: If you override this method you must call
        super.onMultiWindowModeChanged to correctly dispatch the event to support
        fragments attached to this activity."""
        pass

    def onPanelClosed(self, featureId, menu):
        """Call onOptionsMenuClosed() on fragments."""
        pass

    def onPictureInPictureModeChanged(self, isInPictureInPictureMode):
        """ Note: If you override this method you must call
        super.onPictureInPictureModeChanged to correctly dispatch the event
        to support fragments attached to this activity."""
        pass

    def onPreparePanel(self, featureId, view, menu):
        """Dispatch onPrepareOptionsMenu() to fragments."""
        pass

    def onRequestPermissionsResult(self, requestCode, permissions, grantResults):
        """Callback for the result from requesting permissions."""
        pass

    def onRetainCustomNonConfigurationInstance(self):
        """Use this instead of onRetainNonConfigurationInstance()."""
        pass

    def onRetainNonConfigurationInstance(self):
        """Retain all appropriate fragment state."""
        pass

    def onStateNotSaved(self):
        """Hook in to note that fragment state is no longer saved."""
        pass

    def setEnterSharedElementCallback(self, callback):
        """When makeSceneTransitionAnimation(Activity, android.view.View, String)
        was used to start an Activity, callback will be called to handle shared
        elements on the launched Activity."""
        pass

    def setExitSharedElementCallback(self, listener):
        """When makeSceneTransitionAnimation(Activity, android.view.View, String)
        was used to start an Activity, listener will be called to handle shared elements on the launching Activity."""
        pass

    def startActivityForResult(self, intent, requestCode, options):
        """Modifies the standard behavior to allow results to be delivered
        to fragments."""
        pass

    def startActivityFromFragment(self, fragment, intent, requestCode):
        """Called by Fragment.startActivityForResult() to implement its behavior."""
        pass

    def startActivityFromFragment(self, fragment, intent, requestCode, options):
        """Called by Fragment.startActivityForResult() to implement its behavior."""
        pass

    def startIntentSenderForResult(self, intent, requestCode, fillInIntent, flagsMask, flagsValues, extraFlags):
        """Called by Fragment.startIntentSenderForResult() to implement its behavior."""
        pass

    def supportFinishAfterTransition(self):
        """Reverses the Activity Scene entry Transition and triggers the calling Activity to reverse its exit Transition."""
        pass

    def supportInvalidateOptionsMenu(self):
        """This method was deprecated  in API level 26.1.0. Call invalidateOptionsMenu()
         directly.                                                                                      void                      supportPostponeEnterTransition()                    Support library version of postponeEnterTransition() that works only on API 21 and later."""
        pass

    def supportStartPostponedEnterTransition(self):
        """Support library version of startPostponedEnterTransition() that only works with API 21 and later."""
        pass

    def validateRequestPermissionsRequestCode(self, requestCode):
        pass

    def setContentView(self, viewid, settings=None):
        selPanel = self.getResources().getLayout(viewid).find('category')
        fm = self.getSupportFragmentManager()
        ft = fm.beginTransaction()
        for item in selPanel.findall('.//fragment'):
            id, tag, name = map(item.get, ('id', 'tag', 'name'))
            resid = self.getResources().getIdentifier(id)
            fInstance = Fragment.instantiate(self, name)
            ft.attach(fInstance).add(fInstance, resid, tag)
        self.form = form = BasicViews.formFrameGen(self.frame, settings, selPanel)
        ft.commitNow()
        form.pack(fill=tk.BOTH, expand=tk.YES)
        form.onClickEvent = self.onClickEvent
        form.onChangeSelEvent = self.onChangeSelEvent

    def onLifecycleEvent(self, event):
        fm = self.getSupportFragmentManager()
        if event == ON_CREATE:
            self.onCreate()
            for id, tag, fragment in fm.getFragments():
                fragment.onActivityCreated(None)
        elif event == ON_START:
            self.onStart()
            for id, tag, fragment in fm.getFragments():
                fragment.onStart()
        elif event == ON_RESUME:
            self.onResume()
            for id, tag, fragment in fm.getFragments():
                fragment.onResume()
        elif event == ON_PAUSE:
            for id, tag, fragment in fm.getFragments():
                fragment.onPauseCreated()
            self.onPause()
        elif event == ON_STOP:
            for id, tag, fragment in fm.getFragments():
                fragment.onStop()
            self.onStop()
        elif event == ON_DESTROY:
            for id, tag, fragment in fm.getFragments():
                fragment.onDestroyView()
                fragment.onDestroy()
                fragment.onDetach()
            self.onDestroy()
