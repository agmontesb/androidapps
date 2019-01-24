# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/util/Log"""
from Android import Object, overload

"""
public static final int ASSERT:
Priority constant for the println method.
"""
ASSERT = 0x00000007

"""
public static final int DEBUG:
Priority constant for the println method; use Log.d.
"""
DEBUG = 0x00000003

"""
public static final int ERROR:
Priority constant for the println method; use Log.e.
"""
ERROR = 0x00000006

"""
public static final int INFO:
Priority constant for the println method; use Log.i.
"""
INFO = 0x00000004

"""
public static final int VERBOSE:
Priority constant for the println method; use Log.v.
"""
VERBOSE = 0x00000002

"""
public static final int WARN:
Priority constant for the println method; use Log.w.
"""
WARN = 0x00000005


class Log(Object):
    @classmethod
    def d(self, tag, msg, tr=None):
        """
        Send a DEBUG log message and log the exception.
        :param tag: String: Used to identify the source of a log message.  It
        usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :param tr: Throwable: An exception to log
        :return: int.
        """
        pass

    @classmethod
    def e(self, tag, msg, tr=None):
        """
        Send a ERROR log message and log the exception.
        :param tag: String: Used to identify the source of a log message.  It
        usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :param tr: Throwable: An exception to log
        :return: int.
        """
        pass

    @classmethod
    def getStackTraceString(self, tr):
        """
        Handy function to get a loggable stack trace from a Throwable
        :param tr: Throwable: An exception to log
        :return: String.
        """
        pass

    @classmethod
    def i(self, tag, msg, tr=None):
        """
        Send an INFO log message and log the exception.
        :param tag: String: Used to identify the source of a log message.  It
        usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :param tr: Throwable: An exception to log
        :return: int.
        """
        pass

    @classmethod
    def isLoggable (cls, tag, level):
        """
        Checks to see whether or not a log for the specified tag is loggable at the
        specified level. The default level of any tag is set to INFO. This means
        that any level above and including INFO will be logged. Before you make any
        calls to a logging method you should check to see if your tag should be logged.
        You can change the default level by setting a system property:
                        'setprop log.tag.<YOUR_LOG_TAG> <LEVEL>'
        Where level is either VERBOSE, DEBUG, INFO, WARN, ERROR, ASSERT, or SUPPRESS.
        SUPPRESS will turn off all logging for your tag. You can also create a
        local.prop file that with the following in it: 'log.tag.<YOUR_LOG_TAG>=<LEVEL>'
        and place that in /data/local.prop.
        :param tag: String: The tag to check.
        :param level: int: The level to check.
        :return: boolean: Whether or not that this is allowed to be logged.
        """
        pass

    @classmethod
    def println (cls, priority, tag, msg):
        """
        Low-level logging call.
        :param priority: int: The priority/type of this log message
        :param tag: String: Used to identify the source of a log message.
        It usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :return: int: The number of bytes written.
        """
        pass

    @classmethod
    def v(self, tag, msg, tr=None):
        """
        Send an VERBOSE log message and log the exception.
        :param tag: String: Used to identify the source of a log message.  It
        usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :param tr: Throwable: An exception to log
        :return: int.
        """
        pass

    @classmethod
    def w(self, tag, msg, tr=None):
        """
        Send an WARN log message and log the exception.
        :param tag: String: Used to identify the source of a log message.  It
        usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :param tr: Throwable: An exception to log
        :return: int.
        """
        pass

    @classmethod
    def wtf(self, tag, msg=None, tr=None):
        """
        What a Terrible Failure: Report an exception that should never happen.
        :param tag: String: Used to identify the source of a log message.  It
        usually identifies the class or activity where the log call occurs.
        :param msg: String: The message you would like logged.
        :param tr: Throwable: An exception to log
        :return: int.
        """
        pass


