from Android.app.Fragment import Fragment
from Android import BasicViews
from TestActivityManager import R


class DetailsFragment(Fragment):
    mListener = None

    def onCreateView(self, context, container, savedInstanceState):
        super(DetailsFragment, self).onCreateView(context, container, savedInstanceState)
        settings = self.getArguments()
        selPanel = self.getResources().getLayout(R.layout.detailsfragment).find('category')
        form = BasicViews.formFrameGen(container, settings, selPanel)
        return form

    def onAttach(self, context):
        super(DetailsFragment, self).onAttach(context)
        self.mListener = context

    def onCreate(self, savedInstanceState):
        pass

    def onViewCreated(self, view, savedInstanceState):
        super(DetailsFragment, self).onViewCreated(view, savedInstanceState)
        pass

    def onActivityCreated(self, savedInstanceState):
        pass

