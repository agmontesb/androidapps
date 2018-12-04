# -*- coding: utf-8 -*-
import pytest

from Android import overload


class test(object):
    @overload
    def funcA(self):
        return 'funcA_1 {0}'.format('No arguments')

    @funcA.adddef('int', 'str')
    def funcA(self, x1, x2):
        return 'funcA_2 x1={0}, x2={1}'.format('int', 'str')

    @funcA.adddef('str', 'str', 'int')
    def funcA(self, x1, x2, x3):
        return 'funcA_3 x1={0}, x2={1}, x3={2}'.format('str', 'str', 'int')

    @overload('int', 'str')
    def funcB(self, x1, x2):
        return 'funcB_1 x1={0}, x2={1}'.format('int', 'str')

    @funcB.adddef('int', 'str', 'str')
    def funcB(self, x1, x2, x3):
        return 'funcB_2 x1={0}, x2={1}, x3={2}'.format('int', 'str', 'str')


def test_overload():
    a = test()
    assert a.funcA() == 'funcA_1 {0}'.format('No arguments')
    assert a.funcA(3, 'uno') == 'funcA_2 x1={0}, x2={1}'.format('int', 'str')
    assert a.funcA('uno', 'dos', 3) == 'funcA_3 x1={0}, x2={1}, x3={2}'.format('str', 'str', 'int')
    assert a.funcB(3, 'uno') == 'funcB_1 x1={0}, x2={1}'.format('int', 'str')
    assert a.funcB(1, 'uno', 'dos') == 'funcB_2 x1={0}, x2={1}, x3={2}'.format('int', 'str', 'str')

    with pytest.raises(TypeError) as excinfo:
        a.funcA(1,2)
    assert str(excinfo.value) == "funcA('int', 'int'), unknown function signature."

    with pytest.raises(TypeError) as excinfo:
        a.funcB()
    assert str(excinfo.value) == 'funcB(), unknown function signature.'
