# -*- coding: utf-8 -*-
"""
https://developer.android.com/reference/android/util/TypedValue
ported from:
https://android.googlesource.com/platform/frameworks/base/+/master/core/java/android/util/TypedValue.java
"""
from Android import overload, Object

class TypedValue(Object):
    """
    Container for a dynamically typed data value. Primarily used with Resources
    for holding resource values.
    """

    """
    public static final int COMPLEX_MANTISSA_MASK:
    Complex data: mask to extract mantissa information (after shifting by
    COMPLEX_MANTISSA_SHIFT). This gives us 23 bits of precision;
    the top bit is the sign. 
    """
    COMPLEX_MANTISSA_MASK = 0x00ffffff

    """
    public static final int COMPLEX_MANTISSA_SHIFT:
    Complex data: bit location of mantissa information. 
    """
    COMPLEX_MANTISSA_SHIFT = 0x00000008

    """
    public static final int COMPLEX_RADIX_0p23:
    Complex data: the mantissa magnitude is 0 bits -- i.e, 0x0.nnnnnn 
    """
    COMPLEX_RADIX_0p23 = 0x00000003

    """
    public static final int COMPLEX_RADIX_16p7:
    Complex data: the mantissa magnitude is 16 bits -- i.e, 0xnnnn.nn 
    """
    COMPLEX_RADIX_16p7 = 0x00000001

    """
    public static final int COMPLEX_RADIX_23p0:
    Complex data: the mantissa is an integral number -- i.e., 0xnnnnnn.0 
    """
    COMPLEX_RADIX_23p0 = 0x00000000

    """
    public static final int COMPLEX_RADIX_8p15:
    Complex data: the mantissa magnitude is 8 bits -- i.e, 0xnn.nnnn 
    """
    COMPLEX_RADIX_8p15 = 0x00000002

    """
    public static final int COMPLEX_RADIX_MASK:
    Complex data: mask to extract radix information (after shifting by
    COMPLEX_RADIX_SHIFT). This give us 4 possible fixed point
    representations as defined below. 
    """
    COMPLEX_RADIX_MASK = 0x00000003

    """
    public static final int COMPLEX_RADIX_SHIFT:
    Complex data: where the radix information is, telling where the decimal
    place appears in the mantissa. 
    """
    COMPLEX_RADIX_SHIFT = 0x00000004

    """
    public static final int COMPLEX_UNIT_DIP:
    TYPE_DIMENSION complex unit: Value is Device Independent
    Pixels. 
    """
    COMPLEX_UNIT_DIP = 0x00000001

    """
    public static final int COMPLEX_UNIT_FRACTION:
    TYPE_FRACTION complex unit: A basic fraction of the overall
    size. 
    """
    COMPLEX_UNIT_FRACTION = 0x00000000

    """
    public static final int COMPLEX_UNIT_FRACTION_PARENT:
    TYPE_FRACTION complex unit: A fraction of the parent size. 
    """
    COMPLEX_UNIT_FRACTION_PARENT = 0x00000001

    """
    public static final int COMPLEX_UNIT_IN:
    TYPE_DIMENSION complex unit: Value is in inches. 
    """
    COMPLEX_UNIT_IN = 0x00000004

    """
    public static final int COMPLEX_UNIT_MASK:
    Complex data: mask to extract unit information (after shifting by
    COMPLEX_UNIT_SHIFT). This gives us 16 possible types, as
    defined below. 
    """
    COMPLEX_UNIT_MASK = 0x0000000f

    """
    public static final int COMPLEX_UNIT_MM:
    TYPE_DIMENSION complex unit: Value is in millimeters. 
    """
    COMPLEX_UNIT_MM = 0x00000005

    """
    public static final int COMPLEX_UNIT_PT:
    TYPE_DIMENSION complex unit: Value is in points. 
    """
    COMPLEX_UNIT_PT = 0x00000003

    """
    public static final int COMPLEX_UNIT_PX:
    TYPE_DIMENSION complex unit: Value is raw pixels. 
    """
    COMPLEX_UNIT_PX = 0x00000000

    """
    public static final int COMPLEX_UNIT_SHIFT:
    Complex data: bit location of unit information. 
    """
    COMPLEX_UNIT_SHIFT = 0x00000000

    """
    public static final int COMPLEX_UNIT_SP:
    TYPE_DIMENSION complex unit: Value is a scaled pixel. 
    """
    COMPLEX_UNIT_SP = 0x00000002

    """
    public static final int DATA_NULL_EMPTY:
    TYPE_NULL data indicating the value was explicitly set to null.
    """
    DATA_NULL_EMPTY = 0x00000001

    """
    public static final int DATA_NULL_UNDEFINED:
    TYPE_NULL data indicating the value was not specified.
    """
    DATA_NULL_UNDEFINED = 0x00000000

    """
    public static final int DENSITY_DEFAULT:
    If density is equal to this value, then the density should be
    treated as the system's default density value: 
    DisplayMetrics.DENSITY_DEFAULT:
    .
    """
    DENSITY_DEFAULT = 0x00000000

    """
    public static final int DENSITY_NONE:
    If density is equal to this value, then there is no density
    associated with the resource and it should not be scaled.
    """
    DENSITY_NONE = 0x0000ffff

    """
    public static final int TYPE_ATTRIBUTE:
    The data field holds an attribute resource
    identifier (referencing an attribute in the current theme
    style, not a resource entry). 
    """
    TYPE_ATTRIBUTE = 0x00000002

    """
    public static final int TYPE_DIMENSION:
    The data field holds a complex number encoding a
    dimension value. 
    """
    TYPE_DIMENSION = 0x00000005

    """
    public static final int TYPE_FIRST_COLOR_INT:
    Identifies the start of integer values that were specified as
    color constants (starting with '#'). 
    """
    TYPE_FIRST_COLOR_INT = 0x0000001c

    """
    public static final int TYPE_FIRST_INT:
    Identifies the start of plain integer values.  Any type value
    from this to TYPE_LAST_INT means the
    data field holds a generic integer value. 
    """
    TYPE_FIRST_INT = 0x00000010

    """
    public static final int TYPE_FLOAT:
    The data field holds an IEEE 754 floating point number. 
    """
    TYPE_FLOAT = 0x00000004

    """
    public static final int TYPE_FRACTION:
    The data field holds a complex number encoding a fraction
    of a container. 
    """
    TYPE_FRACTION = 0x00000006

    """
    public static final int TYPE_INT_BOOLEAN:
    The data field holds 0 or 1 that was originally
    specified as "false" or "true". 
    """
    TYPE_INT_BOOLEAN = 0x00000012

    """
    public static final int TYPE_INT_COLOR_ARGB4:
    The data field holds a color that was originally
    specified as #argb. 
    """
    TYPE_INT_COLOR_ARGB4 = 0x0000001e

    """
    public static final int TYPE_INT_COLOR_ARGB8:
    The data field holds a color that was originally
    specified as #aarrggbb. 
    """
    TYPE_INT_COLOR_ARGB8 = 0x0000001c

    """
    public static final int TYPE_INT_COLOR_RGB4:
    The data field holds a color that was originally
    specified as #rgb. 
    """
    TYPE_INT_COLOR_RGB4 = 0x0000001f

    """
    public static final int TYPE_INT_COLOR_RGB8:
    The data field holds a color that was originally
    specified as #rrggbb. 
    """
    TYPE_INT_COLOR_RGB8 = 0x0000001d

    """
    public static final int TYPE_INT_DEC:
    The data field holds a number that was
    originally specified in decimal. 
    """
    TYPE_INT_DEC = 0x00000010

    """
    public static final int TYPE_INT_HEX:
    The data field holds a number that was
    originally specified in hexadecimal (0xn). 
    """
    TYPE_INT_HEX = 0x00000011

    """
    public static final int TYPE_LAST_COLOR_INT:
    Identifies the end of integer values that were specified as color
    constants. 
    """
    TYPE_LAST_COLOR_INT = 0x0000001f

    """
    public static final int TYPE_LAST_INT:
    Identifies the end of plain integer values. 
    """
    TYPE_LAST_INT = 0x0000001f

    """
    public static final int TYPE_NULL:
    The value contains no data. 
    """
    TYPE_NULL = 0x00000000

    """
    public static final int TYPE_REFERENCE:
    The data field holds a resource identifier. 
    """
    TYPE_REFERENCE = 0x00000001

    """
    public static final int TYPE_STRING:
    The string field holds string data.  In addition, if
    data is non-zero then it is the string block
    index of the string and assetCookie is the set of
    assets the string came from. 
    """
    TYPE_STRING = 0x00000003


    def __init__(self):
        super(TypedValue, self).__init__()

        """
        public int assetCookie:
        Additional information about where the value came from; only
        set for strings.
        """
        self.assetCookie = None

        """
        public int changingConfigurations:
        If the value came from a resource, these are the configurations for
        which its contents can change.

        For example, if a resource has a value defined for the -land resource 
        qualifier,
        this field will have the ActivityInfo.CONFIG_ORIENTATION bit set.
        Value is either 0 or combination of CONFIG_MCC, CONFIG_MNC, CONFIG_LOCALE, 
        CONFIG_TOUCHSCREEN, CONFIG_KEYBOARD, CONFIG_KEYBOARD_HIDDEN, 
        CONFIG_NAVIGATION, CONFIG_ORIENTATION, CONFIG_SCREEN_LAYOUT, 
        CONFIG_UI_MODE, CONFIG_SCREEN_SIZE, CONFIG_SMALLEST_SCREEN_SIZE, 
        CONFIG_DENSITY, CONFIG_LAYOUT_DIRECTION, CONFIG_COLOR_MODE or 
        CONFIG_FONT_SCALE.
        See also:
        ActivityInfo.CONFIG_MCC
        ActivityInfo.CONFIG_MNC
        ActivityInfo.CONFIG_LOCALE
        ActivityInfo.CONFIG_TOUCHSCREEN
        ActivityInfo.CONFIG_KEYBOARD
        ActivityInfo.CONFIG_KEYBOARD_HIDDEN
        ActivityInfo.CONFIG_NAVIGATION
        ActivityInfo.CONFIG_ORIENTATION
        ActivityInfo.CONFIG_SCREEN_LAYOUT
        ActivityInfo.CONFIG_UI_MODE
        ActivityInfo.CONFIG_SCREEN_SIZE
        ActivityInfo.CONFIG_SMALLEST_SCREEN_SIZE
        ActivityInfo.CONFIG_DENSITY
        ActivityInfo.CONFIG_LAYOUT_DIRECTION
        ActivityInfo.CONFIG_COLOR_MODE
        """
        self.changingConfigurations = None

        """
        public int data:
        Basic data in the value, interpreted according to type
        """
        self.data = None

        """
        public int density:
        If the Value came from a resource, this holds the corresponding pixel 
        density.
        """
        self.density = None

        """
        public int resourceId:
        If Value came from a resource, this holds the corresponding resource id.
        """
        self.resourceId = None

        """
        public CharSequence string:
        If the value holds a string, this is it.
        """
        self.string = None

        """
        public int type:
        The type held by this value, as defined by the constants here.
        This tells you how to interpret the other fields in the object.
        """
        self.type = None
        pass

    @classmethod
    def applyDimension(cls, unit, value, metrics):
        """
        Converts an unpacked complex data value holding a dimension to its 
        final floating point value. The two parameters unit and value are as 
        in TYPE_DIMENSION.
        :param unit: int: The unit to convert from.
        :param value: float: The value to apply the unit to.
        :param metrics: DisplayMetrics: Current display metrics to use in the 
        conversion -- supplies display density and scaling information.
        :return: float. The complex floating point value multiplied by the 
        appropriate metrics depending on its unit.
        """
        if unit == cls.COMPLEX_UNIT_PX: return value
        elif unit == cls.COMPLEX_UNIT_DIP: return value * metrics.density
        elif unit == cls.COMPLEX_UNIT_SP: return value * metrics.scaledDensity
        elif unit == cls.COMPLEX_UNIT_PT: return value * metrics.xdpi * (1.0/72)
        elif unit == cls.COMPLEX_UNIT_IN: return value * metrics.xdpi
        elif unit == cls.COMPLEX_UNIT_MM: return value * metrics.xdpi * (1.0/25.4)
        return 0

    @overload
    def coerceToString(self):
        """
        Regardless of the actual type of the value, try to convert it to a
        string value.  For example, a color type will be converted to a string
        of the form #aarrggbb.
        :return: CharSequence. CharSequence The coerced string value.  If the
        value is null or the type is not known, null is returned.
        """
        t = self.type
        if t == self.TYPE_STRING:
            return self.string
        return self.coerceToString(t, self.data)

    @coerceToString.adddef('int', 'int')
    @classmethod
    def coerceToString(cls, atype, data):
        """
        Perform type conversion as per coerceToString() on an explicitly 
        supplied type and data.
        :param atype: int: The data type identifier.
        :param data: int: The data value.
        :return: String. String The coerced string value.  If the value is 
        null or the type is not known, null is returned.
        """
        if atype == cls.TYPE_NULL: return ''
        elif atype == cls.TYPE_REFERENCE: return '@' + data
        elif atype == cls.TYPE_ATTRIBUTE: return '?' + data
        elif atype == cls.TYPE_FLOAT: return str(data)
        elif atype == cls.TYPE_FLOAT:
            _DIMENSION_UNIT_STRS = ["px", "dip", "sp", "pt", "in", "mm"]
            units = (data >> cls.COMPLEX_UNIT_SHIFT) & cls.COMPLEX_UNIT_MASK
            return str(data) + _DIMENSION_UNIT_STRS[units]
        elif atype == cls.TYPE_FRACTION:
            _FRACTION_UNIT_STRS = ["%", "%p"]
            units = (data >> cls.COMPLEX_UNIT_SHIFT) & cls.COMPLEX_UNIT_MASK
            return str(data) + _FRACTION_UNIT_STRS[units]
        elif atype == cls.TYPE_INT_HEX: return hex(data)
        elif atype == cls.TYPE_INT_BOOLEAN: return 'True' if data else 'False'

        if cls.TYPE_FIRST_COLOR_INT <= atype <= cls.TYPE_LAST_COLOR_INT:
            return '#' + hex(data)[2:]
        elif cls.TYPE_FIRST_INT <= atype <= cls.TYPE_LAST_INT:
            return str(data)
        return ''

    @classmethod
    def complexToDimension(cls, data, metrics):
        """
        Converts a complex data value holding a dimension to its final 
        floating point value. The given data must be structured as a 
        TYPE_DIMENSION.
        :param data: int: A complex data value holding a unit, magnitude, and 
        mantissa.
        :param metrics: DisplayMetrics: Current display metrics to use in the 
        conversion -- supplies display density and scaling information.
        :return: float. The complex floating point value multiplied by the 
        appropriate metrics depending on its unit.
        """
        return cls.applyDimension(
            (data >> cls.COMPLEX_UNIT_SHIFT) & cls.COMPLEX_UNIT_MASK,
            cls.complexToFloat(data),
            metrics
        )

    @classmethod
    def complexToDimensionPixelOffset(cls, data, metrics):
        """
        Converts a complex data value holding a dimension to its final value 
        as an integer pixel offset.  This is the same as 
        complexToDimension(int, DisplayMetrics), except the raw floating point 
        value is truncated to an integer (pixel) value. The given data must be 
        structured as a TYPE_DIMENSION.
        :param data: int: A complex data value holding a unit, magnitude, and 
        mantissa.
        :param metrics: DisplayMetrics: Current display metrics to use in the 
        conversion -- supplies display density and scaling information.
        :return: int. The number of pixels specified by the data and its 
        desired multiplier and units.
        """
        return int(
            cls.complexToDimension(data, metrics)
        )

    @classmethod
    def complexToDimensionPixelSize(cls, data, metrics):
        """
        Converts a complex data value holding a dimension to its final value 
        as an integer pixel size.  This is the same as complexToDimension(int, 
        DisplayMetrics), except the raw floating point value is converted to 
        an integer (pixel) value for use as a size.  A size conversion 
        involves rounding the base value, and ensuring that a non-zero base 
        value is at least one pixel in size. The given data must be structured 
        as a TYPE_DIMENSION.
        :param data: int: A complex data value holding a unit, magnitude, and 
        mantissa.
        :param metrics: DisplayMetrics: Current display metrics to use in the 
        conversion -- supplies display density and scaling information.
        :return: int. The number of pixels specified by the data and its 
        desired multiplier and units.
        """
        value = cls.complexToFloat(data)
        f = cls.complexToDimension(data, metrics)
        res = int(f + (1 if f >= 0 else -1)*0.5*f)
        if res != 0: return res
        if value == 0: return 0
        if value > 0: return 1
        return -1

    @classmethod
    def complexToFloat(cls, complex):
        """
        Retrieve the base value from a complex data integer.  This uses the 
        COMPLEX_MANTISSA_MASK and COMPLEX_RADIX_MASK fields of the data to 
        compute a floating point representation of the number they describe.  
        The units are ignored.
        :param complex: int: A complex data value.
        :return: float. A floating point value corresponding to the complex 
        data.
        """
        MANTISSA_MULT = 1.0 / (1 << cls.COMPLEX_MANTISSA_SHIFT)
        RADIX_MULTS = [
            1.0*MANTISSA_MULT, 1.0/(1<<7)*MANTISSA_MULT,
            1.0/(1<<15)*MANTISSA_MULT, 1.0/(1<<23)*MANTISSA_MULT
        ]
        return (complex & (cls.COMPLEX_MANTISSA_MASK<<cls.COMPLEX_MANTISSA_SHIFT)) * \
               RADIX_MULTS[(complex >> cls.COMPLEX_RADIX_SHIFT) & cls.COMPLEX_RADIX_MASK]

    @classmethod
    def complexToFraction(cls, data, base, pbase):
        """
        Converts a complex data value holding a fraction to its final floating 
        point value. The given data must be structured as a TYPE_FRACTION.
        :param data: int: A complex data value holding a unit, magnitude, and 
        mantissa.
        :param base: float: The base value of this fraction.  In other words, 
        a standard fraction is multiplied by this value.
        :param pbase: float: The parent base value of this fraction.  In other 
        words, a parent fraction (nn%p) is multiplied by this value.
        :return: float. The complex floating point value multiplied by the 
        appropriate base value depending on its unit.
        """
        disc = (data >>cls.COMPLEX_UNIT_SHIFT) & cls.COMPLEX_UNIT_MASK
        if disc == cls.COMPLEX_UNIT_FRACTION:
            return cls.complexToFloat(data) * base
        elif disc == cls.COMPLEX_UNIT_FRACTION_PARENT:
            return cls.complexToFloat(data) * pbase
        return 0

    def getComplexUnit(self):
        """
        Return the complex unit type for this value. For example, a dimen type 
        with value 12sp will return COMPLEX_UNIT_SP. Only use for values whose 
        type is TYPE_DIMENSION.
        :return: int. The complex unit type.
        """
        return self.COMPLEX_UNIT_MASK & (self.data >> self.COMPLEX_UNIT_SHIFT)

    def getDimension(self, metrics):
        """
        Return the data for this value as a dimension.  Only use for values 
        whose type is TYPE_DIMENSION.
        :param metrics: DisplayMetrics: Current display metrics to use in the 
        conversion -- supplies display density and scaling information.
        :return: float. The complex floating point value multiplied by the 
        appropriate metrics depending on its unit.
        """
        return self.complexToDimension(self.data, metrics)

    def getFloat(self):
        """
        Return the data for this value as a float.  Only use for values whose 
        type is TYPE_FLOAT.
        :return: float.
        """
        return self.data

    def getFraction(self, base, pbase):
        """
        Return the data for this value as a fraction.  Only use for values 
        whose type is TYPE_FRACTION.
        :param base: float: The base value of this fraction.  In other words, 
        a standard fraction is multiplied by this value.
        :param pbase: float: The parent base value of this fraction.  In other 
        words, a parent fraction (nn%p) is multiplied by this value.
        :return: float. The complex floating point value multiplied by the 
        appropriate base value depending on its unit.
        """
        return self.complexToFraction(self.data, base, pbase)

    def setTo(self, other):
        """
        :param other: TypedValue
        """
        self.type = other.type
        self.string = other.string
        self.data = other.data
        self.assetCookie = other.assetCookie
        self.resourceId = other.resourceId
        self.density = other.density

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
        sb = ''
        sb += 'TypedValue{t=' + hex(self.type)
        sb += '/d=' + hex(self.data)
        if self.type == self.TYPE_STRING:
            sb += ' "' + (self.string if self.string else '<null>') + '"'
        if self.assetCookie:
            sb += ' a=' + str(self.assetCookie)
        if self.resourceId:
            sb += ' r=' + hex(self.resourceId)
        sb += '}'
        return sb
