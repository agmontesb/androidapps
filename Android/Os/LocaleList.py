# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/os/LocaleList"""
import threading

from Android import overload
from Android.interface.IParcelable import IParcelable
from Android.java.Locale import Locale


class LocaleList(IParcelable):

    """
    public static final Creator<LocaleList> CREATOR:
    
    """
    CREATOR = type(
        'LocaleListCreator',
        (IParcelable.ICreator,),
        {
            'createFromParcel':
                lambda self, inparcel: LocaleList.forLanguageTags(inparcel.readString()),
            'newArray': lambda self, size: (size * LocaleList)()
        }
    )()
    sLock = threading.RLock()
    EN_LATN = Locale.forLanguageTag("en-Latn")

    def __init__(self, *args):
        """
        :param list: Locale....
        """
        super(LocaleList, self).__init__(*args)
        if not args:
            self.mList = self.sEmpyList
            self.mStringRepresentation = ''
        else:
            localelist = []
            seenlocales = set()
            sb = ''
            for k, l in enumerate(args):
                if l is None: raise Exception('NullPointerException: "list[%s] is None"' % k)
                if l in seenlocales: raise Exception('NullPointerException: "list[%s] is a repetition"' % k)
                localelist.append(l.clone())
                sb += localelist[-1].toLanguageTag() + ','
                seenlocales.add(localelist[-1])
            self.mList = localelist
            self.mStringRepresentation = sb.rstrip(',')

    def describeContents(self):
        """
        Describe the kinds of special objects contained in this Parcelable 
        instance's marshaled representation. For example, if the object will 
        include a file descriptor in the output of writeToParcel(Parcel, int), 
        the return value of this method must include the 
        CONTENTS_FILE_DESCRIPTOR bit.
        :return: int. a bitmask indicating the set of special object types 
        marshaled by this Parcelable object instance.
        """
        return 0

    def equals(this, other):
        """
        Indicates whether some other object is "equal to" this one.  The 
        equals method implements an equivalence relation on non-null object 
        references: It is reflexive: for any non-null reference value x, 
        x.equals(x) should return true. It is symmetric: for any non-null 
        reference values x and y, x.equals(y) should return true if and only 
        if y.equals(x) returns true. It is transitive: for any non-null 
        reference values x, y, and z, if x.equals(y) returns true and 
        y.equals(z) returns true, then x.equals(z) should return true. It is 
        consistent: for any non-null reference values x and y, multiple 
        invocations of x.equals(y) consistently return true or consistently 
        return false, provided no information used in equals comparisons on 
        the objects is modified. For any non-null reference value x, 
        x.equals(null) should return false.  The equals method for class 
        Object implements the most discriminating possible equivalence 
        relation on objects; that is, for any non-null reference values x and 
        y, this method returns true if and only if x and y refer to the same 
        object (x == y has the value true).  Note that it is generally 
        necessary to override the hashCode method whenever this method is 
        overridden, so as to maintain the general contract for the hashCode 
        method, which states that equal objects must have equal hash codes.
        :param other: Object: the reference object with which to compare.
        :return: boolean. true if this object is the same as the obj argument; 
        false otherwise.
        """
        if this == other: return True
        if not isinstance(other, LocaleList): return False
        otherList = other.mList
        if len(otherList) != len(this.mList): return False
        for i in range(this.size()):
            if not this.mList[i].equals(otherList[i]): return False
        return True

    @classmethod
    def forLanguageTags(cls, list):
        """
        Generates a new LocaleList with the given language tags.
        :param list: String: The language tags to be included as a single 
        String separated by commas.This value may be null.
        :return: LocaleList. A new instance with the Locale items identified 
        by the given tags. This value will never be null.
        """
        if not list:
            return cls.getEmptyLocaleList()
        localeArray = map(lambda x: Locale.forLanguageTag(x), list.split(','))
        return cls(*localeArray)

    def get(self, index):
        """
        Retrieves the Locale at the specified index.
        :param index: int: The position to retrieve.
        :return: Locale. The Locale in the given index.
        """
        bFlag = (0 <= index and index < len(self.mList))
        return  self.mList[index] if bFlag else None

    @classmethod
    def getAdjustedDefault(self):
        """
        Returns the default locale list, adjusted by moving the default locale 
        to its first position.
        :return: LocaleList. This value will never be null.
        """
        self.getDefault()
        with self.sLock:
            return self.sDefaultAdjustedLocaleList

    @classmethod
    def getDefault(cls):
        """
        The result is guaranteed to include the default Locale returned by 
        Locale.getDefault(), but not necessarily at the top of the list. The 
        default locale not being at the top of the list is an indication that 
        the system has set the default locale to one of the user's other 
        preferred locales, having concluded that the primary preference is not 
        supported but a secondary preference is.  Note that the default 
        LocaleList would change if Locale.setDefault() is called. This method 
        takes that into account by always checking the output of 
        Locale.getDefault() and recalculating the default LocaleList if needed.
        :return: LocaleList. This value will never be null.
        """
        defaultLocale = Locale.getDefault()
        with cls.sLock:
            if not defaultLocale.equals(cls.sLastDefaultLocale):
                cls.sLastDefaultLocale = defaultLocale
                if (cls.sDefaultLocaleList != None and \
                    defaultLocale.equals(cls.sDefaultLocaleList.get(0))):
                    return cls.sDefaultLocaleList
                cls.sDefaultLocaleList = LocaleList(defaultLocale, *cls.sLastExplicitlySetLocaleList)
                cls.sDefaultAdjustedLocaleList = cls.sDefaultLocaleList
            return cls.sDefaultLocaleList
        pass

    @classmethod
    def getEmptyLocaleList(cls):
        """
        Retrieve an empty instance of LocaleList.
        :return: LocaleList. This value will never be null.
        """
        return cls.sEmptyLocaleList

    def getFirstMatch(self, supportedLocales):
        """
        Returns the first match in the locale list given an unordered array of 
        supported locales in BCP 47 format.
        :param supportedLocales: String
        :return: Locale. The first Locale from this list that appears in the 
        given array, or null if the LocaleList is empty.
        """
        return self._computeFirstMatch(supportedLocales, False)

    def hashCode(self):
        """
        Returns a hash code value for the object. This method is supported for 
        the benefit of hash tables such as those provided by HashMap.  The 
        general contract of hashCode is: Whenever it is invoked on the same 
        object more than once during an execution of a Java application, the 
        hashCode method must consistently return the same integer, provided no 
        information used in equals comparisons on the object is modified. This 
        integer need not remain consistent from one execution of an 
        application to another execution of the same application. If two 
        objects are equal according to the equals(Object) method, then calling 
        the hashCode method on each of the two objects must produce the same 
        integer result. It is not required that if two objects are unequal 
        according to the equals(java.lang.Object) method, then calling the 
        hashCode method on each of the two objects must produce distinct 
        integer results.  However, the programmer should be aware that 
        producing distinct integer results for unequal objects may improve the 
        performance of hash tables.  As much as is reasonably practical, the 
        hashCode method defined by class Object does return distinct integers 
        for distinct objects. (This is typically implemented by converting the 
        internal address of the object into an integer, but this 
        implementation technique is not required by the Java&trade; 
        programming language.)
        :return: int. a hash code value for this object.
        """
        return reduce(lambda t, x: 31*t + x.hashCode(), self.mList, 1)

    def indexOf(self, locale):
        """
        Searches this LocaleList for the specified Locale and returns the 
        index of the first occurrence.
        :param locale: Locale: The Locale to search for.
        :return: int. The index of the first occurrence of the Locale or -1 if 
        the item wasn't found. Value is -1 or greater.
        """
        size = self.size()
        for i in range(size):
            if self.mList[i].equals(locale): return i
        return -1

    def isEmpty(self):
        """
        Returns whether the LocaleList contains no Locale items.
        :return: boolean. true if this LocaleList has no Locale items, false 
        otherwise.
        """
        return len(self.mList) == 0

    @classmethod
    def setDefault(cls, locales):
        """
        Also sets the default locale by calling Locale.setDefault() with the 
        first locale in the list.
        :param locales: LocaleListThis value must never be null.
        :raises: NullPointerExceptionif the input is 
        null.IllegalArgumentExceptionif the input is empty.
        """
        localeIndex = 0
        if locales is None: raise Exception('NullPointerException: "locales is None"')
        if locales.isEmpty(): raise Exception('IllegalArgumentException: "locales is empty"')
        with cls.sLock:
            cls.sLastDefaultLocale = locales.get(localeIndex)
            Locale.setDefault(cls.sLastDefaultLocale)
            cls.sLastExplicitlySetLocaleList = locales
            cls.sDefaultLocaleList = locales
            if localeIndex == 0:
                cls.sDefaultAdjustedLocaleList = cls.sDefaultLocaleList
            else:
                cls.sDefaultAdjustedLocaleList = cls(cls.sLastDefaultLocale, *cls.sDefaultLocaleList)
        pass

    def size(self):
        """
        Returns the number of Locale items in this LocaleList.
        :return: int.
        """
        return len(self.mList)

    def toLanguageTags(self):
        """
        Retrieves a String representation of the language tags in this list.
        :return: String. This value will never be null.
        """
        return self.mStringRepresentation

    def toString(self):
        """
        Returns a string representation of the object. In general, the 
        toString method returns a string that "textually represents" this 
        object. The result should be a concise but informative representation 
        that is easy for a person to read. It is recommended that all 
        subclasses override this method.  The toString method for class Object 
        returns a string consisting of the name of the class of which the 
        object is an instance, the at-sign character `@', and the unsigned 
        hexadecimal representation of the hash code of the object. In other 
        words, this method returns a string equal to the value of:  
        getClass().getName() + '@' + Integer.toHexString(hashCode())
        :return: String. a string representation of the object.
        """
        return '[' + ','.join(self.mList) + ']'

    def writeToParcel(self, dest, parcelableFlags):
        """
        Flatten this object in to a Parcel.
        :param dest: Parcel: The Parcel in which the object should be written.
        :param parcelableFlags: int: Additional flags about how the object 
        should be written. May be 0 or 
        Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        dest.writeString(self.mStringRepresentation)

    def _computeFirstMatch(self, supportedLocales, assumeEnglishIsSupported):
        bestIndex = self._computeFirstMatchIndex(supportedLocales, assumeEnglishIsSupported)
        return None if bestIndex == -1 else self.mList[bestIndex]

    def _computeFirstMatchIndex(self, supportedLocales, assumeEnglishIsSupported):
        if self.size() == 1: return 0
        if self.isEmpty(): return -1
        bestindex = 1000 * self.size()
        if assumeEnglishIsSupported:
            idx = self.findFirstMatchIndex(self.EN_LATN)
            if idx == 0: return 0
            elif idx < bestindex: bestindex = idx
        for languageTag in supportedLocales:
            supportedLocale = Locale.forLanguageTag(languageTag)
            idx = self.findFirstMatchIndex(supportedLocale)
            if idx == 0: return 0
            elif idx < bestindex: bestindex = idx
        if bestindex == 1000 * self.size(): return 0
        return bestindex


LocaleList.sEmptyLocaleList = LocaleList()