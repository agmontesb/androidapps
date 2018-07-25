# -*- coding: utf-8 -*-
import abc


class IFragmentManager(object):
    __metaclass__ = abc.ABCMeta

    POP_BACK_STACK_INCLUSIVE =  0x00000001

    @abc.abstractmethod
    def addOnBackStackChangedListener(self, listener):
        """Add a new listener for changes to the fragment back stack."""
        pass

    @abc.abstractmethod
    def beginTransaction(self):
        """Start a series of edit operations on the Fragments associated
        with this FragmentManager."""
        pass

    @abc.abstractmethod
    def dump(self, prefix, fd, writer, args):
        """Print the FragmentManager's state into the given stream."""
        pass

    @abc.abstractmethod
    def enableDebugLogging(self, enabled):
        """Control whether the framework's internal fragment manager debugging
        logs are turned on."""
        pass

    @abc.abstractmethod
    def executePendingTransactions(self):
        """After a FragmentTransaction is committed with
        FragmentTransaction.commit(), it is scheduled to be executed asynchronously
        on the process's main thread."""
        pass

    @abc.abstractmethod
    def findFragmentById(self, id):
        """Finds a fragment that was identified by the given id either when
        inflated from XML or as the container ID when added in a transaction."""
        pass

    @abc.abstractmethod
    def findFragmentByTag(self, tag):
        """Finds a fragment that was identified by the given tag either when
        inflated from XML or as supplied when added in a transaction."""
        pass

    @abc.abstractmethod
    def getBackStackEntryAt(self, index):
        """Return the BackStackEntry at index index in the back stack; entries
        start index 0 being the bottom of the stack."""
        pass

    @abc.abstractmethod
    def getBackStackEntryCount(self):
        """Return the number of entries currently in the back stack."""
        pass

    @abc.abstractmethod
    def getFragment(self, bundle, key):
        """Retrieve the current Fragment instance for a reference previously
        placed with putFragment(Bundle, String, Fragment)."""
        pass

    @abc.abstractmethod
    def getFragments(self):
        """Get a list of all fragments that are currently added to the
        FragmentManager."""
        pass

    @abc.abstractmethod
    def getPrimaryNavigationFragment(self):
        """Return the currently active primary navigation fragment for this
        FragmentManager."""
        pass

    @abc.abstractmethod
    def isDestroyed(self):
        """Returns true if the final Activity.onDestroy() call has been made on the FragmentManager's Activity, so this instance is now dead."""
        pass

    @abc.abstractmethod
    def isStateSaved(self):
        """Returns true if the FragmentManager's state has already been saved
        by its host."""
        pass

    @abc.abstractmethod
    def popBackStack(self, id=None, name=None, flags=None):
        """Pop the top state off the back stack when id, name and flags are None.
        Or pop all back stack states up to the one with the given identifier or name.
        """
        pass

    @abc.abstractmethod
    def popBackStackImmediate(self, id=None, name=None, flags=None):
        """Like popBackStack(), but performs the operation immediately inside
        of the call."""
        pass

    @abc.abstractmethod
    def putFragment(self, bundle, key, fragment):
        """Put a reference to a fragment in a Bundle."""
        pass

    @abc.abstractmethod
    def registerFragmentLifecycleCallbacks(self, cb, recursive):
        """Registers a FragmentManager.FragmentLifecycleCallbacks to listen to
        fragment lifecycle events happening in this FragmentManager."""
        pass

    @abc.abstractmethod
    def removeOnBackStackChangedListener(self, listener):
        """Remove a listener that was previously added with
        addOnBackStackChangedListener(OnBackStackChangedListener)."""
        pass

    @abc.abstractmethod
    def saveFragmentInstanceState(self, f):
        """Save the current instance state of the given Fragment."""
        pass

    @abc.abstractmethod
    def unregisterFragmentLifecycleCallbacks(self, cb):
        """Unregisters a previously registered
        FragmentManager.FragmentLifecycleCallbacks."""
        pass
