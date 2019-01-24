# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/res/Configuration"""
from Android import Object, overload


class DisplayMetrics(Object):
    """
    A structure describing general information about a display, such as its 
    size, density, and font scaling. To access the DisplayMetrics members, 
    initialize an object like this:
    DisplayMetrics metrics = newDisplayMetrics();
    getWindowManager().getDefaultDisplay().getMetrics(metrics); 
    """

    """
    public static final int DENSITY_260:
    Intermediate density for screens that sit between DENSITY_HIGH (240dpi) and
    DENSITY_XHIGH (320dpi). This is not a density that applications should 
    target,
    instead relying on the system to scale their DENSITY_XHIGH assets for them.
    """
    DENSITY_260 = 0x00000104

    """
    public static final int DENSITY_280:
    Intermediate density for screens that sit between DENSITY_HIGH (240dpi) and
    DENSITY_XHIGH (320dpi). This is not a density that applications should 
    target,
    instead relying on the system to scale their DENSITY_XHIGH assets for them.
    """
    DENSITY_280 = 0x00000118

    """
    public static final int DENSITY_300:
    Intermediate density for screens that sit between DENSITY_HIGH (240dpi) and
    DENSITY_XHIGH (320dpi). This is not a density that applications should 
    target,
    instead relying on the system to scale their DENSITY_XHIGH assets for them.
    """
    DENSITY_300 = 0x0000012c

    """
    public static final int DENSITY_340:
    Intermediate density for screens that sit somewhere between
    DENSITY_XHIGH (320 dpi) and DENSITY_XXHIGH (480 dpi).
    This is not a density that applications should target, instead relying
    on the system to scale their DENSITY_XXHIGH assets for them.
    """
    DENSITY_340 = 0x00000154

    """
    public static final int DENSITY_360:
    Intermediate density for screens that sit somewhere between
    DENSITY_XHIGH (320 dpi) and DENSITY_XXHIGH (480 dpi).
    This is not a density that applications should target, instead relying
    on the system to scale their DENSITY_XXHIGH assets for them.
    """
    DENSITY_360 = 0x00000168

    """
    public static final int DENSITY_400:
    Intermediate density for screens that sit somewhere between
    DENSITY_XHIGH (320 dpi) and DENSITY_XXHIGH (480 dpi).
    This is not a density that applications should target, instead relying
    on the system to scale their DENSITY_XXHIGH assets for them.
    """
    DENSITY_400 = 0x00000190

    """
    public static final int DENSITY_420:
    Intermediate density for screens that sit somewhere between
    DENSITY_XHIGH (320 dpi) and DENSITY_XXHIGH (480 dpi).
    This is not a density that applications should target, instead relying
    on the system to scale their DENSITY_XXHIGH assets for them.
    """
    DENSITY_420 = 0x000001a4

    """
    public static final int DENSITY_440:
    Intermediate density for screens that sit somewhere between
    DENSITY_XHIGH (320 dpi) and DENSITY_XXHIGH (480 dpi).
    This is not a density that applications should target, instead relying
    on the system to scale their DENSITY_XXHIGH assets for them.
    """
    DENSITY_440 = 0x000001b8

    """
    public static final int DENSITY_560:
    Intermediate density for screens that sit somewhere between
    DENSITY_XXHIGH (480 dpi) and DENSITY_XXXHIGH (640 dpi).
    This is not a density that applications should target, instead relying
    on the system to scale their DENSITY_XXXHIGH assets for them.
    """
    DENSITY_560 = 0x00000230

    """
    public static final int DENSITY_DEFAULT:
    The reference density used throughout the system.
    """
    DENSITY_DEFAULT = 0x000000a0

    """
    public static final int DENSITY_HIGH:
    Standard quantized DPI for high-density screens.
    """
    DENSITY_HIGH = 0x000000f0

    """
    public static final int DENSITY_LOW:
    Standard quantized DPI for low-density screens.
    """
    DENSITY_LOW = 0x00000078

    """
    public static final int DENSITY_MEDIUM:
    Standard quantized DPI for medium-density screens.
    """
    DENSITY_MEDIUM = 0x000000a0

    """
    public static final int DENSITY_TV:
    This is a secondary density, added for some common screen configurations.
    It is recommended that applications not generally target this as a first
    class density -- that is, don't supply specific graphics for this
    density, instead allow the platform to scale from other densities
    (typically DENSITY_HIGH) as
    appropriate.  In most cases (such as using bitmaps in
    Drawable) the platform
    can perform this scaling at load time, so the only cost is some slight
    startup runtime overhead.
    
    This density was original introduced to correspond with a
    720p TV screen: the density for 1080p televisions is
    DENSITY_XHIGH, and the value here provides the same UI
    size for a TV running at 720p.  It has also found use in 7" tablets,
    when these devices have 1280x720 displays.
    """
    DENSITY_TV = 0x000000d5

    """
    public static final int DENSITY_XHIGH:
    Standard quantized DPI for extra-high-density screens.
    """
    DENSITY_XHIGH = 0x00000140

    """
    public static final int DENSITY_XXHIGH:
    Standard quantized DPI for extra-extra-high-density screens.
    """
    DENSITY_XXHIGH = 0x000001e0

    """
    public static final int DENSITY_XXXHIGH:
    Standard quantized DPI for extra-extra-extra-high-density screens.  
    Applications
    should not generally worry about this density; relying on XHIGH graphics
    being scaled up to it should be sufficient for almost all cases.  A typical
    use of this density would be 4K television screens -- 3840x2160, which
    is 2x a traditional HD 1920x1080 screen which runs at DENSITY_XHIGH.
    """
    DENSITY_XXXHIGH = 0x00000280

    """
    public static final int DENSITY_DEVICE_STABLE:
    The device's stable density.
    
    This value is constant at run time and may not reflect the current
    display density. To obtain the current density for a specific display,
    use densityDpi.
    """
    DENSITY_DEVICE_STABLE = None

    def __init__(self):
        super(DisplayMetrics, self).__init__()
        """
        public float density:
        The logical density of the display.  This is a scaling factor for the
        Density Independent Pixel unit, where one DIP is one pixel on an
        approximately 160 dpi screen (for example a 240x320, 1.5"x2" screen),
        providing the baseline of the system's display. Thus on a 160dpi screen
        this density value will be 1; on a 120 dpi screen it would be .75; etc.

        This value does not exactly follow the real screen size (as given by
        xdpi and ydpi, but rather is used to scale the size of
        the overall UI in steps based on gross changes in the display dpi.  For
        example, a 240x320 screen will have a density of 1 even if its width is
        1.8", 1.3", etc. However, if the screen resolution is increased to
        320x480 but the screen size remained 1.5"x2" then the density would be
        increased (probably to 1.5).See also:DENSITY_DEFAULT
        """
        self.density = None

        """
        public int densityDpi:
        The screen density expressed as dots-per-inch.  May be either
        DENSITY_LOW, DENSITY_MEDIUM, or DENSITY_HIGH.
        """
        self.densityDpi = None

        """
        public int heightPixels:
        The absolute height of the available display size in pixels.
        """
        self.heightPixels = None

        """
        public float scaledDensity:
        A scaling factor for fonts displayed on the display.  This is the same
        as density, except that it may be adjusted in smaller
        increments at runtime based on a user preference for the font size.
        """
        self.scaledDensity = None

        """
        public int widthPixels:
        The absolute width of the available display size in pixels.
        """
        self.widthPixels = None

        """
        public float xdpi:
        The exact physical pixels per inch of the screen in the X dimension.
        """
        self.xdpi = None

        """
        public float ydpi:
        The exact physical pixels per inch of the screen in the Y dimension.
        """
        self.ydpi = None

        pass

    @overload('Object')
    def equals(self, o):
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
        :param o: Object: the reference object with which to compare.
        :return: boolean. true if this object is the same as the obj argument; 
        false otherwise.
        """
        pass

    @equals.adddef('DisplayMetrics')
    def equals(self, other):
        """
        Returns true if these display metrics equal the other display metrics.
        :param other: DisplayMetrics: The display metrics with which to 
        compare.
        :return: boolean. True if the display metrics are equal.
        """
        pass

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
        pass

    def setTo(self, o):
        """
        :param o: DisplayMetrics
        """
        pass

    def setToDefaults(self):
        pass

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
        pass
