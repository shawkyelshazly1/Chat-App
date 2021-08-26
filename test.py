import sqlite3
from sqlite3.dbapi2 import Cursor
import bcrypt
from datetime import datetime

con = sqlite3.connect('test.db')
cur = con.cursor()


cur.execute('''
    create table if not exists users (id integer primary key,firstname text, lastname text, username text, password text)
''')


def insert_user_db(firstname, lastname, username, password, cur):
    hashed_password = bcrypt.hashpw(
        password.lower().encode('utf-8'), bcrypt.gensalt())

    cur.execute('''
            INSERT INTO users (firstname, lastname, username, password) values (?,?,?,?) 
        ''', (firstname.lower().strip(), lastname.lower().strip(), username.lower().strip(), hashed_password))


insert_user_db('Shawky', 'AHmed', 'shaq', 'Shawky_Capo1', cur)


def retrieve_user_db(username, cur):
    time0 = datetime.now()
    user = cur.execute('''
            select * from users where username=?
        ''', (username.lower().strip(),))
    print(user.fetchone())
    time1 = datetime.now()
    print(str(time1-time0))


retrieve_user_db('shaqs', cur)
