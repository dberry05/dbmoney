import sqlite3, json
from datetime import datetime
from collections import defaultdict

DB = '/app/db/expenses.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def default_dict(my_list):
    d = defaultdict(list)
    for k, v in my_list:
        if k != v:
            d[k].append(v)
    return d

def get(table):
    ''' Gets all transactions from DB database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * FROM " + table + " ORDER BY date")
    my_data =  cur.fetchall()
    return [item for item in my_data] 
    
def get_categories(table):
    ''' Gets all categories from DB database and returns json string'''
    con = sqlite3.connect(DB)
    #con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select parent, child FROM " + table)
    my_data =  cur.fetchall()
    return default_dict(my_data)

def get_payees(table):
    ''' Gets all transactions from DB database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select DISTINCT payee FROM " + table)
    my_data =  cur.fetchall()
    return [item['payee'] for item in my_data]
	

def add_transaction(transaction):
    ''' Adds a row to DB database and returns json string'''
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (date, type, payee, category, notes, amount, trans_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (transaction['date'], transaction['type'], transaction['payee'], transaction['category'], transaction['notes'], transaction['amount'], transaction['trans_id']))
    conn.commit()
	
def delete_transaction(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ' + str(id))
    conn.commit()
	
def get_last_transaction(table):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT MAX(trans_id) FROM " + table)
    my_data =  c.fetchall()
    return [item for item in my_data]
	
def update_task(task):
    if task['status'] == 'closed':
        task['date_closed'] = datetime.now()
    format_sql = ', '.join(["{}='{}'".format(k,v) for k,v in task.iteritems()])
    SQL="UPDATE todo SET %s WHERE id=%s" % (format_sql, task['id'])
    con = sqlite3.connect('z:/data/site/db/home.db')
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
