# -*- coding: utf-8 -*-
import abc

class IFragmentTransaction(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, containerViewId, fragment, tag):
        """Add a fragment to the activity state."""
        pass

    @abc.abstractmethod
    def addSharedElement(self, sharedElement, name):
        """Used with custom Transitions to map a View from a removed or hidden
        Fragment to a View from a shown or added Fragment."""
        pass

    @abc.abstractmethod
    def addToBackStack(self, name):
        """Add this transaction to the back stack."""
        pass

    @abc.abstractmethod
    def attach(self, fragment):
        """Re-attach a fragment after it had previously been detached from the UI
        with detach(Fragment)."""
        pass

    @abc.abstractmethod
    def commit(self):
        """Schedules a commit of this transaction."""
        pass

    @abc.abstractmethod
    def commitAllowingStateLoss(self):
        """Like commit() but allows the commit to be executed after an activity's
        state is saved."""
        pass

    @abc.abstractmethod
    def commitNow(self):
        """Commits this transaction synchronously."""
        pass

    @abc.abstractmethod
    def commitNowAllowingStateLoss(self):
        """Like commitNow() but allows the commit to be executed after an
        activity's state is saved."""
        pass

    @abc.abstractmethod
    def detach(self, fragment):
        """Detach the given fragment from the UI."""
        pass

    @abc.abstractmethod
    def disallowAddToBackStack(self):
        """Disallow calls to addToBackStack(String)."""
        pass

    @abc.abstractmethod
    def hide(self, fragment):
        """Hides an existing fragment."""
        pass

    @abc.abstractmethod
    def isAddToBackStackAllowed(self):
        """Returns true if this FragmentTransaction is allowed to be added
        to the back stack."""
        pass

    @abc.abstractmethod
    def isEmpty(self):
        """Remove an existing fragment."""
        pass

    @abc.abstractmethod
    def remove(self, fragment):
        """Remove an existing fragment"""
        pass

    @abc.abstractmethod
    def replace(self, fragment, containerViewId=None, tag=''):
        """Replace an existing fragment that was added to a container."""
        pass

    @abc.abstractmethod
    def replace(self, containerViewId, fragment):
        """Calls replace(int, Fragment, String) with a null tag."""
        pass

    @abc.abstractmethod
    def runOnCommit(self, runnable):
        """Add a Runnable to this transaction that will be run after this
        transaction has been committed."""
        pass

    @abc.abstractmethod
    def setAllowOptimization(self, allowOptimization):
        """This method was deprecated in API level 26.1.0.
        This has been renamed setReorderingAllowed(boolean)."""
        pass

    @abc.abstractmethod
    def setBreadCrumbShortTitle(self, int):
        """Set the short title to show as a bread crumb when this transaction
         is on the back stack."""
        pass

    @abc.abstractmethod
    def setBreadCrumbTitle(self, res):
        """Set the full title to show as a bread crumb when this transaction
        is on the back stack."""
        pass

    @abc.abstractmethod
    def setCustomAnimations(self, enter, exit, popEnter=None, popExit=None):
        """Set specific animation resources to run for the fragments that are entering and exiting in this transaction."""
        pass

    @abc.abstractmethod
    def setPrimaryNavigationFragment(self, fragment):
        """Set a currently active fragment in this FragmentManager as the
        primary navigation fragment."""
        pass

    @abc.abstractmethod
    def setReorderingAllowed(self, reorderingAllowed):
        """Sets whether or not to allow optimizing operations within and across
        transactions."""
        pass

    @abc.abstractmethod
    def setTransition(self, transit):
        """Select a standard transition animation for this transaction."""
        pass

    @abc.abstractmethod
    def setTransitionStyle(self, styleRes):
        """Set a custom style resource that will be used for resolving transit
        animations."""
        pass

    @abc.abstractmethod
    def show(self, fragment):
        """Shows a previously hidden fragment."""
        pass