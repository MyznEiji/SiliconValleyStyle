import sqlite3
import time

import memcache

db = memcache.Client(['127.0.0.1:11211'])
db.set('web_page', 'value1', time=3)
time.sleep(1)
print(db.get('web_page'))

db.set('counter', 0)
db.incr('counter', 1)
db.incr('counter', 1)
db.incr('counter', 1)
print(db.get('counter'))

conn = sqlite3.connect('test_sqlite3.db')
curs = conn.cursor()
curs.execute(
    'CREATE TABLE persons('
    'empty_id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')

curs.execute('INSERT INTO persons(name) values("Mike")')
conn.commit()
# conn.close()

def get_employ_id(name):
    """
    社員の名前を元に社員のIDを取得する
    """

    employ_id = db.get(name)
    if employ_id:
        return employ_id
    curs.execute(
        'SELECT * FROM persons WHERE name = "{}"'.format(name)
    )

    person = curs.fetchone()
    if not person:
        raise Exception('No employ')

    employ_id, name= person
    db.set(name, employ_id, time=60)
    return employ_id

print(get_employ_id("Mike"))
