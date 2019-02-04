# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/java/util/Locale"""
import itertools
import re
import threading
import locale as pylocale

from Android import Object, overload, AndroidEnum
from LanguageTag import LanguageTag


class Locale(Object):
    """
    A Locale object represents a specific geographical, political, or cultural
    region. An operation that requires a Locale to perform its task is called
    locale-sensitive and uses the Locale to tailor information for the user.
    For example, displaying a number is a locale-sensitive operation— the number
    should be formatted according to the customs and conventions of the user's
    native country, region, or culture.
    """
    """
    public static final char PRIVATE_USE_EXTENSION:
    The key for the private use extension ('x').See 
    also:getExtension(char)Locale.Builder.setExtension(char, String)
    """
    PRIVATE_USE_EXTENSION = 0x00000078

    """
    public static final char UNICODE_LOCALE_EXTENSION:
    The key for Unicode locale extension ('u').See 
    also:getExtension(char)Locale.Builder.setExtension(char, String)
    """
    UNICODE_LOCALE_EXTENSION = 0x00000075

    """
    public static final Locale CANADA:
    Useful constant for country.
    """
    CANADA = ('en', 'CA')

    """
    public static final Locale CANADA_FRENCH:
    Useful constant for country.
    """
    CANADA_FRENCH = ('fr', 'CA')

    """
    public static final Locale CHINA:
    Useful constant for country.
    """
    CHINA = ('zh', 'CN')

    """
    public static final Locale CHINESE:
    Useful constant for language.
    """
    CHINESE = ('zh',)

    """
    public static final Locale ENGLISH:
    Useful constant for language.
    """
    ENGLISH = ('en', )

    """
    public static final Locale FRANCE:
    Useful constant for country.
    """
    FRANCE = ('fr', 'FR')

    """
    public static final Locale FRENCH:
    Useful constant for language.
    """
    FRENCH = ('fr',)

    """
    public static final Locale GERMAN:
    Useful constant for language.
    """
    GERMAN = ('de', )

    """
    public static final Locale GERMANY:
    Useful constant for country.
    """
    GERMANY = ('de', 'DE')

    """
    public static final Locale ITALIAN:
    Useful constant for language.
    """
    ITALIAN = ('it', )

    """
    public static final Locale ITALY:
    Useful constant for country.
    """
    ITALY = ('it', 'IT')

    """
    public static final Locale JAPAN:
    Useful constant for country.
    """
    JAPAN = ('ja', 'JP')

    """
    public static final Locale JAPANESE:
    Useful constant for language.
    """
    JAPANESE = ('ja',)

    """
    public static final Locale KOREA:
    Useful constant for country.
    """
    KOREA = ('ko', 'KR')

    """
    public static final Locale KOREAN:
    Useful constant for language.
    """
    KOREAN = ('ko',)

    """
    public static final Locale PRC:
    Useful constant for country.
    """
    PRC = ('en', 'US')

    """
    public static final Locale ROOT:
    Useful constant for the root locale.  The root locale is the locale whose
    language, country, and variant are empty ("") strings.  This is regarded
    as the base locale of all locales, and is used as the language/country
    neutral locale for the locale sensitive operations.
    """
    ROOT = ('', )

    """
    public static final Locale SIMPLIFIED_CHINESE:
    Useful constant for language.
    """
    SIMPLIFIED_CHINESE = ('zh', 'CN')

    """
    public static final Locale TAIWAN:
    Useful constant for country.
    """
    TAIWAN = ('zh', 'TW')

    """
    public static final Locale TRADITIONAL_CHINESE:
    Useful constant for language.
    """
    TRADITIONAL_CHINESE = ('zh', 'TW')

    """
    public static final Locale UK:
    Useful constant for country.
    """
    UK = ('en', 'UK')

    """
    public static final Locale US:
    Useful constant for country.
    """
    US = ('en', 'US')

    SEP = '_'

    sLock = threading.RLock()

    _instances = {}

    _defaultLocale = None
    _defaultDisplayLocale = None
    _defaultFormatLocale = None

    class LocaleKey(Object):
        @overload('str', '@str', '@str', '@str', '@dict', 'bool')
        def __init__(self, language, script, region, variant, extensions, normalized):
            super(Locale.LocaleKey, self).__init__()
            self.lang = language or ''
            self.scrt = script or ''
            self.regn = region or ''
            self.vart = variant or ''
            self.normalized = normalized
            self.extensions = extensions or {}
            hash = reduce(
                lambda t, x: t + (x.__hash__() if x is not None else 0),
                (language, script, region, variant),
                0
            )
            hash ^= reduce(
                lambda t, x: t + (x.__hash__() if x is not None else 0),
                itertools.chain.from_iterable(self.extensions.items()),
                0
            )
            self.hash = hash

        @__init__.adddef('str', '@str', '@str', '@str')
        def __init__(self, language, script, region, variant):
            return self.__init__(language, script, region, variant, None, False)

        @classmethod
        def normalize(cls, key):
            if key.normalized: return key
            lang = key.lang.lower()
            scrt = key.scrt.title()
            regn = key.regn.upper()
            vart = key.vart
            exts = key.extensions or {}
            exts = {x[0].lower():x[1].lower() for x in exts.items()}
            return cls(lang, scrt, regn, vart, exts, True)

        def hashCode(self):
            return self.hash

        def equals(self, obj):
            if id(self) == id(obj): return True
            bFlag = isinstance(obj, Locale.LocaleKey) and self.hash == obj.hash
            if not bFlag: return False
            it = itertools.dropwhile(
                lambda x: x[0].lower() == x[1].lower(),
                ((self.lang, obj.lang),
                 (self.scrt, obj.scrt),
                 (self.regn, obj.regn),
                 (self.vart, obj.vart),
                 (self.extensions, obj.extensions))
            )
            try:
                it.next()
                return False
            except:
                return True

        def __hash__(self):
            return self.hashCode()

        def __eq__(self, other):
            return self.equals(other)

    class Builder(Object):
        """
        Builder is used to build instances of Locale from values configured by
        the setters. Unlike the Locale constructors, the Builder checks if a value
        configured by a setter satisfies the syntax requirements defined by the
        Locale class. A Locale object created by a Builder is well-formed and can be
        transformed to a well-formed IETF BCP 47 language tag without losing
        information.
        """
        def __init__(self):
            super(Locale.Builder, self).__init__()
            self.clear()
            pass

        def addUnicodeLocaleAttribute(self, attribute):
            """
            Adds a unicode locale attribute, if not already present, otherwise has
            no effect.  The attribute must not be null and must be well-formed or
            an exception is thrown.
            :param attribute: String: the attribute
            :return: Locale.Builder. This builder.
            :raises:
            NullPointerException: if attribute is null
            IllformedLocaleException: if attribute is ill-formed
            See also:
            setExtension(char, String)
            """
            if not attribute:
                raise Exception('NullPointerException: "attribute must not be None"')
            predicate = re.compile(r'[0-9a-zA-z]{3,8}$').match
            if not predicate(attribute):
                raise Exception('IllformedLocaleException: "ill formed attribute %s"' % attribute)
            self.uattributes.add(attribute.lower())
            return self

        def build(self):
            """
            Returns an instance of Locale created from the fields set on this
            builder.  This applies the conversions listed in
            Locale.forLanguageTag(String) when constructing a Locale.
            (Grandfathered tags are handled in setLanguageTag(String).)
            :return: Locale. A Locale.
            """
            ltag = LanguageTag
            language = ltag.canonicalizeLanguage(self.language)
            script = ltag.canonicalizeScript(self.script or '')
            region = ltag.canonicalizeRegion(self.region or '')
            variants = (self.variants or '').replace(LanguageTag.SEP, Locale.SEP)
            variants = ltag.canonicalizeVariant(variants)
            if self.extensions and self.extensions.has_key(LanguageTag.PRIVATEUSE):
                privuse = self.extensions.pop(LanguageTag.PRIVATEUSE)
                pattern = r'\b%s\b' % LanguageTag.PRIVUSE_VARIANT_PREFIX
                try:
                    privuse, lvariant = re.split(pattern, privuse, 1)
                    if lvariant:
                        variants += lvariant
                        variants = variants.strip(LanguageTag.SEP).replace(LanguageTag.SEP, Locale.SEP)
                except:
                    pass
                if privuse:
                    privuse = privuse.lower()
                    self.extensions[LanguageTag.PRIVATEUSE] = privuse.strip(LanguageTag.SEP)
            ule = ''
            if self.uattributes:
                uattributes = sorted(self.uattributes)
                ule += Locale.SEP.join(sorted(uattributes))
            if self.ukeywords:
                ukeywords = itertools.chain.from_iterable(sorted(self.ukeywords.items()))
                ule += Locale.SEP.join(ukeywords)
            if ule:
                self.extensions['u'] = ule
            extensions = {key:value.replace(LanguageTag.SEP, Locale.SEP) for key, value in self.extensions.items()}
            instance = Locale(language, script, region, variants, extensions)
            instance.normalized = True
            return instance

        def clear(self):
            """
            Resets the builder to its initial, empty state.
            :return: Locale.Builder. This builder.
            """
            self.language = ''
            self.script = ''
            self.region = ''
            self.variants = ''
            return self.clearExtensions()

        def clearExtensions(self):
            """
            Resets the extensions to their initial, empty state. Language, script,
            region and variant are unchanged.
            :return: Locale.Builder. This builder.
            See also: setExtension(char, String)
            """
            self.extensions = dict()
            self.uattributes = set()
            self.ukeywords = dict()
            return self

        def removeUnicodeLocaleAttribute(self, attribute):
            """
            Removes a unicode locale attribute, if present, otherwise has no
            effect.  The attribute must not be null and must be well-formed or an
            exception is thrown.  Attribute comparision for removal is
            case-insensitive.
            :param attribute: String: the attribute
            :return: Locale.Builder. This builder.
            :raises: NullPointerExceptionif attribute is
            nullIllformedLocaleExceptionif attribute is ill-formed
            See also: setExtension(char, String)
            """
            if not attribute:
                raise Exception('NullPointerException: "attribute must not be None"')
            predicate = re.compile(r'[0-9a-zA-z]{3,8}$').match
            if not predicate(attribute):
                raise Exception('IllformedLocaleException: "ill formed attribute %s"' % attribute)
            self.uattributes.discard(attribute.lower())
            pass

        def setExtension(self, key, value):
            """
            Sets the extension for the given key. If the value is null or the
            empty string, the extension is removed.  Otherwise, the extension must
            be well-formed or an exception is thrown.  Note: The key
            UNICODE_LOCALE_EXTENSION ('u') is used for the Unicode locale
            extension. Setting a value for this key replaces any existing Unicode
            locale key/type pairs with those defined in the extension.  Note: The
            key PRIVATE_USE_EXTENSION ('x') is used for the private use code. To
            be well-formed, the value for this key needs only to have subtags of
            one to eight alphanumeric characters, not two to eight as in the
            general case.
            :param key: char: the extension key
            :param value: String: the extension value
            :return: Locale.Builder. This builder.
            :raises: IllformedLocaleExceptionif key is illegal or value is
            ill-formed
            See also:
            setUnicodeLocaleKeyword(String, String)
            """
            isPrivateUse = key == LanguageTag.PRIVATEUSE
            if not isPrivateUse and not LanguageTag.isExtension(key):
                raise Exception('LocaleSyntaxException: "Ill-formed extension key: %s"' % key)
            if not value:
                if key == 'u':
                    self.uattributes = set()
                    self.ukeywords = dict()
                else:
                    try:
                        key = key.lower()
                        self.extensions.pop(key)
                    except:
                        pass
            else:
                value = value.replace(Locale.SEP, LanguageTag.SEP)
                predicate = LanguageTag.isPrivateUseSubtag if isPrivateUse else LanguageTag.isExtensionSubtag
                res, dmy = LanguageTag._parseComponent(value, predicate, LanguageTag.SEP)
                if res:
                    raise Exception('LocaleSyntaxException: "Ill-formed extension value: %s"' % res)
                if key == 'u':
                    self.uattributes = set()
                    self.ukeywords = dict()
                    ext = value.split(LanguageTag.SEP)
                    k = 0
                    while k < len(ext):
                        try:
                            self.addUnicodeLocaleAttribute(ext[k])
                            k += 1
                        except:
                            break
                    while k < len(ext) - 1:
                        key = ext[k]
                        k += 1
                        utype = ext[k] if len(ext[k]) > 2 else ''
                        if utype:
                            self.setUnicodeLocaleKeyword(key, utype)
                            k += 1
                else:
                    key = key.lower()
                    self.extensions[key] = value if isPrivateUse else value.lower()
            return self

        def setLanguage(self, language):
            """
            Sets the language.  If language is the empty string or null, the
            language in this Builder is removed.  Otherwise, the language must be
            well-formed or an exception is thrown.  The typical language value is
            a two or three-letter language code as defined in ISO639.
            :param language: String: the language
            :return: Locale.Builder. This builder.
            :raises: IllformedLocaleExceptionif language is ill-formed
            """
            if not language:
                language = ''
            elif not LanguageTag.isLanguage(language):
                raise Exception('LocaleSyntaxException: "Ill-formed language: %s"' % language)
            self.language = language
            return self

        def setLanguageTag(self, languageTag):
            """
            Resets the Builder to match the provided IETF BCP 47 language tag.
            Discards the existing state.  Null and the empty string cause the
            builder to be reset, like clear().  Grandfathered tags (see
            Locale.forLanguageTag(String)) are converted to their canonical form
            before being processed.  Otherwise, the language tag must be
            well-formed (see Locale) or an exception is thrown (unlike
            Locale.forLanguageTag, which just discards ill-formed and following
            portions of the tag).
            :param languageTag: String: the language tag
            :return: Locale.Builder. This builder.
            :raises: IllformedLocaleException: If languageTag is ill-formed
            See also: Locale.forLanguageTag(String)
            """
            if not languageTag:
                self.clear()
                return self
            tag, status = LanguageTag.parse(languageTag)
            if status != 'OK':
                raise Exception('IllformedLocaleException: "%s"' % status)
            self.clear()
            extLangs = tag.getExtlangs()
            if extLangs:
                self.language = extLangs[0]
            else:
                lang = tag.getLanguage()
                if lang != LanguageTag.UNDETERMINED:
                    self.language = lang
            self.script = tag.getScript()
            self.region = tag.getRegion()
            self.variants = Locale.SEP.join(tag.getVariants())

            tagext = tag.getExtensions() or []
            privateUse = tag.getPrivateuse()
            if privateUse:
                tagext.append(privateUse)
            map(lambda x: self.setExtension(*x.split(LanguageTag.SEP, 1)), tagext)
            return self

        def setLocale(self, locale):
            """
            Resets the Builder to match the provided locale.  Existing state is
            discarded.  All fields of the locale must be well-formed, see Locale.
            Locales with any ill-formed fields cause IllformedLocaleException to
            be thrown, except for the following three cases which are accepted for
            compatibility reasons:Locale("ja", "JP", "JP") is treated as
            "ja-JP-u-ca-japanese" Locale("th", "TH", "TH") is treated as
            "th-TH-u-nu-thai" Locale("no", "NO", "NY") is treated as "nn-NO"
            :param locale: Locale: the locale
            :return: Locale.Builder. This builder.
            :raises:
            NullPointerException: if locale is null.
            IllformedLocaleException: if locale has any ill-formed fields.
            """
            if not locale:
                raise Exception('NullPointerException: "locale is None"')
            self.setLanguage(locale.getLanguage())
            self.setScript(locale.getScript())
            self.setRegion(locale.getCountry())
            self.setVariant(locale.getVariant())
            self.clearExtensions()
            map(lambda x: self.setExtension(x, locale.getExtension(x)), locale.getExtensionKeys())
            return self

        def setRegion(self, region):
            """
            Sets the region.  If region is null or the empty string, the region in
            this Builder is removed.  Otherwise, the region must be well-formed or
            an exception is thrown.  The typical region value is a two-letter ISO
            3166 code or a three-digit UN M.49 area code.  The country value in
            the Locale created by the Builder is always normalized to upper case.
            :param region: String: the region
            :return: Locale.Builder. This builder.
            :raises: IllformedLocaleExceptionif region is ill-formed
            """
            if not region:
                region = ''
            elif not LanguageTag.isRegion(region):
                raise Exception('LocaleSyntaxException: "Ill-formed region: %s"' % region)
            self.region = region
            return self

        def setScript(self, script):
            """
            Sets the script. If script is null or the empty string, the script in
            this Builder is removed. Otherwise, the script must be well-formed or
            an exception is thrown.  The typical script value is a four-letter
            script code as defined by ISO 15924.
            :param script: String: the script
            :return: Locale.Builder. This builder.
            :raises: IllformedLocaleExceptionif script is ill-formed
            """
            if not script:
                script = ''
            elif not LanguageTag.isScript(script):
                raise Exception('LocaleSyntaxException: "Ill-formed script: %s"' % script)
            self.script = script
            return self

        def setUnicodeLocaleKeyword(self, key, utype):
            """
            Sets the Unicode locale keyword type for the given key.  If the type
            is null, the Unicode keyword is removed.  Otherwise, the key must be
            non-null and both key and type must be well-formed or an exception is
            thrown.  Keys and types are converted to lower case.  Note:Setting the
            'u' extension via setExtension(char, String) replaces all Unicode
            locale keywords with those defined in the extension.
            :param key: String: the Unicode locale key
            :param utype: String: the Unicode locale type
            :return: Locale.Builder. This builder.
            :raises:
                IllformedLocaleException: if key or type is ill-formed
                NullPointerException: if key is null
            See also:
            setExtension(char, String)
            """
            if not key:
                raise Exception('NullPointerException: "key is null"')
            predicate = re.compile(r'[0-9a-zA-z]{2}$').match
            if not predicate(key):
                raise  Exception('IllformedLocaleException: "ill formed key %s"' % key)
            key = key.lower()
            if not utype:
                if self.ukeywords.has_key(key):
                    self.ukeywords.pop(key)
            else:
                predicate = re.compile(r'[0-9a-zA-z]{3,8}$').match
                if not predicate(utype):
                    raise Exception('IllformedLocaleException: "ill formed type %s"' % utype)
                self.ukeywords[key] = utype.lower()
            return self

        def setVariant(self, variants):
            """
            Sets the variant.  If variant is null or the empty string, the variant
            in this Builder is removed.  Otherwise, it must consist of one or more
            well-formed subtags, or an exception is thrown.  Note: This method
            checks if variant satisfies the IETF BCP 47 variant subtag's syntax
            requirements, and normalizes the value to lowercase letters.  However,
            the Locale class does not impose any syntactic restriction on variant,
            and the variant value in Locale is case sensitive.  To set such a
            variant, use a Locale constructor.
            :param variant: String: the variant
            :return: Locale.Builder. This builder.
            :raises: IllformedLocaleExceptionif variant is ill-formed
            """
            if not variants:
                variants = ''
            else:
                residual, dmy = LanguageTag._parseComponent(variants, LanguageTag.isVariant, Locale.SEP)
                if residual:
                    raise Exception('LocaleSyntaxException: "Ill-formed variant: %s"' % residual)
            self.variants = variants
            return self

    @AndroidEnum
    class Category(Object):
        """
        Enum for locale categories. These locale categories are used to get/set
        the default locale for the specific functionality represented by the
        category.
        """
        """
        public static final Locale.Category DISPLAY
        Category used to represent the default locale for displaying user interfaces.
        """
        DISPLAY = (1,)

        """
        public static final Locale.Category FORMAT
        Category used to represent the default locale for formatting dates, 
        numbers, and/or currencies.
        """
        FORMAT = (2,)

        def __init__(self, value):
            super(self.__class__, self).__init__()
            self._value = value

        @classmethod
        def valueOf(self, name):
            """
            :param name: String
            :return: Locale.Category.
            """
            return getattr(self, name.upper(), None)

        @classmethod
        def values(self):
            """
            :return: Category[].
            """
            names = sorted(filter(lambda x: x.isupper(), vars(self)))
            return map(self.valueOf, names)

    @AndroidEnum
    class FilteringMode(Object):
        """
        public static final Locale.FilteringMode AUTOSELECT_FILTERING
        Specifies automatic filtering mode based on the given Language Priority
        List consisting of language ranges. If all of the ranges are basic,
        basic filtering is selected. Otherwise, extended filtering is selected.
        """
        AUTOSELECT_FILTERING = (1,)

        """
        public static final Locale.FilteringMode EXTENDED_FILTERING
        Specifies extended filtering.
        """
        EXTENDED_FILTERING = (2,)

        """
        public static final Locale.FilteringMode IGNORE_EXTENDED_RANGES
        Specifies basic filtering: Note that any extended language ranges included 
        in the given Language Priority List are ignored.
        """
        IGNORE_EXTENDED_RANGES = (3,)

        """
        public static final Locale.FilteringMode MAP_EXTENDED_RANGES
        Specifies basic filtering: If any extended language ranges are included 
        in the given Language Priority List, they are mapped to the basic 
        language range. Specifically, a language range starting with a 
        subtag "*" is treated as a language range "*". For example, "*-US" is 
        treated as "*". If "*" is not the first subtag, "*" and extra "-" are 
        removed. For example, "ja-*-JP" is mapped to "ja-JP".
        """
        MAP_EXTENDED_RANGES = (4,)

        """
        public static final Locale.FilteringMode REJECT_EXTENDED_RANGES
        Specifies basic filtering: If any extended language ranges are included 
        in the given Language Priority List, the list is rejected and the 
        filtering method throws IllegalArgumentException.
        """
        REJECT_EXTENDED_RANGES = (5,)

        def __init__(self, value):
            super(self.__class__, self).__init__()
            self._value = value

        @classmethod
        def valueOf(self, name):
            """
            :param name: String
            :return: Locale.Category.
            """
            return getattr(self, name.upper(), None)

        @classmethod
        def values(self):
            """
            :return: Category[].
            """
            names = sorted(filter(lambda x: x.isupper(), vars(self)))
            return map(self.valueOf, names)

    class LanguageRange(Object):
        """
        This class expresses a Language Range defined in RFC 4647 Matching of
        Language Tags. A language range is an identifier which is used to select
        language tag(s) meeting specific requirements by using the mechanisms
        described in Locale Matching. A list which represents a user's preferences
        and consists of language ranges is called a Language Priority List.
        """

        """
        public static final double MAX_WEIGHT:
        A constant holding the maximum value of weight, 1.0, which indicates
        that the language range is a good fit for the user.
        """
        MAX_WEIGHT = 1.0
        """
        public static final double MIN_WEIGHT:
        A constant holding the minimum value of weight, 0.0, which indicates
        that the language range is not a good fit for the user.
        """
        MIN_WEIGHT = 0.0

        @overload('str')
        def __init__(self, range):
            """
            :param range: String.
            """
            return self.__init__(range, self.MAX_WEIGHT)

        @__init__.adddef('str', 'float')
        def __init__(self, range, weight):
            """
            :param range: String.
            :param weight: double.
            """
            if not range:
                raise Exception('NullPointerException')
            if weight < self.MIN_WEIGHT or weight > self.MAX_WEIGHT:
                raise Exception('IllegalArgumentException: "weight=%s"' % weight)
            range = range.lower()
            basicPattern = r'(?:(?:[a-z]{1,8}(?:-[0-9a-z]{1,8})*)|\*)$'
            extPattern = r'(?:[a-z]{1,8}|\*)(?:-(?:[0-9a-z]{1,8}|\*))*$'
            if not re.match(basicPattern, range) and not re.match(extPattern, range):
                raise Exception('IllegalArgumentException: "range=%s"' % range)
            self.range = range
            self.weight = weight
            self.hash = None

        def equals(self, obj):
            """
            Compares this object to the specified object. The result is true if
            and only if the argument is not null and is a LanguageRange object
            that contains the same range and weight values as this object.
            :param obj: Object: the object to compare with
            :return: boolean. true if this object's range and weight are the same
            as the obj's; false otherwise.
            """
            if id(self) == id(obj): return True
            if not isinstance(obj, self.__class__): return False
            bFlag =  self.hash == obj.hash and \
                     self.getRange() == obj.getRange() and \
                     abs(self.getWeight() - obj.getWeight()) < 0.01
            return bFlag

        def __eq__(self, other):
            return self.equals(other)

        def getRange(self):
            """
            Returns the language range of this LanguageRange.
            :return: String. the language range.
            """
            return self.range

        def getWeight(self):
            """
            Returns the weight of this LanguageRange.
            :return: double. the weight value.
            """
            return self.weight

        def hashCode(self):
            """
            Returns a hash code value for the object.
            :return: int. a hash code value for this object.
            """
            if not self.hash:
                hash = self.getRange().__hash__()
                hash ^= self.getWeight().__hash__()
                self.hash = hash
            return self.hash

        @classmethod
        def mapEquivalents(cls, priorityList, map):
            """
            Generates a new customized Language Priority List using the given
            priorityList and map. If the given map is empty, this method returns a
            copy of the given priorityList.  In the map, a key represents a
            language range whereas a value is a list of equivalents of it. '*'
            cannot be used in the map. Each equivalent language range has the same
            weight value as its original language range.   An example of map:

            Key                             Value
            "zh" (Chinese)                  "zh", "zh-Hans"(Simplified Chinese)
            "zh-HK" (Chinese, Hong Kong)    "zh-HK"
            "zh-TW" (Chinese, Taiwan)       "zh-TW"

            The customization is performed after modification using the IANA
            Language Subtag Registry. For example, if a user's Language Priority List
            consists of five language ranges
            ("zh", "zh-CN", "en", "zh-TW", and "zh-HK"), the newly generated
            Language Priority List which is customized using the above map example
            will consists of "zh", "zh-Hans", "zh-CN", "zh-Hans-CN", "en",
            "zh-TW", and "zh-HK".  "zh-HK" and "zh-TW" aren't converted to
            "zh-Hans-HK" nor "zh-Hans-TW" even if they are included in the
            Language Priority List. In this example, mapping is used to clearly
            distinguish Simplified Chinese and Traditional Chinese.  If the
            "zh"-to-"zh" mapping isn't included in the map, a simple replacement
            will be performed and the customized list won't include "zh" and
            "zh-CN".
            :param priorityList: List: user's Language Priority ListmapMap: a map
            containing information to customize language ranges
            :return: List<Locale.LanguageRange>. a new Language Priority List with
            customization. The list is modifiable.
            :raises: NullPointerException: if priorityList is null
            See also: parse(String, Map)
            """
            from LocaleMatcher import LocaleMatcher
            return LocaleMatcher.mapEquivalents(priorityList, map)

        @overload('str')
        @classmethod
        def parse(cls, ranges):
            """
            Parses the given ranges to generate a Language Priority List.  This
            method performs a syntactic check for each language range in the given
            ranges but doesn't do validation using the IANA Language Subtag
            Registry.  The ranges to be given can take one of the following forms:
              "Accept-Language: ja,en;q=0.4"  (weighted list with Accept-Language prefix)
              "ja,en;q=0.4"                   (weighted list)
              "ja,en"                         (prioritized list)
            In a weighted list, each language range is given a weight value. The
            weight value is identical to the "quality value" in RFC 2616, and it
            expresses how much the user prefers  the language.
            A weight value is specified after a corresponding language range
            followed by ";q=", and the default weight value is MAX_WEIGHT when it
            is omitted.
            Unlike a weighted list, language ranges in a prioritized list are
            sorted in the descending order based on its priority. The first
            language range has the highest priority and meets the user's preference
            most.
            In either case, language ranges are sorted in descending order in the
            Language Priority List based on priority or weight. If a language range
            appears in the given ranges more than once, only the first one is
            included on the Language Priority List.  The returned list consists of
            language ranges from the given ranges and their equivalents found in
            the IANA Language Subtag Registry. For example, if the given ranges is
            "Accept-Language: iw,en-us;q=0.7,en;q=0.3", the elements in the list
            to be returned are:
                Range                                  Weight
                "iw" (older tag for Hebrew)             1.0
                "he" (new preferred code for Hebrew)    1.0
                "en-us" (English, United States)        0.7
                "en" (English)                          0.3
            Two language ranges, "iw" and "he", have the same highest priority in
            the list. By adding "he" to the user's Language Priority List,
            locale-matching method can find Hebrew as a matching locale (or
            language tag) even if the application or system offers only "he" as a
            supported locale (or language tag).
            :param ranges: String: a list of comma-separated language ranges or a
            list of language ranges in the form of the "Accept-Language" header
            defined in RFC 2616
            :return: List<Locale.LanguageRange>. a Language Priority List
            consisting of language ranges included in the given ranges and their
            equivalent language ranges if available. The list is modifiable.
            :raises: NullPointerExceptionif ranges is
            nullIllegalArgumentExceptionif a language range or a weight found in
            the given ranges is ill-formed
            """
            from LocaleMatcher import LocaleMatcher
            return LocaleMatcher.parse(ranges)

        @parse.adddef('str', 'dict')
        @classmethod
        def parse(cls, ranges, map):
            """
            Parses the given ranges to generate a Language Priority List, and then
            customizes the list using the given map. This method is equivalent to
            mapEquivalents(parse(ranges), map).
            :param ranges: String: a list of comma-separated language ranges or a list of
            language ranges in the form of the "Accept-Language" header defined in
            RFC 2616.
            :param map: Map: a map containing information to customize language
            ranges
            :return: List<Locale.LanguageRange>. a Language Priority List with
            customization. The list is modifiable.
            :raises:
            NullPointerException: if ranges is None.
            IllegalArgumentException: if a language range or a weight found in
            the given ranges is ill-formed
            See also:
            parse(String)
            mapEquivalents(List, Map)
            """
            return cls.mapEquivalents(cls.parse(ranges), map)

    def __new__(cls, *args, **kwargs):
        LocaleKey = Locale.LocaleKey
        if len(args) <= 3:
            script = ''
            extensions = None
            language, country, variant  = (args + ('', ''))[:3]
        else:
            language, script, country, variant, extensions  = args
        # Casos especiales
        if not extensions and language.lower() == 'ja' and \
                not script and country.upper() == 'JP' and variant == 'JP':
            variant = ''
            extensions = {'u': 'ca_japanese'}
        elif not extensions and language.lower() == 'th' and \
                not script and country.upper() == 'TH' and variant == 'TH':
            variant = ''
            extensions = {'u': 'nu_thai'}
        key = LocaleKey.normalize(LocaleKey(language, script, country, variant, extensions, False))
        if cls._instances.has_key(key):
            self = cls._instances[key]
        else:
            cls._instances[key] = self = super(Locale, cls).__new__(cls, *args, **kwargs)
            self._lang = key.lang
            self._scrt = key.scrt
            self._regn = key.regn
            self._vart = key.vart
            self._extensions = key.extensions
            self._languageTag = ''
        return self

    @overload('str', 'str', 'str')
    def __init__(self, language, country, variant):
        """
        :param language: String.
        :param country: String.
        :param variant:String.
        """
        self.__init__(language, '', country, variant, None)
        pass

    @__init__.adddef('str', 'str')
    def __init__(self, language, country):
        """
        :param language: String.
        :param country: String.
        """
        self.__init__(language, '', country, '', None)

    @__init__.adddef('str')
    def __init__(self, language):
        """
        :param language: String.
        """
        self.__init__(language, '', '', '', None)

    @__init__.adddef('str', '@str', '@str', '@str', '@dict')
    def __init__(self, language, script, country, variant, extensions):
        super(Locale, self).__init__()
        pass

    def clone(self):
        """
        Overrides Cloneable.
        :return: Object. a clone of this instance.
        """
        return self

    def equals(self, obj):
        """
        Returns true if this Locale is equal to another object.  A Locale is
        deemed equal to another Locale with identical language, script,
        country, variant and extensions, and unequal to all other objects.
        :param obj: Object: the reference object with which to compare.
        :return: boolean. true if this Locale is equal to the specified object.
        """
        pass

    @overload('list', 'set')
    @classmethod
    def filter(cls, priorityList, locales):
        """
        Returns a list of matching Locale instances using the filtering
        mechanism defined in RFC 4647. This is equivalent to filter(List,
        Collection, FilteringMode) when mode is
        Locale.FilteringMode.AUTOSELECT_FILTERING.
        :param priorityList: List: user's Language Priority List in which each
        language tag is sorted in descending order based on priority or weight
        :param locales: Collection: Locale instances used for matching
        :return: List<Locale>. a list of Locale instances for matching
        language tags sorted in descending order based on priority or weight,
        or an empty list if nothing matches. The list is modifiable.
        :raises NullPointerException: if priorityList or locales is null
        """
        from LocaleMatcher import LocaleMatcher
        return LocaleMatcher.filter(priorityList, locales, Locale.FilteringMode.AUTOSELECT_FILTERING)

    @filter.adddef('list', 'set', 'FilteringMode')
    @classmethod
    def filter(cls, priorityList, locales, mode):
        """
        Returns a list of matching Locale instances using the filtering
        mechanism defined in RFC 4647.
        :param priorityList: List: user's Language Priority List in which each
        language tag is sorted in descending order based on priority or weight
        :param locales: Collection: Locale instances used for matching
        :param mode: Locale.FilteringMode: filtering mode
        :return: List<Locale>. a list of Locale instances for matching
        language tags sorted in descending order based on priority or weight,
        or an empty list if nothing matches. The list is modifiable.
        :raises: NullPointerExceptionif priorityList or locales is
        nullIllegalArgumentExceptionif one or more extended language ranges
        are included in the given list when
        Locale.FilteringMode.REJECT_EXTENDED_RANGES is specified
        """
        from LocaleMatcher import LocaleMatcher
        return LocaleMatcher.filter(priorityList, locales, mode)

    @overload('list', 'set', 'FilteringMode')
    @classmethod
    def filterTags(cls, priorityList, tags, mode):
        """
        Returns a list of matching languages tags using the basic filtering
        mechanism defined in RFC 4647.
        :param priorityList: List: user's Language Priority List in which each
        language tag is sorted in descending order based on priority or weight
        :param tags: Collection: language tags
        :param mode: Locale.FilteringMode: filtering mode
        :return: List<String>. a list of matching language tags sorted in
        descending order based on priority or weight, or an empty list if
        nothing matches. The list is modifiable.
        :raises: NullPointerExceptionif priorityList or tags is
        nullIllegalArgumentExceptionif one or more extended language ranges
        are included in the given list when
        Locale.FilteringMode.REJECT_EXTENDED_RANGES is specified
        """
        from LocaleMatcher import LocaleMatcher
        return LocaleMatcher.filterTags(priorityList, tags, mode)

    @filterTags.adddef('List', 'set')
    @classmethod
    def filterTags(cls, priorityList, tags):
        """
        Returns a list of matching languages tags using the basic filtering
        mechanism defined in RFC 4647. This is equivalent to filterTags(List,
        Collection, FilteringMode) when mode is
        Locale.FilteringMode.AUTOSELECT_FILTERING.
        :param priorityList: List: user's Language Priority List in which each
        language tag is sorted in descending order based on priority or weight
        :param tags: Collection: language tags
        :return: List<String>. a list of matching language tags sorted in
        descending order based on priority or weight, or an empty list if
        nothing matches. The list is modifiable.
        :raises: NullPointerExceptionif priorityList or tags is null
        """
        from LocaleMatcher import LocaleMatcher
        return LocaleMatcher.filterTags(priorityList, tags, Locale.FilteringMode.AUTOSELECT_FILTERING)

    @classmethod
    def forLanguageTag(cls, languageTag):
        """
        Returns a locale for the specified IETF BCP 47 language tag string.
        If the specified language tag contains any ill-formed subtags, the
        first such subtag and all following subtags are ignored.  Compare to
        Locale.Builder.setLanguageTag(String) which throws an exception in
        this case.  The following conversions are performed:The language code
        "und" is mapped to language "".  The language codes "he", "yi", and
        "id" are mapped to "iw", "ji", and "in" respectively. (This is the
        same canonicalization that's done in Locale's constructors.)  The
        portion of a private use subtag prefixed by "lvariant", if any, is
        removed and appended to the variant field in the result locale
        (without case normalization).  If it is then empty, the private use
        subtag is discarded:   Locale loc; loc =
        Locale.forLanguageTag("en-US-x-lvariant-POSIX"); loc.getVariant(); //
        returns "POSIX" loc.getExtension('x'); // returns null  loc =
        Locale.forLanguageTag("de-POSIX-x-URP-lvariant-Abc-Def");
        loc.getVariant(); // returns "POSIX_Abc_Def" loc.getExtension('x'); //
        returns "urp" When the languageTag argument contains an extlang
        subtag, the first such subtag is used as the language, and the primary
        language subtag and other extlang subtags are ignored:
        Locale.forLanguageTag("ar-aao").getLanguage(); // returns "aao"
        Locale.forLanguageTag("en-abc-def-us").toString(); // returns "abc_US"
        Case is normalized except for variant tags, which are left unchanged.
        Language is normalized to lower case, script to title case, country to
        upper case, and extensions to lower case.  If, after processing, the
        locale would exactly match either ja_JP_JP or th_TH_TH with no
        extensions, the appropriate extensions are added as though the
        constructor had been called:
        Locale.forLanguageTag("ja-JP-x-lvariant-JP").toLanguageTag(); //
        returns "ja-JP-u-ca-japanese-x-lvariant-JP"
        Locale.forLanguageTag("th-TH-x-lvariant-TH").toLanguageTag(); //
        returns "th-TH-u-nu-thai-x-lvariant-TH" This implements the
        'Language-Tag' production of BCP47, and so supports grandfathered
        (regular and irregular) as well as private use language tags.  Stand
        alone private use tags are represented as empty language and extension
        'x-whatever', and grandfathered tags are converted to their canonical
        replacements where they exist.  Grandfathered tags with canonical
        replacements are as follows:  grandfathered tag&nbsp;modern

        replacementart-lojban&nbsp;jboi-ami&nbsp;amii-bnn&nbsp;bnni-hak&nbsp;haki-klingon&nbsp;tlhi-lux&nbsp;lbi-navajo&nbsp;nvi-pwn&nbsp;pwni-tao&nbsp;taoi-tay&nbsp;tayi-tsu&nbsp;tsuno-bok&nbsp;nbno-nyn&nbsp;nnsgn-BE-FR&nbsp;sfbsgn-BE-NL&nbsp;vgtsgn-CH-DE&nbsp;sggzh-guoyu&nbsp;cmnzh-hakka&nbsp;hakzh-min-nan&nbsp;nanzh-xiang&nbsp;hsnGrandfathered tags with no modern replacement will be converted as follows:  grandfathered tag&nbsp;converts tocel-gaulish&nbsp;xtg-x-cel-gaulishen-GB-oed&nbsp;en-GB-x-oedi-default&nbsp;en-x-i-defaulti-enochian&nbsp;und-x-i-enochiani-mingo&nbsp;see-x-i-mingozh-min&nbsp;nan-x-zh-minFor a list of all grandfathered tags, see the IANA Language Subtag Registry (search for "Type: grandfathered").  Note: there is no guarantee that toLanguageTag and forLanguageTag will round-trip.
        :param languageTag: String: the language tag
        :return: Locale. The locale that best represents the language tag.
        :raises NullPointerException: if languageTag is null
        See also: toLanguageTag()Locale.Builder.setLanguageTag(String)
        """
        builder = Locale.Builder()
        builder.setLanguageTag(languageTag)
        return builder.build()

    @classmethod
    def getAvailableLocales(cls):
        """
        Returns an array of all installed locales.
        :return: Locale[]. An array of installed locales.
        """
        return cls._instances.values()

    def getCountry(self):
        """
        Returns the country/region code for this locale, which should either
        be the empty string, an uppercase ISO 3166 2-letter code, or a UN M.49
        3-digit code.
        :return: String. The country/region code, or the empty string if none
        is defined.
        See also:
        getDisplayCountry()
        """
        return self._regn

    @overload('Category')
    @classmethod
    def getDefault(cls, category):
        """
        Gets the current value of the default locale for the specified
        Category for this instance of the Java Virtual Machine.  The Java
        Virtual Machine sets the default locale during startup based on the
        host environment. It is used by many locale-sensitive methods if no
        locale is explicitly specified. It can be changed using the
        setDefault(Locale.Category, Locale) method.
        :param category: Locale.Category: - the specified category to get the
        default locale
        :return: Locale. the default locale for the specified Category for
        this instance of the Java Virtual Machine
        :raises: NullPointerException- if category is null
        See also: setDefault(Locale.Category, Locale)
        """
        if category == Locale.Category.DISPLAY:
            if cls._defaultDisplayLocale is None:
                with cls.sLock:
                    if cls._defaultDisplayLocale is None:
                        cls.defaultDisplayLocale = cls._initDefault(category)
            return cls.defaultDisplayLocale
        elif category == Locale.Category.FORMAT:
            if cls.defaultFormatLocale is None:
                with cls.sLock:
                    if cls.defaultFormatLocale is None:
                        cls.defaultFormatLocale = cls._initDefault(category)
            return cls.defaultFormatLocale
        else:
            # assert False, "Unknown Category"
            return cls.getDefault()

    @getDefault.adddef()
    @classmethod
    def getDefault(cls):
        """
        Gets the current value of the default locale for this instance of the
        Java Virtual Machine.  The Java Virtual Machine sets the default
        locale during startup based on the host environment. It is used by
        many locale-sensitive methods if no locale is explicitly specified. It
        can be changed using the setDefault method.
        :return: Locale. the default locale for this instance of the Java
        Virtual Machine
        """
        if not cls._defaultLocale:
            with cls.sLock:
                if not cls._defaultLocale:
                    cls._defaultLocale = cls._initDefault()
        return cls._defaultLocale

    @overload('Locale')
    def getDisplayCountry(self, locale):
        """
        Returns the name of this locale's country, localized to locale.
        Returns the empty string if this locale does not correspond to a
        specific country.
        :param locale: Locale
        :return: String.
        """
        return locale.getCountry()

    @getDisplayCountry.adddef()
    def getDisplayCountry(self):
        """
        Returns a name for the locale's country that is appropriate for
        display to the user. If possible, the name returned will be localized
        for the default DISPLAY locale. For example, if the locale is fr_FR
        and the default DISPLAY locale is en_US, getDisplayCountry() will
        return "France"; if the locale is en_US and the default DISPLAY locale
        is fr_FR, getDisplayCountry() will return "Etats-Unis". If the name
        returned cannot be localized for the default DISPLAY locale, (say, we
        don't have a Japanese name for Croatia), this function falls back on
        the English name, and uses the ISO code as a last-resort value.  If
        the locale doesn't specify a country, this function returns the empty
        string.
        :return: String. The name of the country appropriate to the locale.
        """
        return self.getDisplayCountry(self.getDefault(Locale.Category.DISPLAY))

    @overload('Locale')
    def getDisplayLanguage(self, locale):
        """
        Returns the name of this locale's language, localized to locale. If
        the language name is unknown, the language code is returned.
        :param locale: Locale
        :return: String.
        """
        pass

    @getDisplayLanguage.adddef()
    def getDisplayLanguage(self):
        """
        Returns a name for the locale's language that is appropriate for
        display to the user. If possible, the name returned will be localized
        for the default DISPLAY locale. For example, if the locale is fr_FR
        and the default DISPLAY locale is en_US, getDisplayLanguage() will
        return "French"; if the locale is en_US and the default DISPLAY locale
        is fr_FR, getDisplayLanguage() will return "anglais". If the name
        returned cannot be localized for the default DISPLAY locale, (say, we
        don't have a Japanese name for Croatian), this function falls back on
        the English name, and uses the ISO code as a last-resort value.  If
        the locale doesn't specify a language, this function returns the empty
        string.
        :return: String. The name of the display language.
        """
        self.getDisplayLanguage(self.getDefault(Locale.Category.DISPLAY))

    @overload
    def getDisplayName(self):
        """
        Returns a name for the locale that is appropriate for display to the
        user. This will be the values returned by getDisplayLanguage(),
        getDisplayScript(), getDisplayCountry(), and getDisplayVariant()
        assembled into a single string. The the non-empty values are used in
        order, with the second and subsequent names in parentheses.  For
        example:  language (script, country, variant) language (country)
        language (variant) script (country) country depending on which fields
        are specified in the locale.  If the language, script, country, and
        variant fields are all empty, this function returns the empty string.
        :return: String. The name of the locale appropriate to display.
        """
        return self.getDisplayName(self.getDefault(Locale.Category.DISPLAY))

    @getDisplayName.adddef('Locale')
    def getDisplayName(self, inLocale):
        """
        Returns this locale's language name, country name, and variant,
        localized to locale. The exact output form depends on whether this
        locale corresponds to a specific language, script, country and
        variant.  For example:
        new Locale("en").getDisplayName(Locale.US) -> English
        new Locale("en", "US").getDisplayName(Locale.US) -> English (United States)
        new Locale("en", "US", "POSIX").getDisplayName(Locale.US) -> English (United States,Computer)
        Locale.fromLanguageTag("zh-Hant-CN").getDisplayName(Locale.US) -> Chinese (Traditional Han,China)
        new Locale("en").getDisplayName(Locale.FRANCE) -> anglais
        new Locale("en", "US").getDisplayName(Locale.FRANCE) -> anglais (États-Unis)
        new Locale("en", "US", "POSIX").getDisplayName(Locale.FRANCE) -> anglais (États-Unis,informatique).
        :param locale: Locale
        :return: String.
        """
        languageName = self.getDisplayLanguage(inLocale)
        scriptName = self.getDisplayScript(inLocale)
        countryName = self.getDisplayCountry(inLocale)
        variantName = self.getDisplayVariant(inLocale)
        if all((languageName, scriptName, countryName, variantName)):
            return ''
        if languageName:
            return '%s (%s)' % (languageName, ','.join(map(str, (scriptName, countryName, variantName))))
        if scriptName:
            return '%s (%s)' % (scriptName, str(countryName))
        return countryName

    @overload
    def getDisplayScript(self):
        """
        Returns a name for the the locale's script that is appropriate for
        display to the user. If possible, the name will be localized for the
        default DISPLAY locale.  Returns the empty string if this locale
        doesn't specify a script code.
        :return: String. the display name of the script code for the current
        default DISPLAY locale
        """
        return self.getDisplayScript(self.getDefault(Locale.Category.DISPLAY))

    @getDisplayScript.adddef('Locale')
    def getDisplayScript(self, inLocale):
        """
        Returns a name for the locale's script that is appropriate for display
        to the user. If possible, the name will be localized for the given
        locale. Returns the empty string if this locale doesn't specify a
        script code.
        :param inLocale: Locale: The locale for which to retrieve the display
        script.
        :return: String. the display name of the script code for the current
        default DISPLAY locale
        :raises: NullPointerExceptionif inLocale is null
        """
        return inLocale.getScript()

    @overload('Locale')
    def getDisplayVariant(self, inLocale):
        """
        Returns a name for the locale's variant code that is appropriate for
        display to the user.  If possible, the name will be localized for
        inLocale.  If the locale doesn't specify a variant code, this function
        returns the empty string.
        :param inLocale: Locale: The locale for which to retrieve the display
        variant code.
        :return: String. The name of the display variant code appropriate to
        the given locale.
        :raises: NullPointerExceptionif inLocale is null
        """
        return inLocale.getVariant()

    @getDisplayVariant.adddef()
    def getDisplayVariant(self):
        """
        Returns a name for the locale's variant code that is appropriate for
        display to the user.  If possible, the name will be localized for the
        default DISPLAY locale.  If the locale doesn't specify a variant code,
        this function returns the empty string.
        :return: String. The name of the display variant code appropriate to
        the locale.
        """
        return self.getDisplayVariant(self.getDefault(Locale.Category.DISPLAY))

    def getExtension(self, key):
        """
        Returns the extension (or private use) value associated with the
        specified key, or null if there is no extension associated with the
        key. To be well-formed, the key must be one of [0-9A-Za-z]. Keys are
        case-insensitive, so for example 'z' and 'Z' represent the same
        extension.
        :param key: char: the extension key
        :return: String. The extension, or null if this locale defines no
        extension for the specified key.
        :raises: IllegalArgumentExceptionif key is not well-formed
        See also: PRIVATE_USE_EXTENSIONUNICODE_LOCALE_EXTENSION
        """
        if not LanguageTag.isExtension(key) and key != LanguageTag.PRIVATEUSE:
            raise Exception('IllegalArgumentException: "Ill-formed extension key: %s"' % key)
        if self.hasExtensions():
            return self._extensions.get(key, '')

    def getExtensionKeys(self):
        """
        Returns the set of extension keys associated with this locale, or the
        empty set if it has no extensions. The returned set is unmodifiable.
        The keys will all be lower-case.
        :return: Set<Character>. The set of extension keys, or the empty set
        if this locale has no extensions.
        """
        keys = self._extensions.keys() if self.hasExtensions() else []
        return set(keys)

    def getISO3Country(self):
        """
        Returns a three-letter abbreviation for this locale's country. If the
        country matches an ISO 3166-1 alpha-2 code, the corresponding ISO
        3166-1 alpha-3 uppercase code is returned. If the locale doesn't
        specify a country, this will be the empty string.  The ISO 3166-1
        codes can be found on-line.
        :return: String. A three-letter abbreviation of this locale's country.
        :raises: MissingResourceExceptionThrows MissingResourceException if
        the three-letter country abbreviation is not available for this locale.
        """
        pass

    def getISO3Language(self):
        """
        Returns a three-letter abbreviation of this locale's language. If the
        language matches an ISO 639-1 two-letter code, the corresponding ISO
        639-2/T three-letter lowercase code is returned.  The ISO 639-2
        language codes can be found on-line, see "Codes for the Representation
        of Names of Languages Part 2: Alpha-3 Code".  If the locale specifies
        a three-letter language, the language is returned as is.  If the
        locale does not specify a language the empty string is returned.
        :return: String. A three-letter abbreviation of this locale's language.
        :raises: MissingResourceExceptionThrows MissingResourceException if
        three-letter language abbreviation is not available for this locale.
        """
        pass

    @classmethod
    def getISOCountries(cls):
        """
        Returns a list of all 2-letter country codes defined in ISO 3166. Can
        be used to create Locales. Note: The Locale class also supports other
        codes for country (region), such as 3-letter numeric UN M.49 area
        codes. Therefore, the list returned by this method does not contain
        ALL valid codes that can be used to create Locales.
        :return: String[]. An array of ISO 3166 two-letter country codes.
        """
        pass

    @classmethod
    def getISOLanguages(cls):
        """
        Returns a list of all 2-letter language codes defined in ISO 639. Can
        be used to create Locales. Note:ISO 639 is not a stable
        standard&mdash; some languages' codes have changed. The list this
        function returns includes both the new and the old codes for the
        languages whose codes have changed. The Locale class also supports
        language codes up to 8 characters in length.  Therefore, the list
        returned by this method does not contain ALL valid codes that can be
        used to create Locales.
        :return: String[]. Am array of ISO 639 two-letter language codes.
        """
        pass

    def getLanguage(self):
        """
        Returns the language code of this Locale.  Note: ISO 639 is not a
        stable standard&mdash; some languages' codes have changed. Locale's
        constructor recognizes both the new and the old codes for the
        languages whose codes have changed, but this function always returns
        the old code.  If you want to check for a specific language whose code
        has changed, don't do  if (locale.getLanguage().equals("he")) // BAD!
        ...  Instead, do  if (locale.getLanguage().equals(new
        Locale("he").getLanguage())) ...
        :return: String. The language code, or the empty string if none is
        defined.
        See also: getDisplayLanguage()
        """
        return self._lang

    def getScript(self):
        """
        Returns the script for this locale, which should either be the empty
        string or an ISO 15924 4-letter script code. The first letter is
        uppercase and the rest are lowercase, for example, 'Latn', 'Cyrl'.
        :return: String. The script code, or the empty string if none is
        defined.
        See also: getDisplayScript()
        """
        return self._scrt

    def getUnicodeLocaleAttributes(self):
        """
        Returns the set of unicode locale attributes associated with this
        locale, or the empty set if it has no attributes. The returned set is
        unmodifiable.
        :return: Set<String>. The set of attributes.
        """
        if not self.hasExtensions(): return set()
        ule = self.getExtension('u')
        builder = Locale.Builder()
        builder.setExtension('u', ule)
        return builder.uattributes

    def getUnicodeLocaleKeys(self):
        """
        Returns the set of Unicode locale keys defined by this locale, or the
        empty set if this locale has none.  The returned set is immutable.
        Keys are all lower case.
        :return: Set<String>. The set of Unicode locale keys, or the empty set
        if this locale has no Unicode locale keywords.
        """
        if not self.hasExtensions(): return set()
        ule = self.getExtension('u')
        builder = Locale.Builder()
        builder.setExtension('u', ule)
        return set(builder.ukeywords.keys())

    def getUnicodeLocaleType(self, key):
        """
        Returns the Unicode locale type associated with the specified Unicode
        locale key for this locale. Returns the empty string for keys that are
        defined with no type. Returns null if the key is not defined. Keys are
        case-insensitive. The key must be two alphanumeric characters
        ([0-9a-zA-Z]), or an IllegalArgumentException is thrown.
        :param key: String: the Unicode locale key
        :return: String. The Unicode locale type associated with the key, or
        null if the locale does not define the key.
        :raises: IllegalArgumentExceptionif the key is not
        well-formedNullPointerExceptionif key is null
        """
        if not key:
            raise Exception('NullPointerException')
        if not LanguageTag.isExtension(key):
            raise Exception('IllegalArgumentException: "key is not well-formed"')
        if not self.hasExtensions(): return set()
        ule = self.getExtension('u')
        builder = Locale.Builder()
        builder.setExtension('u', ule)
        return builder.ukeywords.get(key, None)

    def getVariant(self):
        """
        Returns the variant code for this locale.
        :return: String. The variant code, or the empty string if none is
        defined.
        See also: getDisplayVariant()
        """
        return self._vart

    def hasExtensions(self):
        """
        Returns true if this Locale has any extensions.
        :return: boolean. true if this Locale has any extensions
        """
        return bool(self._extensions)

    def hashCode(self):
        """
        Override hashCode. Since Locales are often used in hashtables, caches
        the value for speed.
        :return: int. a hash code value for this object.
        """
        language, script, region, variant = self._lang, self._scrt, self._regn, self._vart
        hash = reduce(
            lambda t, x: t + (x.__hash__() if x is not None else 0),
            (language, script, region, variant),
            0
        )
        if self.hasExtensions():
            hash ^= reduce(
                lambda t, x: t + (x.__hash__() if x is not None else 0),
                itertools.chain.from_iterable(self._extensions.items()),
                0
            )
        return hash

    @classmethod
    def lookup(self, priorityList, locales):
        """
        Returns a Locale instance for the best-matching language tag using the
        lookup mechanism defined in RFC 4647.
        :param priorityList: List: user's Language Priority List in which each
        language tag is sorted in descending order based on priority or weight
        :param locales: Collection: Locale instances used for matching
        :return: Locale. the best matching Locale instance chosen based on
        priority or weight, or null if nothing matches.
        :raises: NullPointerExceptionif priorityList or tags is null
        """
        from LocaleMatcher import LocaleMatcher
        return LocaleMatcher.lookup(priorityList, locales)

    @classmethod
    def lookupTag(self, priorityList, tags):
        """
        Returns the best-matching language tag using the lookup mechanism
        defined in RFC 4647.
        :param priorityList: List: user's Language Priority List in which each
        language tag is sorted in descending order based on priority or weight
        :param tags: Collection: language tangs used for matching
        :return: String. the best matching language tag chosen based on
        priority or weight, or null if nothing matches.
        :raises: NullPointerExceptionif priorityList or tags is null
        """
        from LocaleMatcher import LocaleMatcher
        return LocaleMatcher.lookupTag(priorityList, tags)

    @overload('Locale')
    @classmethod
    def setDefault(cls, newLocale):
        """
        Sets the default locale for this instance of the Java Virtual Machine.
        This does not affect the host locale.  If there is a security manager,
        its checkPermission method is called with a
        PropertyPermission("user.language", "write") permission before the
        default locale is changed.  The Java Virtual Machine sets the default
        locale during startup based on the host environment. It is used by
        many locale-sensitive methods if no locale is explicitly specified.
        Since changing the default locale may affect many different areas of
        functionality, this method should only be used if the caller is
        prepared to reinitialize locale-sensitive code running within the same
        Java Virtual Machine.  By setting the default locale with this method,
        all of the default locales for each Category are also set to the
        specified default locale.
        :param newLocale: Locale: the new default locale
        :raises: SecurityExceptionif a security manager exists and its
        checkPermission method doesn't allow the
        operation.NullPointerExceptionif newLocale is null
        See also: SecurityManager.checkPermission(Permission)PropertyPermission
        """
        cls.setDefault(Locale.Category.DISPLAY, newLocale)
        cls.setDefault(Locale.Category.FORMAT, newLocale)
        cls.defaultLocale = newLocale
        pass

    @setDefault.adddef('Category', 'Locale')
    @classmethod
    def setDefault(cls, category, newLocale):
        """
        Sets the default locale for the specified Category for this instance
        of the Java Virtual Machine. This does not affect the host locale.  If
        there is a security manager, its checkPermission method is called with
        a PropertyPermission("user.language", "write") permission before the
        default locale is changed.  The Java Virtual Machine sets the default
        locale during startup based on the host environment. It is used by
        many locale-sensitive methods if no locale is explicitly specified.
        Since changing the default locale may affect many different areas of
        functionality, this method should only be used if the caller is
        prepared to reinitialize locale-sensitive code running within the same
        Java Virtual Machine.
        :param category: Locale.Category: - the specified category to set the
        default locale
        :param newLocale: Locale: - the new default locale
        :raises: SecurityException- if a security manager exists and its
        checkPermission method doesn't allow the
        operation.NullPointerException- if category and/or newLocale is null
        See also:
        SecurityManager.checkPermission(java.security.Permission)
        PropertyPermissiongetDefault(Locale.Category)
        """
        if category is None:
            raise Exception('NullPointerException:"Category cannot be NULL"')
        if newLocale is None:
            raise Exception('NullPointerException:"Can\'t set default locale to NONE"')
        with cls.sLock:
            if category == Locale.Category.DISPLAY:
                cls._defaultDisplayLocale = newLocale
            elif category == Locale.Category.FORMAT:
                cls._defaultFormatLocale = newLocale
            else:
                assert False, 'Unknown format'
        pass

    def stripExtensions(self):
        """
        Returns a copy of this Locale with no extensions. If this Locale has
        no extensions, this Locale is returned.
        :return: Locale. a copy of this Locale with no extensions, or this if
        this has no extensions
        """
        if not self.hasExtensions():
            return self
        other = self.clone()
        other._extensions = {}
        return other

    def toLanguageTag(self):
        """
        Returns a well-formed IETF BCP 47 language tag representing this
        locale.  If this Locale has a language, country, or variant that does
        not satisfy the IETF BCP 47 language tag syntax requirements, this
        method handles these fields as described below:
        Language: If language is empty, or not well-formed (for example "a" or
        "e2"), it will be emitted as "und" (Undetermined).
        Country: If country is not well-formed (for example "12" or "USA"),
        it will be omitted.
        Variant: If variant iswell-formed, each sub-segment (delimited by '-'
        or '_') is emitted as a subtag.
        Otherwise: if all sub-segments match [0-9a-zA-Z]{1,8} (for example "WIN"
        or "Oracle_JDK_Standard_Edition"), the first ill-formed sub-segment and
        all following will be appended to the private use subtag.
        The first appended subtag will be "lvariant", followed by the sub-segments
        in order, separated by hyphen.
        For example, "x-lvariant-WIN", "Oracle-x-lvariant-JDK-Standard-Edition".
        if any sub-segment does not match [0-9a-zA-Z]{1,8}, the variant will
        be truncated and the problematic sub-segment and all following
        sub-segments will be omitted.  If the remainder is non-empty, it will
        be emitted as a private use subtag as above (even if the remainder
        turns out to be well-formed).  For example,
        "Solaris_isjustthecoolestthing" is emitted as "x-lvariant-Solaris",
        not as "solaris".
        Special Conversions: Java supports some old locale representations,
        including deprecated ISO language codes, for compatibility. This method
        performs the following conversions:
        Deprecated ISO language codes "iw", "ji", and "in" are converted to
        "he", "yi", and "id", respectively.
        A locale with language "no", country "NO", and variant "NY", representing
        Norwegian Nynorsk (Norway), is converted to a language tag "nn-NO".
        Note: Although the language tag created by this method is well-formed
        (satisfies the syntax requirements defined by the IETF BCP 47 specification),
        it is not necessarily a valid BCP 47 language tag.  For example,  new
        Locale("xx", "YY").toLanguageTag();  will return "xx-YY", but the
        language subtag "xx" and the region subtag "YY" are invalid because
        they are not registered in the IANA Language Subtag Registry.
        :return: String. a BCP47 language tag representing the locale
        See also: forLanguageTag(String)
        """
        if self._languageTag:
            return self._languageTag
        tag = LanguageTag.parseLocale(self)
        buf = [tag.canonicalizeLanguage(tag.getLanguage())]
        if tag.getScript():
            buf.append(tag.canonicalizeScript(tag.getScript()))
        if tag.getRegion():
            buf.append(tag.canonicalizeRegion(tag.getRegion()))
        if tag.getVariants():
            buf.extend(map(LanguageTag.canonicalizeVariant, tag.getVariants()))
        extensions = tag.getExtensions()
        if extensions:
            buf.extend(map(tag.canonicalizeExtension, extensions))
        privuse = tag.getPrivateuse()
        if privuse:
            buf.extend((LanguageTag.PRIVATEUSE, privuse))
        return LanguageTag.SEP.join(filter(lambda x: bool(x), buf))

    def toString(self):
        """
        Returns a string representation of this Locale object, consisting of
        language, country, variant, script, and extensions as below:  language
        + "_" + country + "_" + (variant + "_#" | "#") + script + "-" +
        extensions
        Language is always lower case, country is always upper
        case, script is always title case, and extensions are always lower
        case.  Extensions and private use subtags will be in canonical order
        as explained in toLanguageTag().
        When the locale has neither script nor extensions, the result is the
        same as in Java 6 and prior.  If both the language and country fields
        are missing, this function will return the empty string, even if the
        variant, script, or extensions field is present (you can't have a locale
        with just a variant, the variant must accompany a well-formed language
        or country code).
        If script or extensions are present and variant is missing, no underscore
        is added before the "#".  This behavior is designed to support
        debugging and to be compatible with previous uses of toString that
        expected language, country, and variant fields only.  To represent a
        Locale as a String for interchange purposes, use toLanguageTag().
        Examples:
        en, de_DE_GB, en_US_WIN, de__POSIX, zh_CN_#Hans, zh_TW_#Hant-x-java,
        th_TH_TH_#u-nu-thai
        :return: String. A string representation of the Locale, for debugging.
        See also:
        getDisplayName()
        toLanguageTag()
        """
        l = bool(self.getLanguage())
        s = bool(self.getScript())
        r = bool(self.getCountry())
        v = bool(self.getVariant())
        e = self.hasExtensions()

        result = self.getLanguage()
        if (r or (l and (v or s or e))):
            result += Locale.SEP + self.getCountry()
        if (v and (l or r)):
            result += Locale.SEP + self.getVariant()
        if (s and (l or r)):
            result += Locale.SEP + '#' + self.getScript()
        if (e and (l or r)):
            result += Locale.SEP
            if not s:
                result += '#'
            result += Locale.SEP.join(itertools.chain.from_iterable(self._extensions.items()))
        return result

    @classmethod
    def _initDefault(cls, localeCategory=None):
        pylocale.setlocale(pylocale.LC_ALL, '')
        if localeCategory == Locale.Category.DISPLAY:
            envvars = ('LC_MESSAGES', 'LC_COLLATE', 'LC_TYPE', 'LC_LANGUAGE')
        elif localeCategory == Locale.Category.FORMAT:
            envvars = ('LC_TIME', 'LC_NUMERIC', 'LC_MONETARY', 'LC_LANGUAGE')
        else:
            envvars = ('LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE')
        localeTag, encoding = pylocale.getdefaultlocale(envvars=envvars)
        localeTag = localeTag.replace(Locale.SEP, LanguageTag.SEP)
        return cls.forLanguageTag(localeTag)



