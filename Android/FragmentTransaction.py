# -*- coding: utf-8 -*-

from interface.IFragmentTransaction import IFragmentTransaction
import Tkinter as tk


class FragmentTransaction(IFragmentTransaction):
    _ftransaction = []
    _allowAddToBackStack = True
    _fragmentManager = None
    _isAddedToBackStack = False

    def _setFragmentManager(self, fm):
        self._fragmentManager = self._fragmentManager or fm

    def add(self, fragment, containerViewId=None, tag=''):
        """Add a fragment to the activity state."""
        self._ftransaction.append(('add', (fragment, containerViewId, tag)))
        return self

    def addSharedElement(self, sharedElement, name):
        """Used with custom Transitions to map a View from a removed or hidden 
        Fragment to a View from a shown or added Fragment."""
        return self

    def addToBackStack(self, name):
        """Add this transaction to the back stack."""
        if not self._allowAddToBackStack:
            raise Exception('IllegalStateException')
        self._ftransaction.append(('addToBackStack', (name, )))
        self._isAddedToBackStack = True
        return self

    def attach(self, fragment):
        """Re-attach a fragment after it had previously been detached from the UI 
        with detach(Fragment)."""
        self._ftransaction.append(('attach', (fragment, )))
        return self

    def commit(self):
        """Schedules a commit of this transaction."""
        pass

    def commitAllowingStateLoss(self):
        """Like commit() but allows the commit to be executed after an activity's 
        state is saved."""
        pass

    def commitNow(self):
        """Commits this transaction synchronously."""
        fm = self._fragmentManager
        fa = fm._fragmentActivity
        stack = self._ftransaction[::-1]
        while stack:
            operation, args = stack.pop()
            if operation == 'add':
                fInstance, resid, tag = args
                if resid:
                    container = fa.findViewById(resid)
                    frame = fInstance.onCreateView(fa, container, None)
                    if not frame: continue
                    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
                    fInstance.onViewCreated(frame, None)
                fInstance.onCreate(None)
                fm._fmFragments.append((resid, tag, fInstance))
            elif operation == 'remove':
                fInstance, = args
                pass
            elif operation == 'replace':
                pass
            elif operation == 'attach':
                fInstance, = args
                fInstance.onAttach(fa)
            elif operation == 'detach':
                pass
            elif operation == 'hide':
                fInstance, = args
                pass
            elif operation == 'show':
                fInstance, = args
                pass
            elif operation == 'runOnCommit':
                pass



        pass

    def commitNowAllowingStateLoss(self):
        """Like commitNow() but allows the commit to be executed after an 
        activity's state is saved."""
        pass

    def detach(self, fragment):
        """Detach the given fragment from the UI."""
        self._ftransaction.append(('detach', (fragment, )))
        return self

    def disallowAddToBackStack(self):
        """Disallow calls to addToBackStack(String)."""
        self._allowAddToBackStack = False
        return self

    def hide(self, fragment):
        """Hides an existing fragment."""
        self._ftransaction.append(('hide', (fragment, )))
        return self

    def isAddToBackStackAllowed(self):
        """Returns true if this FragmentTransaction is allowed to be added 
        to the back stack."""
        return self._allowAddToBackStack

    def isEmpty(self):
        return self._ftransaction is None

    def remove(self, fragment):
        """Remove an existing fragment"""
        self._ftransaction.append(('remove', (fragment, )))
        return self

    def replace(self, containerViewId, fragment, tag=''):
        """Replace an existing fragment that was added to a container."""
        self._ftransaction.append(('replace', (containerViewId, fragment, tag)))
        return self

    def runOnCommit(self, runnable):
        """Add a Runnable to this transaction that will be run after this 
        transaction has been committed."""
        if self._isAddedToBackStack:
            raise Exception('IllegalStateException')
        self._ftransaction.append(('runOnCommit', (runnable, )))
        return self

    def setAllowOptimization(self, allowOptimization):
        """This method was deprecated in API level 26.1.0.
        This has been renamed setReorderingAllowed(boolean)."""
        return self

    def setBreadCrumbShortTitle(self, int):
        """Set the short title to show as a bread crumb when this transaction
         is on the back stack."""
        return self

    def setBreadCrumbTitle(self, res):
        """Set the full title to show as a bread crumb when this transaction 
        is on the back stack."""
        return self

    def setCustomAnimations(self, enter, exit, popEnter=None, popExit=None):
        """Set specific animation resources to run for the fragments that are entering and exiting in this transaction."""
        return self

    def setPrimaryNavigationFragment(self, fragment):
        """Set a currently active fragment in this FragmentManager as the 
        primary navigation fragment."""
        return self

    def setReorderingAllowed(self, reorderingAllowed):
        """Sets whether or not to allow optimizing operations within and across 
        transactions."""
        return self

    def setTransition(self, transit):
        """Select a standard transition animation for this transaction."""
        return self

    def setTransitionStyle(self, styleRes):
        """Set a custom style resource that will be used for resolving transit 
        animations."""
        return self

    def show(self, fragment):
        """Shows a previously hidden fragment."""
        self._ftransaction.append(('show', (fragment, )))
        return self
