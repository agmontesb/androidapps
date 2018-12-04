# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/os/PatternMatcher"""
import re

from Android import overload, Object
from Android.interface.IParcelable import IParcelable, ICreator

"""
public static final int PATTERN_ADVANCED_GLOB:
Pattern type: the given pattern is interpreted with a regular
expression-like syntax for matching against the string it is tested
against. Supported tokens include dot (.) and sets ([...])
with full support for character ranges and the not (^) modifier.
Supported modifiers include star (*) for zero-or-more, plus (+)
for one-or-more and full range ({...}) support. This is a simple
evaluation implementation in which matching is done against the pattern in
real time with no backtracking support.
"""
PATTERN_ADVANCED_GLOB = 0x00000003

"""
public static final int PATTERN_LITERAL:
Pattern type: the given pattern must exactly match the string it is
tested against.
"""
PATTERN_LITERAL = 0x00000000

"""
public static final int PATTERN_PREFIX:
Pattern type: the given pattern must match the
beginning of the string it is tested against.
"""
PATTERN_PREFIX = 0x00000001

"""
public static final int PATTERN_SIMPLE_GLOB:
Pattern type: the given pattern is interpreted with a
simple glob syntax for matching against the string it is tested against.
In this syntax, you can use the '*' character to match against zero or
more occurrences of the character immediately before.  If the
character before it is '.' it will match any character.  The character
'\' can be used as an escape.  This essentially provides only the '*'
wildcard part of a normal regexp.
"""
PATTERN_SIMPLE_GLOB = 0x00000002

class PatternMatcher(Object, IParcelable):
    """
    A simple pattern matcher, which is safe to use on untrusted data: it does 
    not provide full reg-exp support, only simple globbing that can not be 
    used maliciously.
    """

    """
    public static final Creator<PatternMatcher> CREATOR:
    
    """
    CREATOR = type(
        'PatternMatcherCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: PatternMatcher._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * PatternMatcher)()
        })()

    @overload('str', 'int')
    def __init__(self, pattern, mtype):
        """
        :param pattern: String.
        :param type: int.
        """
        super(PatternMatcher, self).__init__(pattern, type)
        self._pattern = pattern
        self._type = mtype

    @__init__.adddef('Parcel')
    def PatternMatcher(self, src):
        """
        :param src: Parcel.
        """
        pattern = src.readString()
        mtype = src.readInt()
        self.__init__(pattern, mtype)

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

    def getPath(self):
        """
        :return: String.
        """
        return self._pattern

    def getType(self):
        """
        :return: int.
        """
        return self._type

    def match(self, astr):
        """
        :param astr: String
        :return: boolean.
        """
        mtype = self.getType()
        if mtype == PATTERN_ADVANCED_GLOB:
            path = self.getPath()
            pattern = re.sub(r'(?<=[^\\])[$?!()]', lambda x: '\\' + x.group(), path)
            return re.search(pattern, astr) is not None
        if mtype == PATTERN_LITERAL:
            return self.getPath() == astr
        if mtype == PATTERN_PREFIX:
            return astr.startswith(self.getPath())
        if mtype == PATTERN_SIMPLE_GLOB:
            path = self.getPath()
            pattern = re.sub(r'(?<=[^\\])[$?{}^\[\]!()+]', lambda x: '\\' + x.group(), path)
            return re.search(pattern, astr) is not None

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
        return self.__str__()

    def writeToParcel(self, dest, flags):
        """
        Flatten this object in to a Parcel.
        :param dest: Parcel: The Parcel in which the object should be written.
        :param flags: int: Additional flags about how the object should be 
        written. May be 0 or Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        dest.writeString(self.getPath())
        dest.writeInt(self.getType())

