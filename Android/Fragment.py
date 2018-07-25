# -*- coding: utf-8 -*-
import importlib
import inspect

fragmentStyleableItems = ['name', 'id', 'tag', 'fragmentExitTransition',
                          'fragmentEnterTransition', 'fragmentSharedElementEnterTransition',
                          'fragmentReturnTransition', 'fragmentSharedElementReturnTransition',
                          'fragmentReenterTransition', 'fragmentAllowEnterTransitionOverlap',
                          'fragmentAllowReturnTransitionOverlap']


class Fragment(object):
    _id = None
    _tag = ''
    _args = []
    _hasOptionsMenu = False

    def dump(self, prefix, fd, writer, args):
        """Print the Fragments's state into the given stream."""
        pass

    def equals(self, o):
        """Subclasses can not override equals()."""
        pass

    def getActivity(self):
        """Return the FragmentActivity this fragment is currently associated with."""
        return self._activity

    def getAllowEnterTransitionOverlap(self):
        """Returns whether the the exit transition and enter transition overlap
        or not."""
        pass

    def getAllowReturnTransitionOverlap(self):
        """Returns whether the the return transition and reenter transition
        overlap or not."""
        pass

    def getArguments(self):
        """Return the arguments supplied when the fragment was instantiated,
        if any."""
        return self._args

    def getChildFragmentManager(self):
        """Return a private FragmentManager for placing and managing Fragments
        inside of this Fragment."""
        pass

    def getContext(self):
        """Return the Context this fragment is currently associated with."""
        pass

    def getEnterTransition(self):
        """Returns the Transition that will be used to move Views into
        the initial scene."""
        pass

    def getExitTransition(self):
        """Returns the Transition that will be used to move Views out of the scene when the fragment is removed, hidden, or detached when not popping the back stack."""
        pass

    def getFragmentManager(self):
        """Return the FragmentManager for interacting with fragments associated
        with this fragment's activity."""
        return self.getActivity().getSupportFragmentManager()

    def getHost(self):
        """Return the host object of this fragment."""
        pass

    def getId(self):
        """Return the identifier this fragment is known by."""
        return self._id

    def getLayoutInflater(self):
        """Returns the cached LayoutInflater used to inflate Views
        of this Fragment."""
        pass

    def getLifecycle(self):
        pass

    def getLoaderManager(self):
        """Return the LoaderManager for this fragment."""
        pass

    def getParentFragment(self):
        """Returns the parent Fragment containing this Fragment."""
        pass

    def getReenterTransition(self):
        """Returns the Transition that will be used to move Views in to
        the scene when returning due to popping a back stack."""
        pass

    def getResources(self):
        """Return requireActivity().getResources()."""
        return self.requireActivity().getResources()

    def getRetainInstance(self):
        pass

    def getReturnTransition(self):
        """Returns the Transition that will be used to move Views out of the
        scene when the Fragment is preparing to be removed, hidden, or detached
        because of popping the back stack."""
        pass

    def getSharedElementEnterTransition(self):
        """Returns the Transition that will be used for shared elements transferred
        into the content Scene."""
        pass

    def getSharedElementReturnTransition(self):
        """Return the Transition that will be used for shared elements transferred
        back during a pop of the back stack."""
        pass

    def getString(self, resId, formatArgs=None):
        """Return a localized formatted string from the application's package's
        default string table, substituting the format arguments as defined in
        Formatter and format(String, Object...)."""
        res = self.getResources()
        return res.getString(resId)

    def getTag(self):
        """Get the tag name of the fragment, if specified."""
        return self._tag

    def getTargetFragment(self):
        """Return the target fragment set by setTargetFragment(Fragment, int)."""
        pass

    def getTargetRequestCode(self):
        """Return the target request code set by setTargetFragment(Fragment, int)."""
        pass

    def getText(self, resId):
        """Return a localized, styled CharSequence from the application's package's
         default string table."""
        res = self.getResources()
        return res.getText(resId)

    def getUserVisibleHint(self):
        """Get the root view for the fragment's layout (the one returned by
        onCreateView(LayoutInflater, ViewGroup, Bundle)), if provided."""
        pass

    def getViewModelStore(self):
        pass

    def hashCode(self):
        """Subclasses can not override hashCode()."""
        pass

    @classmethod
    def instantiate(self, context, fname, args=None):
        """Create a new instance of a Fragment with the given class name."""
        module = fname.rsplit('.', 1)[-1]
        fragment = getattr(importlib.import_module(fname), module)
        fInstance = fragment()
        fInstance.setArguments(args)
        return fInstance

    def isAdded(self):
        """Return true if the fragment is currently added to its activity."""
        pass

    def isDetached(self):
        """Return true if the fragment has been explicitly detached from the UI."""
        pass

    def isHidden(self):
        """Return true if the fragment has been hidden."""
        pass

    def isInLayout(self):
        """Return true if the layout is included as part of an activity view
        hierarchy via the <fragment> tag."""
        pass

    def isRemoving(self):
        """Return true if this fragment is currently being removed from its
        activity."""
        pass

    def isResumed(self):
        """Return true if the fragment is in the resumed state."""
        pass

    def isStateSaved(self):
        """Returns true if this fragment is added and its state has already been
        saved by its host."""
        pass

    def isVisible(self):
        """Return true if the fragment is currently visible to the user."""
        pass

    def onActivityCreated(self, savedInstanceState):
        """Called when the fragment's activity has been created and this
        fragment's view hierarchy instantiated."""
        pass

    def onActivityResult(self, requestCode, resultCode, data):
        """Receive the result from a previous call to
        startActivityForResult(Intent, int)."""
        pass

    def onAttach(self, context):
        """Called when a fragment is first attached to its context."""
        self._activity = context

    def onAttachFragment(self, childFragment):
        """Called when a fragment is attached as a child of this fragment."""
        pass

    def onConfigurationChanged(self, newConfig):
        """This hook is called whenever an item in a context menu is selected."""
        pass

    def onCreate(self, savedInstanceState):
        """Called to do initial creation of a fragment."""
        pass

    def onCreateAnimation(self, transit, enter, nextAnim):
        """Called when a fragment loads an animation."""
        pass

    def onCreateAnimator(self, transit, enter, nextAnim):
        """Called when a fragment loads an animator."""
        pass

    def onCreateContextMenu(self, menu, v, menuInfo):
        """Called when a context menu for the view is about to be shown."""
        pass

    def onCreateOptionsMenu(self, menu, inflater):
        """Initialize the contents of the Fragment host's standard options menu."""
        pass

    def onCreateView(self, context, container, savedInstanceState):
        """Called to have the fragment instantiate its user interface view."""
        pass

    def onDestroy(self):
        """Called when the fragment is no longer in use."""
        pass

    def onDestroyOptionsMenu(self):
        """Called when this fragment's option menu items are no longer being
        included in the overall options menu."""
        pass

    def onDestroyView(self):
        """Called when the view previously created by
        onCreateView(LayoutInflater, ViewGroup, Bundle) has been detached from
        the fragment."""
        pass

    def onDetach(self):
        """Called when the fragment is no longer attached to its activity."""
        pass

    def onGetLayoutInflater(self, savedInstanceState):
        """Returns the LayoutInflater used to inflate Views of this Fragment."""
        pass

    def onHiddenChanged(self, hidden):
        """Called when the hidden state (as returned by isHidden() of the fragment has
        changed."""
        pass

    def onInflate(self, context, attrs, savedInstanceState):
        """Called when a fragment is being created as part of a view layout
        inflation, typically from setting the content view of an activity."""
        pass

    def onLowMemory(self):
        pass

    def onMultiWindowModeChanged(self, isInMultiWindowMode):
        """Called when the Fragment's activity changes from fullscreen mode to
        multi-window mode and visa-versa."""
        pass

    def onOptionsItemSelected(self, item):
        """This hook is called whenever an item in your options menu is selected."""
        pass

    def onOptionsMenuClosed(self, menu):
        """This hook is called whenever the options menu is being closed (either by
        the user canceling the menu with the back/menu button, or when an item is
        selected)."""
        pass

    def onPause(self):
        """Called when the Fragment is no longer resumed."""
        pass

    def onPictureInPictureModeChanged(self, isInPictureInPictureMode):
        """Called by the system when the activity changes to and from
        picture-in-picture mode."""
        pass

    def onPrepareOptionsMenu(self, menu):
        """Prepare the Fragment host's standard options menu to be displayed."""
        pass

    def onRequestPermissionsResult(self, requestCode, permissions, grantResults):
        """Callback for the result from requesting permissions."""
        pass

    def onResume(self):
        """Called when the fragment is visible to the user and actively running."""
        pass

    def onSaveInstanceState(self, outState):
        """Called to ask the fragment to save its current dynamic state, so it can
        later be reconstructed in a new instance of its process is restarted."""
        pass

    def onStart(self):
        """Called when the Fragment is visible to the user."""
        pass

    def onStop(self):
        """Called when the Fragment is no longer started."""
        pass

    def onViewCreated(self, view, savedInstanceState):
        """Called immediately after onCreateView(LayoutInflater, ViewGroup, Bundle)
        has returned, but before any saved state has been restored in to the view."""
        pass

    def onViewStateRestored(self, savedInstanceState):
        """Called when all saved state has been restored into the view hierarchy of
        the fragment."""
        pass

    def postponeEnterTransition(self):
        """Postpone the entering Fragment transition until
        startPostponedEnterTransition() or executePendingTransactions() has been called."""
        pass

    def registerForContextMenu(self, view):
        """Registers a context menu to be shown for the given view (multiple views
        can show the context menu)."""
        pass

    def requestPermissions(self, permissions, requestCode):
        """Requests permissions to be granted to this application."""
        pass

    def requireActivity(self):
        """Return the FragmentActivity this fragment is currently associated with."""
        return self.getActivity()

    def requireContext(self):
        """Return the Context this fragment is currently associated with."""
        pass

    def requireFragmentManager(self):
        """Return the FragmentManager for interacting with fragments associated with
        this fragment's activity."""
        pass

    def requireHost(self):
        """Return the host object of this fragment."""
        pass

    def setAllowEnterTransitionOverlap(self, allow):
        """Sets whether the the exit transition and enter transition overlap or not."""
        pass

    def setAllowReturnTransitionOverlap(self, allow):
        """Sets whether the the return transition and reenter transition overlap or not."""
        pass

    def setArguments(self, args):
        """Supply the construction arguments for this fragment."""
        self._args = args

    def setEnterSharedElementCallback(self, callback):
        """When custom transitions are used with Fragments, the enter transition
        callback is called when this Fragment is attached or detached when not
        popping the back stack."""
        pass

    def setEnterTransition(self, transition):
        """Sets the Transition that will be used to move Views into the initial
        scene."""
        pass

    def setExitSharedElementCallback(self, callback):
        """When custom transitions are used with Fragments, the exit transition
        callback is called when this Fragment is attached or detached when popping
        the back stack."""
        pass

    def setExitTransition(self, transition):
        """Sets the Transition that will be used to move Views out of the scene
        when the fragment is removed, hidden, or detached when not popping the back
        stack."""
        pass

    def setHasOptionsMenu(self, hasMenu):
        """Report that this fragment would like to participate in populating the
        options menu by receiving a call to onCreateOptionsMenu(Menu, MenuInflater)
        and related methods."""
        self._hasOptionsMenu = hasMenu
        pass

    def setInitialSavedState(self, state):
        """Set the initial saved state that this Fragment should restore itself
        from when first being constructed, as returned by
        FragmentManager.saveFragmentInstanceState."""
        pass

    def setMenuVisibility(self, menuVisible):
        """Set a hint for whether this fragment's menu should be visible."""
        pass

    def setReenterTransition(self, transition):
        """Sets the Transition that will be used to move Views in to the scene
        when returning due to popping a back stack."""
        pass

    def setRetainInstance(self, retain):
        """Control whether a fragment instance is retained across Activity
        re-creation (such as from a configuration change)."""
        pass

    def setReturnTransition(self, transition):
        """Sets the Transition that will be used to move Views out of the scene
        when the Fragment is preparing to be removed, hidden, or detached because
        of popping the back stack."""
        pass

    def setSharedElementEnterTransition(self, transition):
        """Sets the Transition that will be used for shared elements transferred
        into the content Scene."""
        pass

    def setSharedElementReturnTransition(self, transition):
        """Sets the Transition that will be used for shared elements transferred
        back during a pop of the back stack."""
        pass

    def setTargetFragment(self, fragment, requestCode):
        """Optional target for this fragment."""
        pass

    def setUserVisibleHint(self, isVisibleToUser):
        """Set a hint to the system about whether this fragment's UI is currently
        visible to the user."""
        pass

    def shouldShowRequestPermissionRationale(self, permission):
        """Gets whether you should show UI with rationale for requesting a
        permission."""
        pass

    def startActivity(self, intent):
        """Call startActivity(Intent) from the fragment's containing Activity."""
        pass

    def startActivity(self, intent, options):
        """Call startActivity(Intent, Bundle) from the fragment's containing
        Activity."""
        activity = self.getActivity()
        activity.startActivity(intent, options)

    def startActivityForResult(self, intent, requestCode, options=None):
        """Call startActivityForResult(Intent, int, Bundle) from the fragment's
        containing Activity."""
        activity = self.getActivity()
        activity.startActivityForResult(intent, requestCode, options)

    def startIntentSenderForResult(self, intent, requestCode, fillInIntent, flagsMask, flagsValues, extraFlags, options):
        """Call startIntentSenderForResult(IntentSender, int, Intent, int, int, int, Bundle) from the fragment's containing Activity."""
        pass

    def startPostponedEnterTransition(self):
        """Begin postponed transitions after postponeEnterTransition() was called."""
        pass

    def toString(self):
        pass

    def unregisterForContextMenu(self, view):
        """Prevents a context menu to be shown for the given view."""
        pass

    @staticmethod
    def _implementsInterface(obj, interface):
        """
        Checks if obj has all the abstract methods and properties defined by interface
        :param obj: A class instance
        :param interface: An abstrac class with __metaclass__ = ABCMeta
        :return: boolean, True if implements the interface
        """
        assert inspect.isabstract(interface), 'Not a valid interface'
        abstractmethods = interface.__dict__['__abstractmethods__']
        return all(map(lambda x: hasattr(obj, x), abstractmethods))
