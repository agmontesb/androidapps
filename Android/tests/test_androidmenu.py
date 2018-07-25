# -*- coding: utf-8 -*-
import pytest
import Tkinter as tk

from Android.Activity import AndroidMenu, MenuItem


class TestAndroidMenu:
    def test_creation(self):
        root = tk.Tk()
        androidmenu = AndroidMenu(root, tearoff=0)
        assert androidmenu.size() == 0, 'test1: menu.size() no es cero luego de crear'

        androidmenu.setGroupDividerEnabled(False)
        title1, itemId1, order1, groupid1 = 'first menu', 12345, 5, 1
        menuitem1 = androidmenu.add(title1, groupId=groupid1, itemId=itemId1, order=order1)
        assert androidmenu.size() == 1, 'test2: menu.size() no es uno al agregar un item'

        menuitem = androidmenu.findItem(itemId1)
        assert menuitem1.getItemId() == menuitem.getItemId(), 'test3: Igual itemId'
        assert menuitem1.getTitle() == menuitem.getTitle(), 'test4: Igual titulo'

        title2, itemId2, order2, groupid2 = 'second menu', 12346, 2, 1
        menuitem2 = androidmenu.add(title2, groupId=groupid2, itemId=itemId2, order=order2)

        title3, itemId3, order3, groupid3 = 'third menu', 12347, 3, 2
        androidmenu.add(title3, groupId=groupid3, itemId=itemId3, order=order3)

        msize = androidmenu.size()
        assert msize == 3, 'test5: error calculo menu.size()'

        lista = map(lambda y: y.getItemId(), map(lambda x: androidmenu.getItem(x), range(msize)))
        assert lista == [itemId2, itemId3, itemId1], 'test6: Error orden insercion elementos'

        lista = map(lambda x: androidmenu.entrycget(x, 'label'), range(msize))
        assert lista == [title2, title3, title1], 'test7: Error orden insercion en tk.menu'

        androidmenu.removeItem(itemId3)
        msize = androidmenu.size()
        assert msize == 2, 'test8: error calculo menu.size()'

        lista = map(lambda y: y.getItemId(), map(lambda x: androidmenu.getItem(x), range(msize)))
        assert lista == [itemId2, itemId1], 'test9: Error orden insercion elementos'

        lista = map(lambda x: androidmenu.entrycget(x, 'label'), range(msize))
        assert lista == [title2, title1], 'test10: Error orden insercion en tk.menu'

        '''Se recupera configuracion de 3 items'''
        androidmenu.add(title3, groupId=groupid3, itemId=itemId3, order=order3)
        msize = androidmenu.size()
        assert msize == 3, 'test8: error calculo menu.size()'

        lista = map(lambda y: y.getItemId(), map(lambda x: androidmenu.getItem(x), range(msize)))
        assert lista == [itemId2, itemId3, itemId1], 'test6: Error orden insercion elementos'

        lista = map(lambda y: y.isEnabled(), map(lambda x: androidmenu.findItem(x), [itemId1, itemId2]))
        assert lista == [True, True], 'test11: Error alguno no enable'

        '''Operaciones sobre grupos'''

        androidmenu.setGroupEnabled(1, False)
        lista = map(lambda y: y.isEnabled(), map(lambda x: androidmenu.findItem(x), [itemId1, itemId2]))
        assert not all(lista), 'setGroupEnabled: Error not all disabled'

        androidmenu.setGroupEnabled(1, True)
        lista = map(lambda y: y.isEnabled(), map(lambda x: androidmenu.findItem(x), [itemId1, itemId2]))
        assert all(lista), 'setGroupEnabled: Error not all enabled'


        androidmenu.removeGroup(2)
        msize = androidmenu.size()
        lista = map(lambda y: y.getItemId(), map(lambda x: androidmenu.getItem(x), range(msize)))
        assert msize == 2, 'removeGroup: Error en size'
        assert lista == [itemId2, itemId1], 'removeGroup: Not all items in group removed'
        assert androidmenu.findItem(itemId3) is None, 'removeGroup: Find itemId de removed group'

        lista = map(lambda x: x.isCheckable(), [menuitem1, menuitem2])
        assert not all(lista), 'setGroupCheckable: Antes de setGroupCheckable no tos no checkable'
        androidmenu.setGroupCheckable(1, checkable=True, exclusive=False)
        lista = map(lambda x: x.isCheckable(), [menuitem1, menuitem2])
        assert all(lista), 'setGroupCheckable: No todos checkable'
        lista = map(lambda x: androidmenu.type(x), range(msize))
        assert lista == msize*[tk.CHECKBUTTON], 'setGroupCheckable: No todos tk.CHECKBUTTON'

        androidmenu.setGroupCheckable(1, checkable=False, exclusive=True)
        lista = map(lambda x: androidmenu.type(x), range(msize))
        assert lista == msize*[tk.RADIOBUTTON], 'setGroupCheckable: No todos tk.RADIOBUTTON'

        '''addSubMenu'''
        submenu = androidmenu.addSubMenu(title3, groupId=groupid3, itemId=itemId3, order=order3)
        assert isinstance(submenu, AndroidMenu), 'addSubMenu: No entrega un objeto tip AndroidMenu'
        menuitem3 = androidmenu.findItem(itemId3)
        assert menuitem3.hasSubMenu(), 'addSubMenu: El menuItem creado, no tiene submenu'
        assert menuitem3.getSubMenu() == submenu, 'addSubMenu: El submenu del menuitem diferente submenucreado'


