# -*- coding: utf-8 -*-
from Android.interface.IFragmentManager import IFragmentManager
from FragmentTransaction import FragmentTransaction
import Tkinter as tk

class FragmentManager(IFragmentManager):
    _backStack = []
    _backStackChangedListener = []
    _fmFragments = []
    _fragmentActivity = None
    _fragmentLifecycleCallbacks = []

    def _setFragmentActivity(self, fragmentActivity):
        self._fragmentActivity = self._fragmentActivity or fragmentActivity

    def _broadcastToBackStackChangeListeners(self, operationId):
        for listener in self._backStackChangedListener:
            bFlag = listener(operationId)
            if not bFlag: break
        return bFlag

    def _addToBackStack(self, name, fragmentTransaction):
        bFlag = self._broadcastToBackStackChangeListeners('add', name, fragmentTransaction)
        if bFlag: self._backStack.append((name, fragmentTransaction))

    def _onFragmentEvent(self, event, fragment, *args):
        if event == 'onActivityCreated':
            pass
        elif event == 'onAttach':
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentPreAttached(self, fragment, self._fragmentActivity)
            fragment.onAttach(*args)
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentAttached(self, fragment, self._fragmentActivity)
        elif event == 'onCreate':
            bundle, = args
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentPreCreated(self, fragment, bundle)
            fragment.onCreate(bundle)
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentCreated(self, fragment, bundle)
        elif event == 'onDestroy':
            fragment.onDestroy()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentDestroyed(self, fragment)
        elif event == 'onDetach':
            fragment.onDetach()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentDetached(self, fragment)
        elif event == 'onPause':
            fragment.onPause()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentPaused(self, fragment)
        elif event == 'onResume':
            fragment.onResume()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentResumed(self, fragment)
        elif event == 'onStart':
            fragment.onStart()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentStarted(self, fragment)
        elif event == 'onStop':
            fragment.onStop()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentStopped(self, fragment)
        elif event == 'onCreateView':
            inflater, viewgroup, bundle = args
            view = fragment.onCreateView(inflater, viewgroup, bundle)
            if view:
                view.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
                fragment.onViewCreated(view, bundle)
                for cb in self._fragmentLifecycleCallbacks:
                    cb.onFragmentViewCreated(self, fragment, view, bundle)
        elif event == 'onDestroyView':
            fragment.onDestroyView()
            for cb in self._fragmentLifecycleCallbacks:
                cb.onFragmentViewDestroyed(self, fragment)

    def addOnBackStackChangedListener(self, listener):
        """Add a new listener for changes to the fragment back stack."""
        self._backStackChangedListener.append(listener)

    def beginTransaction(self):
        """Start a series of edit operations on the Fragments associated
        with this FragmentManager."""
        ft = FragmentTransaction()
        ft._setFragmentManager(self)
        return ft

    def dump(self, prefix, fd, writer, args):
        """Print the FragmentManager's state into the given stream."""
        pass

    def enableDebugLogging(self, enabled):
        """Control whether the framework's internal fragment manager debugging
        logs are turned on."""
        pass

    def executePendingTransactions(self):
        """After a FragmentTransaction is committed with
        FragmentTransaction.commit(), it is scheduled to be executed asynchronously
        on the process's main thread."""
        self.__fragmentActivity.frame.update_idletasks()
        pass

    def findFragmentById(self, id):
        """Finds a fragment that was identified by the given id either when
        inflated from XML or as the container ID when added in a transaction."""
        filterf = lambda x: x[0] == id
        filterFragments = filter(filterf, self._fmFragments)
        if filterFragments is None:
            """Search in the Transactions"""
            return None
        return filterFragments[0]

    def findFragmentByTag(self, tag):
        """Finds a fragment that was identified by the given tag either when
        inflated from XML or as supplied when added in a transaction."""
        filterf = lambda x: x[1].getId() == tag
        filterFragments = filter(filterf, self._fmFragments)
        if filterFragments is None:
            """Search in the Transactions"""
            return None
        return filterFragments[0]

    def getBackStackEntryAt(self, index):
        """Return the BackStackEntry at index index in the back stack; entries
        start index 0 being the bottom of the stack."""
        return self._backStack[index]

    def getBackStackEntryCount(self):
        """Return the number of entries currently in the back stack."""
        return len(self._backStack)

    def getFragment(self, bundle, key):
        """Retrieve the current Fragment instance for a reference previously
        placed with putFragment(Bundle, String, Fragment)."""
        pass

    def getFragments(self):
        """Get a list of all fragments that are currently added to the
        FragmentManager."""
        filterf = lambda x: not x[2].isDetached()
        return filter(filterf, self._fmFragments)

    def getPrimaryNavigationFragment(self):
        """Return the currently active primary navigation fragment for this
        FragmentManager."""
        pass

    def isDestroyed(self):
        """Returns true if the final Activity.onDestroy() call has been made on
        the FragmentManager's Activity, so this instance is now dead."""
        pass

    def isStateSaved(self):
        """Returns true if the FragmentManager's state has already been saved
        by its host."""
        pass

    def popBackStack(self, id=None, name=None, flags=None):
        """Pop the top state off the back stack when id, name and flags are None.
        Or pop all back stack states up to the one with the given identifier or name.
        """
        self.__fragmentActivity.frame.after(100, self.popBackStackImmediate, (id, name, flags))

    def popBackStackImmediate(self, id=None, name=None, flags=None):
        """Like popBackStack(), but performs the operation immediately inside
        of the call."""
        bFlag = self._broadcastToBackStackChangeListeners('pop', id, name, flags)
        try:
            if id:
                filterf = lambda x: x.getId() != id
            elif name:
                filterf = lambda x: x.getName() != name
            else:
                filterf = False
            while filterf(self.getBackStackEntryAt(-1)):
                self._backStack.pop()
            if flags is None or flags == self.POP_BACK_STACK_INCLUSIVE:
                self._backStack.pop()
            return True
        except:
            return False

    def putFragment(self, bundle, key, fragment):
        """Put a reference to a fragment in a Bundle."""
        bundle[key] = self.saveFragmentInstanceState(fragment)

    def registerFragmentLifecycleCallbacks(self, cb, recursive):
        """Registers a FragmentManager.FragmentLifecycleCallbacks to listen to
        fragment lifecycle events happening in this FragmentManager."""
        self._fragmentLifecycleCallbacks.append(cb)
        pass

    def removeOnBackStackChangedListener(self, listener):
        """Remove a listener that was previously added with
        addOnBackStackChangedListener(OnBackStackChangedListener)."""
        self._backStackChangedListener.remove(listener)

    def saveFragmentInstanceState(self, f):
        """Save the current instance state of the given Fragment."""
        pass

    def unregisterFragmentLifecycleCallbacks(self, cb):
        """Unregisters a previously registered
        FragmentManager.FragmentLifecycleCallbacks."""
        self._fragmentLifecycleCallbacks.remove(cb)
        pass
