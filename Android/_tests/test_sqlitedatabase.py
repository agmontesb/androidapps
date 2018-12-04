# -*- coding: utf-8 -*-
import pytest
from Android.databases.sqlite.SQLiteDatabase import SQLiteDatabase

def test_query_statement():
    db = SQLiteDatabase.create()
    sql_req = '''SELECT * FROM stocks WHERE qty<1000;'''
    sql = db._queryStatement(table='stocks', selection='qty<1000')
    assert sql == sql_req, '_queryStatement: bad selection'

    sql_req = 'SELECT column1, column2 FROM stocks ' \
              'WHERE qty<1000 GROUP BY col1,col2 ' \
              'HAVING COUNT(CustomerID) > 5 ' \
              'ORDER BY column23 LIMIT 5;'
    sql = db._queryStatement(columns=('column1', 'column2'), table='stocks',
                             selection='qty<1000', groupBy='col1,col2',
                             having='COUNT(CustomerID) > 5', orderBy='column23', limit=5)
    assert sql == sql_req, '_queryStatement: bad selection'


def test_memory_db():
    db = SQLiteDatabase.create()
    sql = '''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)'''
    db.execSQL(sql)
    keys = ('date', 'trans', 'symbol', 'qty', 'price')
    purchases = [('2006-01-05','BUY','RHAT',100,35.14),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                 ]
    contentValues = dict(zip(keys, purchases[0]))
    lstin = db.insert('stocks', None, contentValues)
    assert lstin == 1, 'insert: last index bad'
    for values in purchases[1:]:
        contentValues = dict(zip(keys, values))
        lstin = db.insert('stocks', None, contentValues)
    assert lstin == 4, 'insert: last index bad'

    '''SELECT * FROM stocks WHERE symbol=?'''
    cursor = db.query(table='stocks', selection='symbol=?', selectionArgs=('RHAT',))
    assert len(cursor.fetchall()) == 1, 'QUERY: bad cursor rowcount'

    '''SELECT * FROM stocks WHERE qty<1000'''
    cursor = db.query(table='stocks', selection='qty<1000')
    fetchall = cursor.fetchall()
    assert len(fetchall) == 2, 'QUERY: bad cursor rowcount'
    assert all(map(lambda x: fetchall[x] == purchases[x], [0, -1])), 'QUERY, bad content'

    '''DELETE FROM stocks WHERE qty<1000'''
    nrows = db.delete('stocks', whereClause='qty<1000')
    assert nrows == 2, 'DELETE: bad DELETE cursor rowcount'

def test_northwind_database():
    path = '/home/amontesb/Downloads/Northwind_small.sqlite'
    db = SQLiteDatabase.openDatabase(path)
    '''SELECT ContactName, City FROM Customer;'''
    db.query(table='Customer', columns=('ContactName', 'City'))

def test_SQLiteCursor():
    db = SQLiteDatabase.create()
    sql = '''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)'''
    db.execSQL(sql)
    keys = ('date', 'trans', 'symbol', 'qty', 'price')
    purchases = [('2006-01-05','BUY','RHAT',100,35.14),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                 ]
    for values in purchases:
        contentValues = dict(zip(keys, values))
        lstin = db.insert('stocks', None, contentValues)

    cursor = db.query(table='stocks')
    assert cursor.getColumnCount() == 5, 'SQLiteCursor.getColumnCount: Ban column count'

    col_names = ['date', 'trans', 'symbol', 'qty', 'price']
    assert cursor.getColumnNames() == col_names, 'SQLiteCursor.getColumnNames: Bad column names'

    mpfunc = lambda x: cursor.getColumnIndex(x[1]) == x[0]
    assert all(map(mpfunc, enumerate(col_names))), 'SQLiteCursor.getColumnIndex: Bad colIndex'
    with pytest.raises(ValueError) as excinfo:
        cursor.getColumnIndexOrThrow('dummy')
    assert 'IllegalArgumentException' in str(excinfo.value)
    assert cursor.getColumnIndex('dummy') == -1, 'SQLiteCursor.getColumnIndex: response != -1'

    cursor.close()