class TestMenuItem:
    def test_creation(self):
        root = tk.Tk()

        androidmenu = AndroidMenu(root, tearoff=0)

        title1, itemId1, order1, groupid1 = 'first menu', 12345, 5, 1
        menuitem1 = androidmenu.add(title1, groupId=groupid1, itemId=itemId1, order=order1)
        assert isinstance(menuitem1, MenuItem), 'Creacion: No es un objeto MenuItem'

        '''AlphabeticShorcut'''
        menuitem1.setAlphabeticShorcut('Q', 'CTRL')
        assert menuitem1.getAlphabeticShorcut() == 'Q', 'AlphabeticShorcut: Error en el shorcut'
        assert menuitem1.getAlphabeticModifier() == 'CTRL', 'AlphabeticShorcut: Error en el Modifier'

        '''Various get'''
        assert menuitem1.getGroupId() == 1, 'getGroupId: No corresponde con el grupo real'
        assert menuitem1.getItemId() == itemId1, 'getItemId: No corresponde con el real'
        assert menuitem1.getOrder() == order1, 'getOrder: No corresponde con el real'

        '''is?'''
        assert not menuitem1.hasSubMenu(), 'hasSubMenu: No corresponde con el grupo real'
        assert not menuitem1.isCheckable(), 'isCheckable: No corresponde con el grupo real'
        assert menuitem1.isEnabled(), 'isEnabled: No corresponde con el grupo real'
        menuitem1.setEnable(False)
        assert not menuitem1.isEnabled(), 'setEnabled: No corresponde con el grupo real'

        '''Icon'''
        # image = Image.open(r'E:\AccionesApp\res\drawable\phone_call.png')
        # menuitem1.setIcon(image)
        # icon = menuitem1.getIcon()
        # assert image == icon, 'Icon: detIcon diferente al de setIcon'

        '''NumericShorcut'''
        menuitem1.setNumericShorcut(1, 'CTRL')
        assert menuitem1.getNumericShorcut() == 1, 'NumericShorcut: Error en el shorcut'

        '''Title'''
        assert menuitem1.getTitle() == title1, 'getTitle: title no corresponde al valor del label'
        menuitem1.setTitle(title1 + ' modified')
        assert menuitem1.getTitle() == title1 + ' modified', 'getTitle: setTitle no corresponde al del getTitle'