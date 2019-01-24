# -*- coding: utf-8 -*-
import pytest
from functools import wraps

from Android import overload

def myDecorator(func):
    """
    Solo decorators que conserven los inspect.argspec se pueden usar
    con overload. Ver documentacion de libreria wraps
    :param func:
    :return:  decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print func.__name__, args, kwargs
        return func(*args, **kwargs)
    return wrapper

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

    @overload('@int', 'str')
    def funcB(self, x1, x2):
        return 'funcB_1 x1={0}, x2={1}'.format('int', 'str')

    @funcB.adddef('int', 'str', 'str')
    def funcB(self, x1, x2, x3):
        return 'funcB_2 x1={0}, x2={1}, x3={2}'.format('int', 'str', 'str')

class TestClassMethod(object):
    @overload('int', 'str')
    def funcA(cls, x1, x2):
        return 'funcA_2 x1={0}, x2={1}'.format('int', 'str')

    @funcA.adddef()
    def funcA(cls):
        return 'funcA_1 {0}'.format('No arguments')

    funcA = classmethod(funcA)

    @overload('int', 'str')
    @classmethod
    def funcAbis(cls, x1, x2):
        return 'funcAbis_2 x1={0}, x2={1}'.format('int', 'str')

    @funcAbis.adddef()
    @classmethod
    def funcAbis(cls):
        return 'funcAbis_1 {0}'.format('No arguments')

    @overload('@int', 'str')
    @staticmethod
    def funcB(x1, x2):
        return 'funcB_1 x1={0}, x2={1}'.format('int', 'str')

    @funcB.adddef('int', 'str', 'str')
    @staticmethod
    def funcB(x1, x2, x3):
        return 'funcB_2 x1={0}, x2={1}, x3={2}'.format('int', 'str', 'str')

    @overload('@int', 'str')
    def funcBbis(self, x1, x2):
        return 'funcBbis_1 x1={0}, x2={1}'.format('int', 'str')

    @funcBbis.adddef('int', 'str', 'str')
    def funcBbis(self, x1, x2, x3):
        return 'funcBbis_2 x1={0}, x2={1}, x3={2}'.format('int', 'str', 'str')

    funcBbis = staticmethod(funcBbis)

    @overload('@int', 'str')
    def funcC(self, x1, x2):
        return 'funcC_1 x1={0}, x2={1}'.format('int', 'str')

    @funcC.adddef('int', 'str', 'str')
    def funcC(self, x1, x2, x3):
        return 'funcC_2 x1={0}, x2={1}, x3={2}'.format('int', 'str', 'str')

    # funcC = myDecorator(funcC)


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

    '''
    Using nullable variables
    '''
    assert a.funcB(None, 'uno') == 'funcB_1 x1={0}, x2={1}'.format('int', 'str')

    with pytest.raises(TypeError) as excinfo:
        a.funcB(3, None)
    assert str(excinfo.value) == "funcB('int', 'NoneType'), unknown function signature."

def test_overload_class_static_method():
    assert TestClassMethod.funcA() == 'funcA_1 No arguments', 'classmethod: error'
    assert TestClassMethod.funcAbis() == 'funcAbis_1 No arguments', 'classmethod: error'
    assert TestClassMethod.funcB(1, 'dos') == 'funcB_1 x1=int, x2=str', 'staticmehod: error'
    assert TestClassMethod.funcBbis(1, 'dos') == 'funcBbis_1 x1=int, x2=str', 'staticmehod: error'
    with pytest.raises(TypeError) as excinfo:
        TestClassMethod.funcC(1, 'dos')
    assert str(excinfo.value) == "unbound method funcC() must be called with TestClassMethod instance as first argument (got int instance instead)"
    pass
