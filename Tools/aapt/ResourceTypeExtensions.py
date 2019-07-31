# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1a008c1/tools/aapt2/ResourceTypeExtensions.h
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/flatten/ResourceTypeExtensions.h
#

from ctypes import *

from Tools.aapt.ResourcesTypes import ResChunk_header, ResStringPool_ref, ResTable_entry, ResTable_ref, ResTable_config

# 
#    New android::ResChunk_header types defined
#    for AAPT to use.
#   
#    TODO(adamlesinski): Consider reserving these
#    enums in androidfw/ResourceTypes.h to avoid
#    future collisions.
#

RES_FILE_EXPORT_TYPE = 0x000c

RES_TABLE_PUBLIC_TYPE = 0x000d
# 
#    A chunk that holds the string pool
#    for source entries (path/to/source:line).
# 
RES_TABLE_SOURCE_POOL_TYPE = 0x000e
# 
#    A chunk holding names of externally
#    defined symbols and offsets to where
#    they are referenced in the table.
# 
RES_TABLE_SYMBOL_TABLE_TYPE = 0x000f

# 
#    New resource types that are meant to only be used
#    by AAPT and will not end up on the device.
#


class ExtendedTypes(object):
    # 
    #    A raw string value that hasn't had its escape sequences
    #    processed nor whitespace removed.
    # 
    TYPE_RAW_STRING = 0xfe

class FileExport_header(Structure):
    #  Followed by exportedSymbolCount ExportedSymbol structs, followed by the string pool.
    _fields_ = [
        ('header', ResChunk_header),
        #  MAGIC value. Must be 'AAPT' (0x41415054)
        ('magic', 4*c_char),
        # Version of AAPT that built this file.
        ('version', c_uint32),
        # The resource name.
        ('name', ResStringPool_ref),
        # Configuration of this file.
        ('config', ResTable_config),
        # Original source path of this file.
        ('source', ResStringPool_ref),
        # Number of symbols exported by this file.
        ('exportedSymbolCount', c_uint32)
    ]

class ExportedSymbol(Structure):
    _fields_ = [
        ('name', ResStringPool_ref),
        ('line', c_uint32)
    ]

class Public_header(Structure):
    _fields_ = [
        ('header', ResChunk_header),
        # 
        #    The ID of the type this structure refers to.
        # 
        ('typeId', c_uint8), 
        # 
        #    Reserved. Must be 0.
        # 
        ('res0', c_uint8),
        # 
        #    Reserved. Must be 0.
        # 
        ('res1', c_uint16),
        # 
        #    Number of public entries.
        # 
        ('count', c_uint32),
    ]
    
    
class Public_entry(Structure):
    _fields_ = [
        ('entryId', c_uint16),
        ('res0', c_uint16),
        ('key', ResStringPool_ref),
        ('source', ResStringPool_ref),
        ('sourceLine', c_uint32),
    ]

# 
#    A chunk with type RES_TABLE_SYMBOL_TABLE_TYPE.
#    Following the header are count number of SymbolTable_entry
#    structures, followed by an android::ResStringPool_header.
# 

class SymbolTable_header(Structure):
    _fields_ = [
        ('header', ResChunk_header),
        # 
        #    Number of SymbolTable_entry structures following
        #    this header.
        # 
        ('count', c_uint32),
    ]


class SymbolTable_entry(Structure):
    _fields_ = [
        # 
        #    Offset from the beginning of the resource table
        #    where the symbol entry is referenced.
        # 
        ('offset', c_uint32),
        # 
        #    The index into the string pool where the name of this
        #    symbol exists.
        # 
        ('stringIndex', c_uint32),
    ]

# 
#    A structure representing the source of a resourc entry.
#    Appears after an android::ResTable_entry or android::ResTable_map_entry.
#   
#    TODO(adamlesinski): This causes some issues when runtime code checks
#    the size of an android::ResTable_entry. It assumes it is an
#    android::ResTable_map_entry if the size is bigger than an android::ResTable_entry
#    which may not be true if this structure is present.
# 

class ResTable_entry_source(Structure):
    _fields_ = [
        # 
        #    Index into the source string pool.
        # 
        ('pathIndex', c_uint32),
        # 
        #    Line number this resource was defined on.
        # 
        ('line', c_uint32),
    ]


# An alternative struct to use instead of ResTable_map_entry.
# This one is a standard_layout struct.
# definida en:
# https://github.com/aosp-mirror/platform_frameworks_base/blob/master/tools/aapt2/format/binary/ResourceTypeExtensions.h
#

class ResTable_entry_ext(Structure):
    _fields_ = [
        ('entry', ResTable_entry),
        ('parent', ResTable_ref),
        ('count', c_uint32),
    ]

    def __getattr__(self, item):
        return getattr(self.entry, item)

    def __setattr__(self, key, value):
        if hasattr(self.entry, key):
            setattr(self.entry, key, value)
        else:
            super(ResTable_entry_ext, self).__setattr__(key, value)


