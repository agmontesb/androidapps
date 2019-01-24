# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/java/io/File"""
import os
import platform
import urlparse
import threading

from Android import overload, Object
from Android.Uri import Uri


class File(Object):
    '''
    An abstract representation of file and directory pathnames.
    '''

    """
    This object is used to syncronize the filesystem access
    """
    sync = threading.RLock()

    """
    public static final String pathSeparator:
    The system-dependent path-separator character, represented as a string
    for convenience.  This string contains a single character, namely
    pathSeparatorChar.
    """
    pathSeparator = os.path.sep

    """
    public static final char pathSeparatorChar:
    The system-dependent path-separator character.  This field is
    initialized to contain the first character of the value of the system
    property path.separator.  This character is used to
    separate filenames in a sequence of files given as a path list.
    On UNIX systems, this character is ':'; on Microsoft Windows systems it
    is ';'.See also:System.getProperty(java.lang.String)
    """
    pathSeparatorChar = os.path.sep

    """
    public static final String separator:
    The system-dependent default name-separator character, represented as a
    string for convenience.  This string contains a single character, namely
    separatorChar.
    """
    separator = '/'

    """
    public static final char separatorChar:
    The system-dependent default name-separator character.  This field is
    initialized to contain the first character of the value of the system
    property file.separator.  On UNIX systems the value of this
    field is '/'; on Microsoft Windows systems it is '\\'.See 
    also:System.getProperty(java.lang.String)
    """
    separatorChar = '/'

    system = platform.system()
    prefixSufixSep= ':' if system == 'Windows' else '/'

    @overload('str')
    def __init__(self, pathname):
        """
        :param pathname: String.
        """
        super(File, self).__init__()
        self._pathname = pathname
        if self.system == 'Windows':
            try:
                prefix, suffix = pathname.split(':', 1)
                prefix += ':'
            except:
                prefix, suffix = '', pathname
        else:
            if pathname.startswith('/'):
                prefix, suffix = pathname[0], pathname[1:]
            else:
                prefix, suffix = '', pathname
        self.prefix, self.suffix = prefix, suffix

    @__init__.adddef('str', 'str')
    def __init__(self, parent, child):
        """
        :param parent: String.
        :param child: String.
        """
        parent = File(parent)
        return self.__init__(parent, child)

    @__init__.adddef('File', 'str')
    def __init__(self, parent, child):
        """
        :param parent: File.
        :param child: String.
        """
        fchild = File(child)
        if not parent or fchild.isAbsolute():
            return self.__init__(child)
        newpathname = parent.prefix + os.path.join(parent.suffix, fchild.suffix)
        return self.__init__(newpathname)

    @__init__.adddef('URI')
    def __init__(self, uri):
        """
        :param uri: URI.
        """
        p = urlparse.urlparse(uri.toString())
        finalPath = os.path.abspath(os.path.join(p.netloc, p.path))
        return self.__init__(finalPath)

    def canExecute(self):
        """
        Tests whether the application can execute the file denoted by this 
        abstract pathname.
        :return: boolean. true if and only if the abstract pathname exists and 
        the application is allowed to execute the file
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkExec(java.lang.String) method denies execute 
        access to the file
        """
        pass

    def canRead(self):
        """
        Tests whether the application can read the file denoted by this 
        abstract pathname.
        :return: boolean. true if and only if the file specified by this 
        abstract pathname exists and can be read by the application; false 
        otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file
        """
        pass

    def canWrite(self):
        """
        Tests whether the application can modify the file denoted by this 
        abstract pathname.
        :return: boolean. true if and only if the file system actually 
        contains a file denoted by this abstract pathname and the application 
        is allowed to write to the file; false otherwise.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        pass

    def compareTo(self, pathname):
        """
        Compares two abstract pathnames lexicographically.  The ordering 
        defined by this method depends upon the underlying system.  On UNIX 
        systems, alphabetic case is significant in comparing pathnames; on 
        Microsoft Windows systems it is not.
        :param pathname: File: The abstract pathname to be compared to this 
        abstract pathname
        :return: int. Zero if the argument is equal to this abstract pathname, 
        a value less than zero if this abstract pathname is lexicographically 
        less than the argument, or a value greater than zero if this abstract 
        pathname is lexicographically greater than the argument
        """
        pass

    def createNewFile(self):
        """
        Atomically creates a new, empty file named by this abstract pathname 
        if and only if a file with this name does not yet exist.  The check 
        for the existence of the file and the creation of the file if it does 
        not exist are a single operation that is atomic with respect to all 
        other filesystem activities that might affect the file.  Note: this 
        method should not be used for file-locking, as the resulting protocol 
        cannot be made to work reliably. The FileLock facility should be used 
        instead.
        :return: boolean. true if the named file does not exist and was 
        successfully created; false if the named file already exists
        :raises:
        IOException: If an I/O error occurred
        SecurityException: If a security manager exists and its
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        with self.sync:
            if self.isFile() and not self.exists():
                filename = self.getPath()
                try:
                    with open(filename, 'w') as f:
                        pass
                    return self.exists()
                except:
                    raise Exception('IOException or SecurityException')
            return False

    @overload('str', '@str', '@File')
    def createTempFile(self, prefix, suffix, directory):
        """
        Creates a new empty file in the specified directory, using the given 
        prefix and suffix strings to generate its name.  If this method 
        returns successfully then it is guaranteed that:  The file denoted by 
        the returned abstract pathname did not exist before this method was 
        invoked, and Neither this method nor any of its variants will return 
        the same abstract pathname again in the current invocation of the 
        virtual machine.   This method provides only part of a temporary-file 
        facility.  To arrange for a file created by this method to be deleted 
        automatically, use the deleteOnExit() method.  The prefix argument 
        must be at least three characters long.  It is recommended that the 
        prefix be a short, meaningful string such as "hjb" or "mail".  The 
        suffix argument may be null, in which case the suffix ".tmp" will be 
        used.  To create the new file, the prefix and the suffix may first be 
        adjusted to fit the limitations of the underlying platform.  If the 
        prefix is too long then it will be truncated, but its first three 
        characters will always be preserved.  If the suffix is too long then 
        it too will be truncated, but if it begins with a period character 
        ('.') then the period and the first three characters following it will 
        always be preserved.  Once these adjustments have been made the name 
        of the new file will be generated by concatenating the prefix, five or 
        more internally-generated characters, and the suffix.  If the 
        directory argument is null then the system-dependent default 
        temporary-file directory will be used.  The default temporary-file 
        directory is specified by the system property java.io.tmpdir.  On UNIX 
        systems the default value of this property is typically "/tmp" or 
        "/var/tmp"; on Microsoft Windows systems it is typically 
        "C:\\WINNT\\TEMP".  A different value may be given to this system 
        property when the Java virtual machine is invoked, but programmatic 
        changes to this property are not guaranteed to have any effect upon 
        the temporary directory used by this method.
        :param prefix: String: The prefix string to be used in generating the 
        file's name; must be at least three characters long
        :param suffix: String: The suffix string to be used in generating the 
        file's name; may be null, in which case the suffix ".tmp" will be used
        :param directory: File: The directory in which the file is to be 
        created, or null if the default temporary-file directory is to be used
        :return: File. An abstract pathname denoting a newly-created empty file
        :raises: IllegalArgumentExceptionIf the prefix argument contains fewer 
        than three charactersIOExceptionIf a file could not be 
        createdSecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method does not allow a 
        file to be created
        """
        pass

    @classmethod
    @createTempFile.adddef('str', 'str')
    def createTempFile(self, prefix, suffix):
        """
        Creates an empty file in the default temporary-file directory, using 
        the given prefix and suffix to generate its name. Invoking this method 
        is equivalent to invoking 
        createTempFile(prefix,&nbsp;suffix,&nbsp;null).  The 
        Files.createTempFile method provides an alternative method to create 
        an empty file in the temporary-file directory. Files created by that 
        method may have more restrictive access permissions to files created 
        by this method and so may be more suited to security-sensitive 
        applications.
        :param prefix: String: The prefix string to be used in generating the 
        file's name; must be at least three characters long
        :param suffix: String: The suffix string to be used in generating the 
        file's name; may be null, in which case the suffix ".tmp" will be used
        :return: File. An abstract pathname denoting a newly-created empty file
        :raises: IllegalArgumentExceptionIf the prefix argument contains fewer 
        than three charactersIOExceptionIf a file could not be 
        createdSecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method does not allow a 
        file to be created
        See also:
        Files.createTempDirectory(String, FileAttribute[])
        """
        pass

    def delete(self):
        """
        Deletes the file or directory denoted by this abstract pathname.  If 
        this pathname denotes a directory, then the directory must be empty in 
        order to be deleted.  Note that the Files class defines the delete 
        method to throw an IOException when a file cannot be deleted. This is 
        useful for error reporting and to diagnose why a file cannot be 
        deleted.
        :return: boolean. true if and only if the file or directory is 
        successfully deleted; false otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkDelete(String) method denies delete access to the 
        file
        """
        pass

    def deleteOnExit(self):
        """
        Requests that the file or directory denoted by this abstract pathname 
        be deleted when the virtual machine terminates. Files (or directories) 
        are deleted in the reverse order that they are registered. Invoking 
        this method to delete a file or directory that is already registered 
        for deletion has no effect. Deletion will be attempted only for normal 
        termination of the virtual machine, as defined by the Java Language 
        Specification.  Once deletion has been requested, it is not possible 
        to cancel the request.  This method should therefore be used with 
        care.   Note: this method should not be used for file-locking, as the 
        resulting protocol cannot be made to work reliably. The FileLock 
        facility should be used instead.  Note that on Android, the 
        application lifecycle does not include VM termination, so calling this 
        method will not ensure that files are deleted. Instead, you should use 
        the most appropriate out of: Use a finally clause to manually invoke 
        delete(). Maintain your own set of files to delete, and process it at 
        an appropriate point in your application's lifecycle. Use the Unix 
        trick of deleting the file as soon as all readers and writers have 
        opened it. No new readers/writers will be able to access the file, but 
        all existing ones will still have access until the last one closes the 
        file.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkDelete(String) method denies delete access to the 
        file
        See also: delete()
        """
        pass

    def equals(self, obj):
        """
        Tests this abstract pathname for equality with the given object. 
        Returns true if and only if the argument is not null and is an 
        abstract pathname that denotes the same file or directory as this 
        abstract pathname.  Whether or not two abstract pathnames are equal 
        depends upon the underlying system.  On UNIX systems, alphabetic case 
        is significant in comparing pathnames; on Microsoft Windows systems it 
        is not.
        :param obj: Object: The object to be compared with this abstract 
        pathname
        :return: boolean. true if and only if the objects are the same; false 
        otherwise
        """
        return self.toString() == obj.toString()

    def exists(self):
        """
        Tests whether the file or directory denoted by this abstract pathname 
        exists.
        :return: boolean. true if and only if the file or directory denoted by 
        this abstract pathname exists; false otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file or directory
        """
        return os.path.exists(self.getPath())

    def getAbsoluteFile(self):
        """
        Returns the absolute form of this abstract pathname.  Equivalent to 
        new&nbsp;File(this.getAbsolutePath()).
        :return: File. The absolute abstract pathname denoting the same file 
        or directory as this abstract pathname
        :raises: SecurityExceptionIf a required system property value cannot 
        be accessed.
        """
        return File(self.getAbsolutePath())

    def getAbsolutePath(self):
        """
        Returns the absolute path of this file. An absolute path is a path 
        that starts at a root of the file system. On Android, there is only 
        one root: /.  A common use for absolute paths is when passing paths to 
        a Process as command-line arguments, to remove the requirement implied 
        by relative paths, that the child must have the same working directory 
        as its parent.
        :return: String. The absolute pathname string denoting the same file 
        or directory as this abstract pathname
        See also: isAbsolute()
        """
        prefix, suffix = self.prefix, self.suffix
        if self.isAbsolute():
            suffix = suffix[1:]
        else:
            prefix = '.'
        return os.path.abspath(os.path.join(prefix, suffix))

    def getCanonicalFile(self):
        """
        Returns the canonical form of this abstract pathname.  Equivalent to 
        new&nbsp;File(this.getCanonicalPath()).
        :return: File. The canonical pathname string denoting the same file or 
        directory as this abstract pathname
        :raises: IOExceptionIf an I/O error occurs, which is possible because 
        the construction of the canonical pathname may require filesystem 
        queriesSecurityExceptionIf a required system property value cannot be 
        accessed, or if a security manager exists and its 
        SecurityManager.checkRead(FileDescriptor) method denies read access to 
        the file
        See also:
        Path.toRealPath(LinkOption...)
        """
        return File(self.getCanonicalPath())

    def getCanonicalPath(self):
        """
        Returns the canonical pathname string of this abstract pathname.  A 
        canonical pathname is both absolute and unique.  The precise 
        definition of canonical form is system-dependent.  This method first 
        converts this pathname to absolute form if necessary, as if by 
        invoking the getAbsolutePath() method, and then maps it to its unique 
        form in a system-dependent way.  This typically involves removing 
        redundant names such as "." and ".." from the pathname, resolving 
        symbolic links (on UNIX platforms), and converting drive letters to a 
        standard case (on Microsoft Windows platforms).  Every pathname that 
        denotes an existing file or directory has a unique canonical form.  
        Every pathname that denotes a nonexistent file or directory also has a 
        unique canonical form.  The canonical form of the pathname of a 
        nonexistent file or directory may be different from the canonical form 
        of the same pathname after the file or directory is created.  
        Similarly, the canonical form of the pathname of an existing file or 
        directory may be different from the canonical form of the same 
        pathname after the file or directory is deleted.
        :return: String. The canonical pathname string denoting the same file 
        or directory as this abstract pathname
        :raises: IOExceptionIf an I/O error occurs, which is possible because 
        the construction of the canonical pathname may require filesystem 
        queriesSecurityExceptionIf a required system property value cannot be 
        accessed, or if a security manager exists and its 
        SecurityManager.checkRead(FileDescriptor) method denies read access to 
        the file
        See also: Path.toRealPath(LinkOption...)
        """
        abspath = self.getAbsolutePath()
        return os.path.expanduser(os.path.expandvars(abspath))

    def getFreeSpace(self):
        """
        Returns the number of unallocated bytes in the partition named by this 
        abstract path name.  The returned number of unallocated bytes is a 
        hint, but not a guarantee, that it is possible to use most or any of 
        these bytes.  The number of unallocated bytes is most likely to be 
        accurate immediately after this call.  It is likely to be made 
        inaccurate by any external I/O operations including those made on the 
        system outside of this virtual machine.  This method makes no 
        guarantee that write operations to this file system will succeed.
        :return: long. The number of unallocated bytes on the partition or 0L 
        if the abstract pathname does not name a partition.  This value will 
        be less than or equal to the total file system size returned by 
        getTotalSpace().
        :raises: SecurityExceptionIf a security manager has been installed and 
        it denies RuntimePermission("getFileSystemAttributes") or its 
        SecurityManager.checkRead(String) method denies read access to the 
        file named by this abstract pathname
        """
        pass

    def getName(self):
        """
        Returns the name of the file or directory denoted by this abstract 
        pathname.  This is just the last name in the pathname's name sequence. 
         If the pathname's name sequence is empty, then the empty string is 
        returned.
        :return: String. The name of the file or directory denoted by this 
        abstract pathname, or the empty string if this pathname's name 
        sequence is empty
        """
        return os.path.basename(self.suffix)

    def getParent(self):
        """
        Returns the pathname string of this abstract pathname's parent, or 
        null if this pathname does not name a parent directory.  The parent of 
        an abstract pathname consists of the pathname's prefix, if any, and 
        each name in the pathname's name sequence except for the last.  If the 
        name sequence is empty then the pathname does not name a parent 
        directory.
        :return: String. The pathname string of the parent directory named by 
        this abstract pathname, or null if this pathname does not name a parent
        """
        return self.prefix + os.path.dirname(self.suffix)

    def getParentFile(self):
        """
        Returns the abstract pathname of this abstract pathname's parent, or 
        null if this pathname does not name a parent directory.  The parent of 
        an abstract pathname consists of the pathname's prefix, if any, and 
        each name in the pathname's name sequence except for the last.  If the 
        name sequence is empty then the pathname does not name a parent 
        directory.
        :return: File. The abstract pathname of the parent directory named by 
        this abstract pathname, or null if this pathname does not name a parent
        """
        return File(self.getParent())

    def getPath(self):
        """
        Converts this abstract pathname into a pathname string.  The resulting 
        string uses the default name-separator character to separate the names 
        in the name sequence.
        :return: String. The string form of this abstract pathname
        """
        return self.prefix + self.suffix

    def getTotalSpace(self):
        """
        Returns the size of the partition named by this abstract pathname.
        :return: long. The size, in bytes, of the partition or 0L if this 
        abstract pathname does not name a partition
        :raises: SecurityExceptionIf a security manager has been installed and 
        it denies RuntimePermission("getFileSystemAttributes") or its 
        SecurityManager.checkRead(String) method denies read access to the 
        file named by this abstract pathname
        """
        pass

    def getUsableSpace(self):
        """
        Returns the number of bytes available to this virtual machine on the 
        partition named by this abstract pathname.  When possible, this method 
        checks for write permissions and other operating system restrictions 
        and will therefore usually provide a more accurate estimate of how 
        much new data can actually be written than getFreeSpace().  The 
        returned number of available bytes is a hint, but not a guarantee, 
        that it is possible to use most or any of these bytes.  The number of 
        unallocated bytes is most likely to be accurate immediately after this 
        call.  It is likely to be made inaccurate by any external I/O 
        operations including those made on the system outside of this virtual 
        machine.  This method makes no guarantee that write operations to this 
        file system will succeed.  On Android (and other Unix-based systems), 
        this method returns the number of free bytes available to non-root 
        users, regardless of whether you're actually running as root, and 
        regardless of any quota or other restrictions that might apply to the 
        user. (The getFreeSpace method returns the number of bytes potentially 
        available to root.)
        :return: long. The number of available bytes on the partition or 0L if 
        the abstract pathname does not name a partition.  On systems where 
        this information is not available, this method will be equivalent to a 
        call to getFreeSpace().
        :raises: SecurityExceptionIf a security manager has been installed and 
        it denies RuntimePermission("getFileSystemAttributes") or its 
        SecurityManager.checkRead(String) method denies read access to the 
        file named by this abstract pathname
        """
        pass

    def hashCode(self):
        """
        Computes a hash code for this abstract pathname.  Because equality of 
        abstract pathnames is inherently system-dependent, so is the 
        computation of their hash codes.  On UNIX systems, the hash code of an 
        abstract pathname is equal to the exclusive or of the hash code of its 
        pathname string and the decimal value 1234321.  On Microsoft Windows 
        systems, the hash code is equal to the exclusive or of the hash code 
        of its pathname string converted to lower case and the decimal value 
        1234321.  Locale is not taken into account on lowercasing the pathname 
        string.
        :return: int. A hash code for this abstract pathname
        """
        pathname = self.getPath()
        if self.system == 'Windows':
            pathname= pathname.lower()
        return pathname.__hash__() ^ 1234321

    def isAbsolute(self):
        """
        Tests whether this abstract pathname is absolute.  The definition of 
        absolute pathname is system dependent.  On Android, absolute paths 
        start with the character '/'.
        :return: boolean. true if this abstract pathname is absolute, false 
        otherwise
        """
        return bool(self.prefix)

    def isDirectory(self):
        """
        Tests whether the file denoted by this abstract pathname is a 
        directory.  Where it is required to distinguish an I/O exception from 
        the case that the file is not a directory, or where several attributes 
        of the same file are required at the same time, then the 
        Files.readAttributes method may be used.
        :return: boolean. true if and only if the file denoted by this 
        abstract pathname exists and is a directory; false otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file
        """
        return self.exists() and os.path.isdir(self.getPath())

    def isFile(self):
        """
        Tests whether the file denoted by this abstract pathname is a normal 
        file.  A file is normal if it is not a directory and, in addition, 
        satisfies other system-dependent criteria.  Any non-directory file 
        created by a Java application is guaranteed to be a normal file.  
        Where it is required to distinguish an I/O exception from the case 
        that the file is not a normal file, or where several attributes of the 
        same file are required at the same time, then the Files.readAttributes 
        method may be used.
        :return: boolean. true if and only if the file denoted by this 
        abstract pathname exists and is a normal file; false otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file
        """
        return os.path.isfile(self.getPath())

    def isHidden(self):
        """
        Tests whether the file named by this abstract pathname is a hidden 
        file.  The exact definition of hidden is system-dependent.  On UNIX 
        systems, a file is considered to be hidden if its name begins with a 
        period character ('.').  On Microsoft Windows systems, a file is 
        considered to be hidden if it has been marked as such in the 
        filesystem.
        :return: boolean. true if and only if the file denoted by this 
        abstract pathname is hidden according to the conventions of the 
        underlying platform
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file
        """
        pass

    def lastModified(self):
        """
        Returns the time that the file denoted by this abstract pathname was 
        last modified.  Where it is required to distinguish an I/O exception 
        from the case where 0L is returned, or where several attributes of the 
        same file are required at the same time, or where the time of last 
        access or the creation time are required, then the 
        Files.readAttributes method may be used.
        :return: long. A long value representing the time the file was last 
        modified, measured in milliseconds since the epoch (00:00:00 GMT, 
        January 1, 1970), or 0L if the file does not exist or if an I/O error 
        occurs
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file
        """
        return os.path.getmtime(self.getPath())

    def length(self):
        """
        Returns the length of the file denoted by this abstract pathname. The 
        return value is unspecified if this pathname denotes a directory.  
        Where it is required to distinguish an I/O exception from the case 
        that 0L is returned, or where several attributes of the same file are 
        required at the same time, then the Files.readAttributes method may be 
        used.
        :return: long. The length, in bytes, of the file denoted by this 
        abstract pathname, or 0L if the file does not exist.  Some operating 
        systems may return 0L for pathnames denoting system-dependent entities 
        such as devices or pipes.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method denies read access 
        to the file
        """
        return os.path.getsize(self.getPath())

    @overload
    def list(self):
        """
        Returns an array of strings naming the files and directories in the 
        directory denoted by this abstract pathname.  If this abstract 
        pathname does not denote a directory, then this method returns null.  
        Otherwise an array of strings is returned, one for each file or 
        directory in the directory.  Names denoting the directory itself and 
        the directory's parent directory are not included in the result.  Each 
        string is a file name rather than a complete path.  There is no 
        guarantee that the name strings in the resulting array will appear in 
        any specific order; they are not, in particular, guaranteed to appear 
        in alphabetical order.  Note that the Files class defines the 
        newDirectoryStream method to open a directory and iterate over the 
        names of the files in the directory. This may use less resources when 
        working with very large directories, and may be more responsive when 
        working with remote directories.
        :return: String[]. An array of strings naming the files and 
        directories in the directory denoted by this abstract pathname.  The 
        array will be empty if the directory is empty.  Returns null if this 
        abstract pathname does not denote a directory, or if an I/O error 
        occurs.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(String) method denies read access to the 
        directory
        """
        pass

    @overload('FilenameFilter')
    def list(self, filter):
        """
        Returns an array of strings naming the files and directories in the
        directory denoted by this abstract pathname that satisfy the specified
        filter.  The behavior of this method is the same as that of the list()
        method, except that the strings in the returned array must satisfy the
        filter.  If the given filter is null then all names are accepted.
        Otherwise, a name satisfies the filter if and only if the value true
        results when the FilenameFilter.accept(File,&nbsp;String) method of
        the filter is invoked on this abstract pathname and the name of a file
        or directory in the directory that it denotes.
        :param filter: FilenameFilter: A filename filter
        :return: String[]. An array of strings naming the files and
        directories in the directory denoted by this abstract pathname that
        were accepted by the given filter.  The array will be empty if the
        directory is empty or if no names were accepted by the filter. Returns
        null if this abstract pathname does not denote a directory, or if an
        I/O error occurs.
        :raises: SecurityExceptionIf a security manager exists and its
        SecurityManager.checkRead(String) method denies read access to the
        directory
        See also: Files.newDirectoryStream(Path, String)
        """
        pass

    @overload
    def listFiles(self):
        """
        Returns an array of abstract pathnames denoting the files in the 
        directory denoted by this abstract pathname.  If this abstract 
        pathname does not denote a directory, then this method returns null.  
        Otherwise an array of File objects is returned, one for each file or 
        directory in the directory.  Pathnames denoting the directory itself 
        and the directory's parent directory are not included in the result.  
        Each resulting abstract pathname is constructed from this abstract 
        pathname using the File(File,&nbsp;String) constructor.  Therefore if 
        this pathname is absolute then each resulting pathname is absolute; if 
        this pathname is relative then each resulting pathname will be 
        relative to the same directory.  There is no guarantee that the name 
        strings in the resulting array will appear in any specific order; they 
        are not, in particular, guaranteed to appear in alphabetical order.  
        Note that the Files class defines the newDirectoryStream method to 
        open a directory and iterate over the names of the files in the 
        directory. This may use less resources when working with very large 
        directories.
        :return: File[]. An array of abstract pathnames denoting the files and 
        directories in the directory denoted by this abstract pathname. The 
        array will be empty if the directory is empty.  Returns null if this 
        abstract pathname does not denote a directory, or if an I/O error 
        occurs.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(String) method denies read access to the 
        directory
        """
        pass

    @listFiles.adddef('FileFilter')
    def listFiles(self, filter):
        """
        Returns an array of abstract pathnames denoting the files and 
        directories in the directory denoted by this abstract pathname that 
        satisfy the specified filter.  The behavior of this method is the same 
        as that of the listFiles() method, except that the pathnames in the 
        returned array must satisfy the filter.  If the given filter is null 
        then all pathnames are accepted.  Otherwise, a pathname satisfies the 
        filter if and only if the value true results when the 
        FileFilter.accept(File) method of the filter is invoked on the 
        pathname.
        :param filter: FileFilter: A file filter
        :return: File[]. An array of abstract pathnames denoting the files and 
        directories in the directory denoted by this abstract pathname. The 
        array will be empty if the directory is empty.  Returns null if this 
        abstract pathname does not denote a directory, or if an I/O error 
        occurs.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(String) method denies read access to the 
        directory
        See also: Files.newDirectoryStream(Path, 
        java.nio.file.DirectoryStream.Filter)
        """
        pass

    @listFiles.adddef('FilenameFilter')
    def listFiles(self, filter):
        """
        Returns an array of abstract pathnames denoting the files and 
        directories in the directory denoted by this abstract pathname that 
        satisfy the specified filter.  The behavior of this method is the same 
        as that of the listFiles() method, except that the pathnames in the 
        returned array must satisfy the filter.  If the given filter is null 
        then all pathnames are accepted.  Otherwise, a pathname satisfies the 
        filter if and only if the value true results when the 
        FilenameFilter.accept(File,&nbsp;String) method of the filter is 
        invoked on this abstract pathname and the name of a file or directory 
        in the directory that it denotes.
        :param filter: FilenameFilter: A filename filter
        :return: File[]. An array of abstract pathnames denoting the files and 
        directories in the directory denoted by this abstract pathname. The 
        array will be empty if the directory is empty.  Returns null if this 
        abstract pathname does not denote a directory, or if an I/O error 
        occurs.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(String) method denies read access to the 
        directory
        See also: Files.newDirectoryStream(Path, String)
        """
        pass

    @classmethod
    def listRoots(self):
        """
        Returns the file system roots. On Android and other Unix systems, 
        there is a single root, /.
        :return: File[].
        """
        pass

    def mkdir(self):
        """
        Creates the directory named by this abstract pathname.
        :return: boolean. true if and only if the directory was created; false 
        otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method does not permit 
        the named directory to be created
        """
        try:
            os.mkdir(self.getPath())
            return True
        except OSError:
            return False
        except:
            raise Exception('SecurityException')


    def mkdirs(self):
        """
        Creates the directory named by this abstract pathname, including any 
        necessary but nonexistent parent directories.  Note that if this 
        operation fails it may have succeeded in creating some of the 
        necessary parent directories.
        :return: boolean. true if and only if the directory was created, along 
        with all necessary parent directories; false otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkRead(java.lang.String) method does not permit 
        verification of the existence of the named directory and all necessary 
        parent directories; or if the 
        SecurityManager.checkWrite(java.lang.String) method does not permit 
        the named directory and all necessary parent directories to be created
        """
        try:
            os.mkdirs(self.getPath())
            return True
        except OSError:
            return False
        except:
            raise Exception('SecurityException')

    def renameTo(self, dest):
        """
        Renames the file denoted by this abstract pathname.  Many failures are 
        possible. Some of the more likely failures include: Write permission 
        is required on the directories containing both the source and 
        destination paths. Search permission is required for all parents of 
        both paths. Both paths be on the same mount point. On Android, 
        applications are most likely to hit this restriction when attempting 
        to copy between internal storage and an SD card. The return value 
        should always be checked to make sure that the rename operation was 
        successful.  Note that the Files class defines the move method to move 
        or rename a file in a platform independent manner.
        :param dest: File: The new abstract pathname for the named file
        :return: boolean. true if and only if the renaming succeeded; false 
        otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to either the old or new pathnamesNullPointerExceptionIf 
        parameter dest is null
        """
        pass

    @overload('bool', 'bool')
    def setExecutable(self, executable, ownerOnly):
        """
        Sets the owner's or everybody's execute permission for this abstract 
        pathname.  The Files class defines methods that operate on file 
        attributes including file permissions. This may be used when finer 
        manipulation of file permissions is required.
        :param executable: boolean: If true, sets the access permission to 
        allow execute operations; if false to disallow execute operations
        :param ownerOnly: boolean: If true, the execute permission applies 
        only to the owner's execute permission; otherwise, it applies to 
        everybody. If the underlying file system can not distinguish the 
        owner's execute permission from that of others, then the permission 
        will apply to everybody, regardless of this value.
        :return: boolean. true if and only if the operation succeeded.  The 
        operation will fail if the user does not have permission to change the 
        access permissions of this abstract pathname.  If executable is false 
        and the underlying file system does not implement an execute 
        permission, then the operation will fail.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        pass

    @setExecutable.adddef('bool')
    def setExecutable(self, executable):
        """
        A convenience method to set the owner's execute permission for this 
        abstract pathname.  An invocation of this method of the form 
        file.setExcutable(arg) behaves in exactly the same way as the 
        invocation   file.setExecutable(arg, true)
        :param executable: boolean: If true, sets the access permission to 
        allow execute operations; if false to disallow execute operations
        :return: boolean. true if and only if the operation succeeded.  The 
        operation will fail if the user does not have permission to change the 
        access permissions of this abstract pathname.  If executable is false 
        and the underlying file system does not implement an execute 
        permission, then the operation will fail.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        pass

    def setLastModified(self, time):
        """
        Sets the last-modified time of the file or directory named by this 
        abstract pathname.  All platforms support file-modification times to 
        the nearest second, but some provide more precision.  The argument 
        will be truncated to fit the supported precision.  If the operation 
        succeeds and no intervening operations on the file take place, then 
        the next invocation of the lastModified() method will return the 
        (possibly truncated) time argument that was passed to this method.
        :param time: long: The new last-modified time, measured in 
        milliseconds since the epoch (00:00:00 GMT, January 1, 1970)
        :return: boolean. true if and only if the operation succeeded; false 
        otherwise
        :raises: IllegalArgumentExceptionIf the argument is 
        negativeSecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the named file
        """
        pass

    def setReadOnly(self):
        """
        Marks the file or directory named by this abstract pathname so that 
        only read operations are allowed. After invoking this method the file 
        or directory will not change until it is either deleted or marked to 
        allow write access. Whether or not a read-only file or directory may 
        be deleted depends upon the underlying system.
        :return: boolean. true if and only if the operation succeeded; false 
        otherwise
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the named file
        """
        pass

    @overload('bool')
    def setReadable(self, readable):
        """
        A convenience method to set the owner's read permission for this 
        abstract pathname.  An invocation of this method of the form 
        file.setReadable(arg) behaves in exactly the same way as the 
        invocation   file.setReadable(arg, true)
        :param readable: boolean: If true, sets the access permission to allow 
        read operations; if false to disallow read operations
        :return: boolean. true if and only if the operation succeeded.  The 
        operation will fail if the user does not have permission to change the 
        access permissions of this abstract pathname.  If readable is false 
        and the underlying file system does not implement a read permission, 
        then the operation will fail.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        pass

    @setReadable.adddef('bool', 'bool')
    def setReadable(self, readable, ownerOnly):
        """
        Sets the owner's or everybody's read permission for this abstract 
        pathname.  The Files class defines methods that operate on file 
        attributes including file permissions. This may be used when finer 
        manipulation of file permissions is required.
        :param readable: boolean: If true, sets the access permission to allow 
        read operations; if false to disallow read operations
        :param ownerOnly: boolean: If true, the read permission applies only 
        to the owner's read permission; otherwise, it applies to everybody.  
        If the underlying file system can not distinguish the owner's read 
        permission from that of others, then the permission will apply to 
        everybody, regardless of this value.
        :return: boolean. true if and only if the operation succeeded.  The 
        operation will fail if the user does not have permission to change the 
        access permissions of this abstract pathname.  If readable is false 
        and the underlying file system does not implement a read permission, 
        then the operation will fail.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        pass

    @overload('bool', 'bool')
    def setWritable(self, writable, ownerOnly):
        """
        Sets the owner's or everybody's write permission for this abstract 
        pathname.  The Files class defines methods that operate on file 
        attributes including file permissions. This may be used when finer 
        manipulation of file permissions is required.
        :param writable: boolean: If true, sets the access permission to allow 
        write operations; if false to disallow write operations
        :param ownerOnly: boolean: If true, the write permission applies only 
        to the owner's write permission; otherwise, it applies to everybody.  
        If the underlying file system can not distinguish the owner's write 
        permission from that of others, then the permission will apply to 
        everybody, regardless of this value.
        :return: boolean. true if and only if the operation succeeded. The 
        operation will fail if the user does not have permission to change the 
        access permissions of this abstract pathname.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the named file
        """
        pass

    @setWritable.adddef('bool')
    def setWritable(self, writable):
        """
        A convenience method to set the owner's write permission for this 
        abstract pathname.  An invocation of this method of the form 
        file.setWritable(arg) behaves in exactly the same way as the 
        invocation   file.setWritable(arg, true)
        :param writable: boolean: If true, sets the access permission to allow 
        write operations; if false to disallow write operations
        :return: boolean. true if and only if the operation succeeded.  The 
        operation will fail if the user does not have permission to change the 
        access permissions of this abstract pathname.
        :raises: SecurityExceptionIf a security manager exists and its 
        SecurityManager.checkWrite(java.lang.String) method denies write 
        access to the file
        """
        pass

    def toPath(self):
        """
        Returns a java.nio.file.Path object constructed from the this abstract 
        path. The resulting Path is associated with the default-filesystem.  
        The first invocation of this method works as if invoking it were 
        equivalent to evaluating the expression: 
        FileSystems.getDefault().getPath(this.getPath());  Subsequent 
        invocations of this method return the same Path.  If this abstract 
        pathname is the empty abstract pathname then this method returns a 
        Path that may be used to access the current user directory.
        :return: Path. a Path constructed from this abstract path
        :raises: InvalidPathExceptionif a Path object cannot be constructed 
        from the abstract path (see FileSystem.getPath)
        See also: Path.toFile()
        """
        pass

    def toString(self):
        """
        Returns the pathname string of this abstract pathname.  This is just 
        the string returned by the getPath() method.
        :return: String. The string form of this abstract pathname
        """
        return self.getPath()

    def toURI(self):
        """
        Constructs a file: URI that represents this abstract pathname.  The 
        exact form of the URI is system-dependent.  If it can be determined 
        that the file denoted by this abstract pathname is a directory, then 
        the resulting URI will end with a slash.  For a given abstract 
        pathname f, it is guaranteed that   new 
        File(&nbsp;f.toURI()).equals(&nbsp;f.getAbsoluteFile())   so long as 
        the original abstract pathname, the URI, and the new abstract pathname 
        are all created in (possibly different invocations of) the same Java 
        virtual machine.  Due to the system-dependent nature of abstract 
        pathnames, however, this relationship typically does not hold when a 
        file: URI that is created in a virtual machine on one operating system 
        is converted into an abstract pathname in a virtual machine on a 
        different operating system.  Note that when this abstract pathname 
        represents a UNC pathname then all components of the UNC (including 
        the server name component) are encoded in the URI path. The authority 
        component is undefined, meaning that it is represented as null. The 
        Path class defines the toUri method to encode the server name in the 
        authority component of the resulting URI. The toPath method may be 
        used to obtain a Path representing this abstract pathname.
        :return: URI. An absolute, hierarchical URI with a scheme equal to 
        "file", a path representing this abstract pathname, and undefined 
        authority, query, and fragment components
        :raises: SecurityExceptionIf a required system property value cannot 
        be accessed.
        See also: File(java.net.URI)URIURI.toURL()
        """
        return Uri.fromFile(self.getPath())

    def toURL(self):
        """
        This method was deprecated in API level 9. This method does not 
        automatically escape characters that are illegal in URLs.  It is 
        recommended that new code convert an abstract pathname into a URL by 
        first converting it into a URI, via the toURI method, and then 
        converting the URI into a URL via the URI.toURL method.  Converts this 
        abstract pathname into a file: URL.  The exact form of the URL is 
        system-dependent.  If it can be determined that the file denoted by 
        this abstract pathname is a directory, then the resulting URL will end 
        with a slash.
        :return: URL. A URL object representing the equivalent file URL
        :raises: MalformedURLExceptionIf the path cannot be parsed as a URL
        See also: toURI()URIURI.toURL()URL
        """
        pass
