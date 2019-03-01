# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/org/xmlpull/v1/XmlPullParserFactory.html"""
import importlib

from Android import overload, Object
from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlSerializer import XmlSerializer

class XmlPullParserFactory(Object):
    '''
    This class is used to create implementations of XML Pull Parser defined
    in XMPULL V1 API.
    '''
    """
    public static final String PROPERTY_NAME
    """
    PROPERTY_NAME = 'org.xmlpull.v1.XmlPullParserFactory'

    def __init__(self):
        super(XmlPullParserFactory, self).__init__()
        """
        protected String classNamesLocation:
        Unused, but we have to keep it because it's public API.
        """
        self.classNamesLocation = ''

        """
        protected HashMap<String, Boolean> features:
        
        """
        self.features = {}

        """
        protected ArrayList parserClasses
        """
        self.parserClasses = []

        """
        protected ArrayList serializerClasses
        """
        self.serializerClasses = []

    def getFeature(self, name):
        """
        Return the current value of the feature with given name. NOTE: factory
        features are not used for XML Serializer.
        :param name: String: The name of feature to be retrieved.
        :return: boolean. The value of named feature. Unknown features are
        always returned as false
        """
        return self.features.get(name, False)

    def isNamespaceAware(self):
        """
        Indicates whether or not the factory is configured to produce parsers
        which are namespace aware (it simply set feature
        XmlPullParser.FEATURE_PROCESS_NAMESPACES to true or false).
        :return: boolean. true if the factory is configured to produce parsers
        which are namespace aware; false otherwise.
        """
        name = XmlPullParser.FEATURE_PROCESS_NAMESPACES
        return self.getFeature(name)

    def isValidating(self):
        """
        Indicates whether or not the factory is configured to produce parsers
        which validate the XML content during parse.
        :return: boolean. true if the factory is configured to produce parsers
        which validate the XML content during parse; false otherwise.
        """
        name = XmlPullParser.FEATURE_VALIDATION
        return self.getFeature(name)

    @overload
    @classmethod
    def newInstance(cls):
        """
        Creates a new instance of a PullParserFactory that can be used to
        create XML pull parsers. The factory will always return instances of
        Android's built-in XmlPullParser and XmlSerializer.
        :return: XmlPullParserFactory.
        :raises: XmlPullParserException
        """
        return cls.newInstance(None, None)

    @newInstance.adddef('@str', '@type')
    @classmethod
    def newInstance(cls, unused, unused2):
        """
        Creates a factory that always returns instances of Android's built-in
        XmlPullParser and XmlSerializer implementation. This does not support
        factories capable of creating arbitrary parser and serializer
        implementations. Both arguments to this method are unused.
        :param unused: String
        :param unused2: Class
        :return: XmlPullParserFactory.
        :raises: XmlPullParserException
        """
        classNames = "Android.reference.xmlpull.XmlPullParserImpl,Android.reference.xmlpull.XmlPullParserFactory"
        parserClasses = []
        serializerClasses = []
        factory = None
        for classname in classNames.split(','):
            try:
                module = importlib.import_module(classname)
                candidate = getattr(module, classname.rsplit('.')[-1])
            except:
                pass
            if issubclass(candidate, XmlPullParser):
                parserClasses.append(candidate)
                continue
            if issubclass(candidate, XmlSerializer):
                serializerClasses.append(candidate)
                continue
            if issubclass(candidate, XmlPullParserFactory) and not factory:
                factory = candidate()
        factory = factory or cls()
        factory.parserClasses = parserClasses
        factory.serializerClasses = serializerClasses
        factory.classNamesLocation = classNames
        return factory

    def newPullParser(self):
        """
        Creates a new instance of a XML Pull Parser using the currently
        configured factory features.
        :return: XmlPullParser. A new instance of a XML Pull Parser.
        :raises: XmlPullParserException
        """
        if self.parserClasses is None:
            raise Exception('XmlPullParserException: "Factory initialization was incomplete"')
        if not self.parserClasses:
            raise Exception('XmlPullParserException: "No valid parser classes found in %s"' % self.classNamesLocation)
        issues = ''
        for parserClass in self.parserClasses:
            try:
                parser = parserClass()
                map(lambda x: parser.setFeature(*x), self.features.items())
                return parser
            except Exception as e:
                issues += parserClass.__name__ + ': ' + e.message
        raise Exception('XmlPullParserException: "could not create parser: %s"' % issues)

    def newSerializer(self):
        """
        Creates a new instance of a XML Serializer.  NOTE: factory features
        are not used for XML Serializer.
        :return: XmlSerializer. A new instance of a XML Serializer.
        :raises: XmlPullParserExceptionif a parser cannot be created which
        satisfies the requested configuration.
        """
        if self.serializerClasses is None:
            raise Exception('XmlPullParserException: "Factory initialization was incomplete"')
        if not self.serializerClasses:
            raise Exception('XmlPullParserException: "No valid serializer classes found in %s"' % self.classNamesLocation)
        issues = ''
        for serializerClass in self.serializerClasses:
            try:
                return serializerClass()
            except Exception as e:
                issues += serializerClass.__name__ + ': ' + e.message
        raise Exception('XmlPullParserException: "could not create serializer: %s"' % issues)

    def setFeature(self, name, state):
        """
        Set the features to be set when XML Pull Parser is created by this
        factory. NOTE: factory features are not used for XML Serializer.
        :param name: String: string with URI identifying feature
        :param state: boolean: if true feature will be set; if false will be
        ignored
        :raises: XmlPullParserException
        """
        self.features[name] = state

    def setNamespaceAware(self, awareness):
        """
        Specifies that the parser produced by this factory will provide
        support for XML namespaces. By default the value of this is set to
        false.
        :param awareness: boolean: true if the parser produced by this code
        will provide support for XML namespaces;  false otherwise.
        """
        name = XmlPullParser.FEATURE_PROCESS_NAMESPACES
        self.setFeature(name, awareness)

    def setValidating(self, validating):
        """
        Specifies that the parser produced by this factory will be validating
        (it simply set feature XmlPullParser.FEATURE_VALIDATION to true or
        false).  By default the value of this is set to false.
        :param validating: boolean: - if true the parsers created by this
        factory  must be validating.
        """
        name = XmlPullParser.FEATURE_VALIDATION
        self.setFeature(name, validating)

