# -*- coding: utf-8 -*-
import abc
from Android import overload


class XmlPullParser(object):
    __metaclass__ = abc.ABCMeta
    '''
    XML Pull Parser is an interface that defines parsing functionality provided
    in XMLPULL V1 API (visit this website to learn more about API and its
    implementations).
    '''
    """
    public static final int CDSECT:
    A CDATA sections was just read;
    this token is available only from calls to nextToken().
    A call to next() will accumulate various text events into a single event
    of type TEXT. The text contained in the CDATA section is available
    by calling getText().
    See also:
    nextToken()
    getText()
    """
    CDSECT = 0x00000005

    """
    public static final int COMMENT:
    An XML comment was just read. This event type is this token is
    available via nextToken() only;
    calls to next() will skip comments automatically.
    The content of the comment can be accessed using the getText()
    method.See also:nextToken()getText()
    """
    COMMENT = 0x00000009

    """
    public static final int DOCDECL:
    An XML document type declaration was just read. This token is
    available from nextToken() only.
    The unparsed text inside the doctype is available via
    the getText() method.See also:nextToken()getText()
    """
    DOCDECL = 0x0000000a

    """
    public static final int END_DOCUMENT:
    Logical end of the xml document. Returned from getEventType, next()
    and nextToken()
    when the end of the input document has been reached.
    NOTE: subsequent calls to
    next() or nextToken()
    may result in exception being thrown.
    See also:
    next()
    nextToken()
    """
    END_DOCUMENT = 0x00000001

    """
    public static final int END_TAG:
    Returned from getEventType(), next(), or
    nextToken() when an end tag was read.
    The name of start tag is available from getName(), its
    namespace and prefix are
    available from getNamespace() and getPrefix().See 

    also:next()nextToken()getName()getPrefix()getNamespace()FEATURE_PROCESS_NAMESPACES
    """
    END_TAG = 0x00000003

    """
    public static final int ENTITY_REF:
    An entity reference was just read;
    this token is available from nextToken()
    only. The entity name is available by calling getName(). If available,
    the replacement text can be obtained by calling getText(); otherwise,
    the user is responsible for resolving the entity reference.
    This event type is never returned from next(); next() will
    accumulate the replacement text and other text
    events to a single TEXT event.See also:nextToken()getText()
    """
    ENTITY_REF = 0x00000006

    """
    public static final String FEATURE_PROCESS_DOCDECL:
    This feature determines whether the document declaration
    is processed. If set to false,
    the DOCDECL event type is reported by nextToken()
    and ignored by next().

    If this feature is activated, then the document declaration
    must be processed by the parser.

    Please note: If the document type declaration
    was ignored, entity references may cause exceptions
    later in the parsing process.
    The default value of this feature is false. 
    This feature cannot be changed during parsing.
    """
    FEATURE_PROCESS_DOCDECL = 'http://xmlpull.org/v1/doc/features.html#process-docdecl'

    """
    public static final String FEATURE_PROCESS_NAMESPACES:
    This feature determines whether the parser processes
    namespaces. As for all features, the default value is false.
    NOTE: The value can not be changed during parsing an must be 
    set before parsing.
    """
    FEATURE_PROCESS_NAMESPACES = 'http://xmlpull.org/v1/doc/features.html#process-namespaces'

    """
    public static final String FEATURE_REPORT_NAMESPACE_ATTRIBUTES:
    This feature determines whether namespace attributes are
    exposed via the attribute access methods. Like all features,
    the default value is false. 
    This feature cannot be changed during parsing.
    """
    FEATURE_REPORT_NAMESPACE_ATTRIBUTES = 'http://xmlpull.org/v1/doc/features.html#report-namespace-prefixes'

    """
    public static final String FEATURE_VALIDATION:
    If this feature is activated, all validation errors as
    defined in the XML 1.0 specification are reported.
    This implies that FEATURE_PROCESS_DOCDECL is true and both, the
    internal and external document type declaration will be processed.
    Please Note: This feature can not be changed
    """
    FEATURE_VALIDATION = 'http://xmlpull.org/v1/doc/features.html#validation'

    """
    public static final int IGNORABLE_WHITESPACE:
    Ignorable whitespace was just read.
    This token is available only from nextToken()).
    For non-validating
    parsers, this event is only reported by nextToken() when outside
    the root element.
    Validating parsers may be able to detect ignorable whitespace at
    other locations.
    The ignorable whitespace string is available by calling getText()

    NOTE: this is different from calling the
    isWhitespace() method, since text content
    may be whitespace but not ignorable.

    Ignorable whitespace is skipped by next() automatically; this event
    type is never returned from next().
    See also:
    nextToken()
    getText()
    """
    IGNORABLE_WHITESPACE = 0x00000007

    """
    public static final String NO_NAMESPACE
    This constant represents the default namespace (empty string "")
    """
    NO_NAMESPACE = ''

    """
    public static final int PROCESSING_INSTRUCTION:
    An XML processing instruction declaration was just read. This
    event type is available only via nextToken().
    getText() will return text that is inside the processing instruction.
    Calls to next() will skip processing instructions automatically.See 
    also:nextToken()getText()
    """
    PROCESSING_INSTRUCTION = 0x00000008

    """
    public static final int START_DOCUMENT:
    Signalize that parser is at the very beginning of the document
    and nothing was read yet.
    This event type can only be observed by calling getEvent()
    before the first call to next(), nextToken, or nextTag()).See 
    also:next()nextToken()
    """
    START_DOCUMENT = 0x00000000

    """
    public static final int START_TAG:
    Returned from getEventType(),
    next(), nextToken() when
    a start tag was read.
    The name of start tag is available from getName(), its namespace and 
    prefix are
    available from getNamespace() and getPrefix()
    if namespaces are enabled.
    See getAttribute* methods to retrieve element attributes.
    See getNamespace* methods to retrieve newly declared namespaces.See 

    also:next()nextToken()getName()getPrefix()getNamespace()getAttributeCount()getDepth()getNamespaceCount(int)getNamespace()FEATURE_PROCESS_NAMESPACES
    """
    START_TAG = 0x00000002

    """
    public static final int TEXT:
    Character data was read and will is available by calling getText().
    Please note:next() will
    accumulate multiple
    events into one TEXT:
     event, skipping IGNORABLE_WHITESPACE,
    PROCESSING_INSTRUCTION and COMMENT events,
    In contrast, nextToken() will stop reading
    text when any other event is observed.
    Also, when the state was reached by calling next(), the text value will
    be normalized, whereas getText() will
    return unnormalized content in the case of nextToken(). This allows
    an exact roundtrip without changing line ends when examining low
    level events, whereas for high level applications the text is
    normalized appropriately.See also:next()nextToken()getText()
    """
    TEXT = 0x00000004

    """
    public static final String[] TYPES:
    This array can be used to convert the event type integer constants
    such as START_TAG or TEXT to
    to a string. For example, the value of TYPES[START_TAG] is
    the string "START_TAG".

    This array is intended for diagnostic output only. Relying
    on the contents of the array may be dangerous since malicious
    applications may alter the array, although it is final, due
    to limitations of the Java language.
    """
    TYPES = ['START_DOCUMENT', 'END_DOCUMENT', 'START_TAG', 'END_TAG', 'TEXT',
             'CDSECT', 'ENTITY_REF', 'IGNORABLE_WHITESPACE', 'PROCESSING_INSTRUCTION',
             'COMMENT', 'DOCDECL']

    def defineEntityReplacementText(self, entityName, replacementText):
        """
        Set new value for entity replacement text as defined in XML 1.0
        Section 4.5 Construction of Internal Entity Replacement Text. If
        FEATURE_PROCESS_DOCDECL or FEATURE_VALIDATION are set, calling this
        function will result in an exception -- when processing of DOCDECL is
        enabled, there is no need to the entity replacement text manually.
        The motivation for this function is to allow very small
        implementations of XMLPULL that will work in J2ME environments. Though
        these implementations may not be able to process the document type
        declaration, they still can work with known DTDs by using this
        function.  Please notes: The given value is used literally as
        replacement text and it corresponds to declaring entity in DTD that
        has all special characters escaped: left angle bracket is replaced
        with &lt;, ampersand with &amp; and so on.
        Note: The given value is the literal replacement text and must not
        contain any other entity reference (if it contains any entity reference
        there will be no further replacement).
        Note: The list of pre-defined entity names will
        always contain standard XML entities such as amp (&amp;), lt
        (&lt;), gt (&gt;), quot (&quot;), and apos (&apos;).
        Those cannot be redefined by this method!
        :param entityName: String
        :param replacementText: String
        :raises: XmlPullParserException
        See also:
        setInput(InputStream,String)
        FEATURE_PROCESS_DOCDECL
        FEATURE_VALIDATION
        """
        pass

    def getAttributeCount(self):
        """
        Returns the number of attributes of the current start tag, or -1 if
        the current event type is not START_TAG
        :return: int.
        See also:
        getAttributeNamespace(int)
        getAttributeName(int)
        getAttributePrefix(int)
        getAttributeValue(int)
        """
        pass

    def getAttributeName(self, index):
        """
        Returns the local name of the specified attribute if namespaces are
        enabled or just attribute name if namespaces are disabled. Throws an
        IndexOutOfBoundsException if the index is out of range or current
        event type is not START_TAG.
        :param index: int: zero-based index of attribute
        :return: String. attribute name (null is never returned)
        """
        pass

    def getAttributeNamespace(self, index):
        """
        Returns the namespace URI of the attribute with the given index
        (starts from 0). Returns an empty string ("") if namespaces are not
        enabled or the attribute has no namespace. Throws an
        IndexOutOfBoundsException if the index is out of range or the current
        event type is not START_TAG.
        NOTE: if FEATURE_REPORT_NAMESPACE_ATTRIBUTES is set then namespace
        attributes (xmlns:ns='...') must be reported with namespace
        http://www.w3.org/2000/xmlns/ (visit this URL for description!). The
        default namespace attribute (xmlns="...") will be reported with empty
        namespace.
        NOTE:The xml prefix is bound as defined in Namespaces in
        XML specification to "http://www.w3.org/XML/1998/namespace".
        :param index: int: zero-based index of attribute
        :return: String. attribute namespace, empty string ("") is returned
        if namespaces processing is not enabled or namespaces processing is
        enabled but attribute has no namespace (it has no prefix).
        """
        pass

    def getAttributePrefix(self, index):
        """
        Returns the prefix of the specified attribute. Returns null if the
        element has no prefix. If namespaces are disabled it will always
        return null. Throws an IndexOutOfBoundsException if the index is out
        of range or current event type is not START_TAG.
        :param index: int: zero-based index of attribute
        :return: String. attribute prefix or null if namespaces processing is
        not enabled.
        """
        pass

    def getAttributeType(self, index):
        """
        Returns the type of the specified attribute If parser is
        non-validating it MUST return CDATA.
        :param index: int: zero-based index of attribute
        :return: String. attribute type (null is never returned)
        """
        pass

    @overload('@str', 'str')
    def getAttributeValue(self, namespace, name):
        """
        Returns the attributes value identified by namespace URI and namespace
        localName. If namespaces are disabled namespace must be null. If
        current event type is not START_TAG then IndexOutOfBoundsException
        will be thrown.
        NOTE: attribute value must be normalized (including
        entity replacement text if PROCESS_DOCDECL is false) as described in
        XML 1.0 section 3.3.3 Attribute-Value Normalization
        :param namespace: String: Namespace of the attribute if namespaces
        are enabled otherwise must be nullname.
        :param name: String: If namespaces enabled local name of attribute
        otherwise just attribute name
        :return: String. value of attribute or null if attribute with given
        name does not exist
        See also:
        defineEntityReplacementText(String, String)
        """
        pass

    @getAttributeValue.adddef('int')
    def getAttributeValue(self, index):
        """
        Returns the given attributes value. Throws an
        IndexOutOfBoundsException if the index is out of range or current
        event type is not START_TAG.
        NOTE: attribute value must be normalized
        (including entity replacement text if PROCESS_DOCDECL is false) as
        described in XML 1.0 section 3.3.3 Attribute-Value Normalization
        :param index: int: zero-based index of attribute
        :return: String. value of attribute (null is never returned)
        See also:
        defineEntityReplacementText(String, String)
        """
        pass

    def getColumnNumber(self):
        """
        Returns the current column number, starting from 0. When the parser
        does not know the current column number or can not determine it,  -1
        is returned (e.g. for WBXML).
        :return: int. current column number or -1 if unknown.
        """
        pass

    def getDepth(self):
        """
        Returns the current depth of the element. Outside the root element,
        the depth is 0. The depth is incremented by 1 when a start tag is
        reached. The depth is decremented AFTER the end tag event was
        observed.
        <!-- outside -->        0
        <root>                  1
            sometext            1
                <foobar>        2
                </foobar>       2
        </root>                 1
        <!-- outside -->        0
        :return: int.
        """
        pass

    def getEventType(self):
        """
        Returns the type of the current event (START_TAG, END_TAG, TEXT, etc.)
        :return: int.
        :raises: XmlPullParserException
        See also:
        next()
        nextToken()
        """
        pass

    def getFeature(self, name):
        """
        Returns the current value of the given feature. Please note: unknown
        features are always returned as false.
        :param name: String: The name of feature to be retrieved.
        :return: boolean. The value of the feature.
        :raises:
        IllegalArgumentException: if string the feature name is null
        """
        pass

    def getInputEncoding(self):
        """
        Returns the input encoding if known, null otherwise. If
        setInput(InputStream, inputEncoding) was called with an inputEncoding
        value other than null, this value must be returned from this method.
        Otherwise, if inputEncoding is null and the parser supports the
        encoding detection feature
        (http://xmlpull.org/v1/doc/features.html#detect-encoding), it must
        return the detected encoding. If setInput(Reader) was called, null is
        returned. After first call to next if XML declaration was present this
        method will return encoding declared.
        :return: String.
        """
        pass

    def getLineNumber(self):
        """
        Returns the current line number, starting from 1. When the parser does
        not know the current line number or can not determine it,  -1 is
        returned (e.g. for WBXML).
        :return: int. current line number or -1 if unknown.
        """
        pass

    def getName(self):
        """
        For START_TAG or END_TAG events, the (local) name of the current
        element is returned when namespaces are enabled. When namespace
        processing is disabled, the raw name is returned. For ENTITY_REF
        events, the entity name is returned. If the current event is not
        START_TAG, END_TAG, or ENTITY_REF, null is returned. Please note: To
        reconstruct the raw element name when namespaces are enabled and the
        prefix is not null, you will need to  add the prefix and a colon to
        localName..
        :return: String.
        """
        pass

    @overload
    def getNamespace(self):
        """
        Returns the namespace URI of the current element. The default
        namespace is represented as empty string. If namespaces are not
        enabled, an empty String ("") is always returned. The current event
        must be START_TAG or END_TAG; otherwise, null is returned.
        :return: String.
        """
        pass

    @getNamespace.adddef('str')
    def getNamespace(self, prefix):
        """
        Returns the URI corresponding to the given prefix, depending on
        current state of the parser.  If the prefix was not declared in the
        current scope, null is returned. The default namespace is included in
        the namespace table and is available via getNamespace (null).  This
        method is a convenience method for   for (int i =
        getNamespaceCount(getDepth ())-1; i >= 0; i--) { if
        (getNamespacePrefix(i).equals( prefix )) { return getNamespaceUri(i);
        } } return null; Please note: parser implementations may provide more
        efficient lookup, e.g. using a Hashtable. The 'xml' prefix is bound to
        "http://www.w3.org/XML/1998/namespace", as defined in the Namespaces
        in XML specification. Analogous, the 'xmlns' prefix is resolved to
        http://www.w3.org/2000/xmlns/
        :param prefix: String
        :return: String.
        See also:
        getNamespaceCount(int)
        getNamespacePrefix(int)
        getNamespaceUri(int)
        """
        pass

    def getNamespaceCount(self, depth):
        """
        Returns the numbers of elements in the namespace stack for the given
        depth. If namespaces are not enabled, 0 is returned.  NOTE: when
        parser is on END_TAG then it is allowed to call this function with
        getDepth()+1 argument to retrieve position of namespace prefixes and
        URIs that were declared on corresponding START_TAG.
        NOTE: to retrieve list of namespaces declared in current element:
            XmlPullParser pp = ...
            int nsStart = pp.getNamespaceCount(pp.getDepth()-1);
            int nsEnd = pp.getNamespaceCount(pp.getDepth());
            for (int i = nsStart; i < nsEnd; i++) {
                String prefix = pp.getNamespacePrefix(i);
                String ns = pp.getNamespaceUri(i);
                // ...
            }
        :param depth: int
        :return: int.
        :raises: XmlPullParserException
        See also:
        getNamespacePrefix(int)
        getNamespaceUri(int)
        getNamespace()
        getNamespace(String)
        """
        pass

    def getNamespacePrefix(self, pos):
        """
        Returns the namespace prefix for the given position in the namespace
        stack. Default namespace declaration (xmlns='...') will have null as
        prefix. If the given index is out of range, an exception is thrown.
        Please note: when the parser is on an END_TAG, namespace prefixes that
        were declared in the corresponding START_TAG are still accessible
        although they are no longer in scope.
        :param pos: int
        :return: String.
        :raises: XmlPullParserException
        """
        pass

    def getNamespaceUri(self, pos):
        """
        Returns the namespace URI for the given position in the namespace
        stack If the position is out of range, an exception is thrown. NOTE:
        when parser is on END_TAG then namespace prefixes that were declared
        in corresponding START_TAG are still accessible even though they are
        not in scope
        :param pos: int
        :return: String.
        :raises: XmlPullParserException
        """
        pass

    def getPositionDescription(self):
        """
        Returns a short text describing the current parser state, including
        the position, a description of the current event and the data source
        if known. This method is especially useful to provide meaningful error
        messages and for debugging purposes.
        :return: String.
        """
        pass

    def getPrefix(self):
        """
        Returns the prefix of the current element. If the element is in the
        default namespace (has no prefix), null is returned. If namespaces are
        not enabled, or the current event is not  START_TAG or END_TAG, null
        is returned.
        :return: String.
        """
        pass

    def getProperty(self, name):
        """
        Look up the value of a property.  The property name is any
        fully-qualified URI. NOTE: unknown properties are always returned as
        null.
        :param name: String: The name of property to be retrieved.
        :return: Object. The value of named property.
        """
        pass

    def getText(self):
        """
        Returns the text content of the current event as String. The value
        returned depends on current event type, for example for TEXT event it
        is element content (this is typical case when next() is used).  See
        description of nextToken() for detailed description of possible
        returned values for different types of events.  NOTE: in case of
        ENTITY_REF, this method returns the entity replacement text (or null
        if not available). This is the only case where getText() and
        getTextCharacters() return different values.
        :return: String.
        See also:
        getEventType()
        next()
        nextToken()
        """
        pass

    def getTextCharacters(self, holderForStartAndLength):
        """
        Returns the buffer that contains the text of the current event, as
        well as the start offset and length relevant for the current event.
        See getText(), next() and nextToken() for description of possible
        returned values.  Please note: this buffer must not be modified and
        its content MAY change after a call to next() or nextToken(). This
        method will always return the same value as getText(), except for
        ENTITY_REF. In the case of ENTITY ref, getText() returns the
        replacement text and this method returns the actual input buffer
        containing the entity name. If getText() returns null, this method
        returns null as well and the values returned in the holder array MUST
        be -1 (both start and length).
        :param holderForStartAndLength: int: Must hold an 2-element int array
        into which the start offset and length values will be written.
        :return: char[]. char buffer that contains the text of the current
        event (null if the current event has no text associated).
        See also:
        getText()
        next()
        nextToken()
        """
        pass

    def isAttributeDefault(self, index):
        """
        Returns if the specified attribute was not in input was declared in
        XML. If parser is non-validating it MUST always return false. This
        information is part of XML infoset:
        :param index: int: zero-based index of attribute
        :return: boolean. false if attribute was in input
        """
        pass

    def isEmptyElementTag(self):
        """
        Returns true if the current event is START_TAG and the tag is
        degenerated (e.g. <foobar/>). NOTE: if the parser is not on START_TAG,
        an exception will be thrown.
        :return: boolean.
        :raises: XmlPullParserException
        """
        pass

    def isWhitespace(self):
        """
        Checks whether the current TEXT event contains only whitespace
        characters. For IGNORABLE_WHITESPACE, this is always true. For TEXT
        and CDSECT, false is returned when the current event text contains at
        least one non-white space character. For any other event type an
        exception is thrown.  Please note: non-validating parsers are not able
        to distinguish whitespace and ignorable whitespace, except from
        whitespace outside the root element. Ignorable whitespace is reported
        as separate event, which is exposed via nextToken only.
        :return: boolean.
        :raises: XmlPullParserException
        """
        pass

    def next(self):
        """
        Get next parsing event - element content will be coalesced and only
        one TEXT event must be returned for whole element content (comments
        and processing instructions will be ignored and entity references must
        be expanded or exception must be thrown if entity reference can not be
        expanded). If element content is empty (content is "") then no TEXT
        event will be reported.
        NOTE: empty element (such as <tag/>) will be
        reported with  two separate events: START_TAG, END_TAG - it must be so
        to preserve parsing equivalency of empty element to <tag></tag>. (see
        isEmptyElementTag ())
        :return: int.
        :raises: XmlPullParserException
        IOException
        See also:
        isEmptyElementTag()
        START_TAG
        TEXT
        END_TAG
        END_DOCUMENT
        """
        pass

    def nextTag(self):
        """
        Call next() and return event if it is START_TAG or END_TAG otherwise
        throw an exception. It will skip whitespace TEXT before actual tag if
        any.  essentially it does this

            int eventType = next();
            if(eventType == TEXT && isWhitespace()) {   // skip whitespace
                eventType = next();
            }
            if (eventType != START_TAG && eventType != END_TAG) {
                throw new XmlPullParserException("expected start or end tag", this, null);
            }
            return eventType;

        :return: int.
        :raises: XmlPullParserExceptionIOException
        """
        pass

    def nextText(self):
        """
        If current event is START_TAG then if next element is TEXT then
        element content is returned or if next event is END_TAG then empty
        string is returned, otherwise exception is thrown. After calling this
        function successfully parser will be positioned on END_TAG.  The
        motivation for this function is to allow to parse consistently both
        empty elements and elements that has non empty content, for example
        for input:
        <tag>foo</tag>
        <tag></tag> (which is equivalent to <tag/> both input can be parsed
                    with the same code:
            p.nextTag()
            p.require(p.START_TAG, "", "tag");
            String content = p.nextText();
            p.require(p.END_TAG, "", "tag");
        This function together with nextTag make it very easy to parse XML that
        has no mixed content.
        Essentially it does this

            if(getEventType() != START_TAG) {
                throw new XmlPullParserException( "parser must be on START_TAG to read next text", this, null);
            }
            int eventType = next();
            if(eventType == TEXT) {
                String result = getText();
                eventType = next();
                if(eventType != END_TAG) {
                    throw new XmlPullParserException( "event TEXT it must be immediately followed by END_TAG", this, null);
                }
                return result;
            } else if(eventType == END_TAG) {
                return "";
            } else {
                throw new XmlPullParserException( "parser must be on START_TAG or TEXT to read text", this, null);
            }

        Warning: Prior to API level 14, the pull parser
        returned by android.util.Xml did not always advance to the END_TAG
        event when this method was called. Work around by using manually
        advancing after calls to nextText(): String text = xpp.nextText(); if
        (xpp.getEventType() != XmlPullParser.END_TAG) { xpp.next(); }
        :return: String.
        :raises: XmlPullParserExceptionIOException
        """
        pass

    def nextToken(self):
        """
        This method works similarly to next() but will expose additional event
        types (COMMENT, CDSECT, DOCDECL, ENTITY_REF, PROCESSING_INSTRUCTION,
        or IGNORABLE_WHITESPACE) if they are available in input.  If special
        feature FEATURE_XML_ROUNDTRIP (identified by URI:
        http://xmlpull.org/v1/doc/features.html#xml-roundtrip) is enabled it
        is possible to do XML document round trip ie. reproduce exectly on
        output the XML input using getText(): returned content is always
        unnormalized (exactly as in input). Otherwise returned content is
        end-of-line normalized as described XML 1.0 End-of-Line Handling and.
        Also when this feature is enabled exact content of START_TAG, END_TAG,
        DOCDECL and PROCESSING_INSTRUCTION is available.  Here is the list of
        tokens that can be  returned from nextToken() and what getText() and
        getTextCharacters() returns:
        START_DOCUMENT
        null
        END_DOCUMENT
        null
        START_TAG
        null unless FEATURE_XML_ROUNDTRIP enabled and then returns
        XML tag, ex: <tag attr='val'>
        END_TAG
        null unless FEATURE_XML_ROUNDTRIP id enabled and then returns XML tag, ex: </tag>
        TEXT
        return element content.
        Note: that element content may be delivered in multiple
        consecutive TEXT events.
        IGNORABLE_WHITESPACE
        return characters that are determined to be ignorable white space. If the
        FEATURE_XML_ROUNDTRIP is enabled all whitespace content outside root
        element will always reported as IGNORABLE_WHITESPACE otherwise
        reporting is optional. Note: that element content may be delivered in
        multiple consecutive IGNORABLE_WHITESPACE events.
        CDSECT
        return text inside CDATA (ex. 'fo<o' from <!CDATA[fo<o]]>)
        PROCESSING_INSTRUCTION
        if FEATURE_XML_ROUNDTRIP is true return exact PI content ex: 'pi foo'
        from <?pi foo?> otherwise it may be exact PI content or concatenation
        of PI target, space and data so for example for <?target    data?>
        string "target data" may be returned if
        FEATURE_XML_ROUNDTRIP is false.
        COMMENT
        return comment content ex. 'foo bar' from <!--foo bar-->
        ENTITY_REF
        getText() MUST return entity replacement text if PROCESS_DOCDECL is
        false otherwise getText() MAY
        return null, additionally getTextCharacters() MUST return entity name
        (for example 'entity_name' for &entity_name;).
        NOTE: this is the only place where value returned from getText() and
        getTextCharacters() are different
        NOTE: it is user responsibility to resolve entity reference if
        PROCESS_DOCDECL is false and there is no entity
        replacement text set in defineEntityReplacementText() method
        (getText() will be null)
        NOTE: character entities (ex. &#32;) and standard entities such as
        &amp; &lt; &gt; &quot; &apos; are reported as well and are not reported
        as TEXT tokens but as ENTITY_REF tokens! This requirement is added to
        allow to do roundtrip of XML documents!
        DOCDECL
        if FEATURE_XML_ROUNDTRIP is true
        or PROCESS_DOCDECL is false then return what is inside of DOCDECL for
        example it returns:
        ' titlepage SYSTEM "http://www.foo.bar/dtds/typo.dtd" [<!ENTITY % active.links
        "INCLUDE">]'
        for input document that contained:
        <!DOCTYPE titlepage SYSTEM "http://www.foo.bar/dtds/typo.dtd" [<!ENTITY % active.links
        "INCLUDE">]>
        otherwise if FEATURE_XML_ROUNDTRIP is false and
        PROCESS_DOCDECL is true then what is returned is undefined (it may be
        even null)
        NOTE: there is no guarantee that there will only one TEXT
        or IGNORABLE_WHITESPACE event from nextToken() as parser may chose to
        deliver element content in multiple tokens (dividing element content
        into chunks)
        NOTE: whether returned text of token is end-of-line
        normalized is depending on FEATURE_XML_ROUNDTRIP.
        NOTE: XMLDecl(<?xml ...?>) is not reported but its content is available
        through optional properties (see class description above).
        :return: int.
        :raises: XmlPullParserExceptionIOException
        See also:
        next()
        START_TAG
        TEXT
        END_TAG
        END_DOCUMENT
        COMMENT
        DOCDECL
        PROCESSING_INSTRUCTION
        ENTITY_REF
        IGNORABLE_WHITESPACE
        """
        pass

    def require(self, atype, namespace, name):
        """
        Test if the current event is of the given type and if the namespace
        and name do match. null will match any namespace and any name. If the
        test is not passed, an exception is thrown. The exception text
        indicates the parser position, the expected event and the current
        event that is not meeting the requirement.  Essentially it does this
        if (type != getEventType() || (namespace != null &amp;&amp;
        !namespace.equals( getNamespace () ) ) || (name != null &amp;&amp;
        !name.equals( getName() ) ) ) throw new XmlPullParserException(
        "expected "+ TYPES[ type ]+getPositionDescription());
        :param atype: int
        :param namespace: String
        :param name: String
        :raises: XmlPullParserException, IOException
        """
        pass

    def setFeature(self, name, state):
        """
        Use this call to change the general behaviour of the parser, such as
        namespace processing or doctype declaration handling. This method must
        be called before the first call to next or nextToken. Otherwise, an
        exception is thrown. Example: call
        setFeature(FEATURE_PROCESS_NAMESPACES, true) in order to switch on
        namespace processing. The initial settings correspond to the
        properties requested from the XML Pull Parser factory. If none were
        requested, all features are deactivated by default.
        :param name: String
        :param state: boolean
        :raises:
        XmlPullParserException: If the feature is not supported or can
        not be set.
        IllegalArgumentException: If string with the feature name is
        null.
        """
        pass

    @overload('@str')
    def setInput(self, reader_in):
        """
        Set the input source for parser to the given reader and resets the
        parser. The event type is set to the initial value START_DOCUMENT.
        Setting the reader to null will just stop parsing and reset parser
        state, allowing the parser to free internal resources such as parsing
        buffers.
        :param reader_in: Reader
        :raises: XmlPullParserException
        """
        pass

    @setInput.adddef('str', '@str')
    def setInput(self, inputStream, inputEncoding):
        """
        Sets the input stream the parser is going to process. This call resets
        the parser state and sets the event type to the initial value
        START_DOCUMENT.
        NOTE: If an input encoding string is passed, it MUST
        be used. Otherwise, if inputEncoding is null, the parser SHOULD try to
        determine input encoding following XML 1.0 specification (see below).
        If encoding detection is supported then following feature
        http://xmlpull.org/v1/doc/features.html#detect-encoding MUST be true
        amd otherwise it must be false
        :param inputStream: InputStream: contains a raw byte input stream of
        possibly unknown encoding (when inputEncoding is null).
        :param inputEncoding: String: if not null it MUST be used as encoding
        for inputStream
        :raises: XmlPullParserException
        """
        pass

    def setProperty(self, name, value):
        """
        Set the value of a property.  The property name is any fully-qualified
        URI.
        :param name: String
        :param value: Object
        :raises:
        XmlPullParserException: If the property is not supported or can
        not be set
        IllegalArgumentException: If string with the property name is null
        """
        pass
