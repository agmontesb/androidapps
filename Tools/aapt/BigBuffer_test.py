# -*- coding: utf-8 -*-
import pytest
import ctypes
import struct

from Tools.aapt.BigBuffer import BigBuffer

def test_AllocateSingleBlock():
    buffer = BigBuffer(4)
    assert buffer.nextBlock(ctypes.c_char, 2) is not None
    assert buffer.size() == 2

def test_ReturnSameBlockIfNextAllocationFits():
    buffer = BigBuffer(16)
    b1 = buffer.nextBlock(ctypes.c_char, 8)
    assert b1 is not None
    assert len(buffer.mBlocks) == 1

    b2 = buffer.nextBlock(ctypes.c_char, 4)
    assert b2 is not None
    assert len(buffer.mBlocks) == 1

def test_AllocateExactSizeBlockIfLargerThanBlockSize():
    buffer = BigBuffer(16)

    assert buffer.nextBlock(ctypes.c_char, 32) is not None
    assert buffer.size() == 32

def test_AppendAndMoveBlock():
    buffer = BigBuffer(16)

    b1 = buffer.nextBlock(ctypes.c_uint32)
    assert b1 is not None
    b1.value = 33

    buffer2 = BigBuffer(16)
    b2 = buffer2.nextBlock(ctypes.c_uint32)
    assert b2 is not None
    b2.value = 44

    buffer.appendBuffer(buffer2)
    assert buffer2.size() == 0

    assert buffer.size() == 2 * ctypes.sizeof(ctypes.c_uint32)

    it = iter(buffer)
    b = it.next()
    assert b.size == ctypes.sizeof(ctypes.c_uint32)
    assert b.buffer.startswith(struct.pack('i', 33))

    b = it.next()
    assert b.size == ctypes.sizeof(ctypes.c_uint32)
    assert b.buffer.startswith(struct.pack('i', 44))

    with pytest.raises(StopIteration):
        b = it.next()

def test_PadAndAlignProperly():
    buffer = BigBuffer(16)

    assert buffer.nextBlock(ctypes.c_char, 2) is not None
    assert buffer.size() == 2
    buffer.pad(2)
    assert buffer.size() == 4
    buffer.align4()
    assert buffer.size() == 4
    buffer.pad(2)
    assert buffer.size() == 6
    buffer.align4()
    assert buffer.size() == 8
