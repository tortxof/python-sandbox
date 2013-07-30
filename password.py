#! /usr/bin/env python3

import sqlite3
import subprocess

# pwdatabase = '/home/tortxof/private/passwords.db'
pwdatabase = ':memory:'

def pwSearch(query):
    conn = sqlite3.connect(pwdatabase)
    result = conn.execute("select * from passwords where name like '%{}%'".format(query))
    showResult(result)

def showResult(result):
    for row in result:
        for field in row:
            print(field)
        print()

def newPassword():
    conn = sqlite3.connect(pwdatabase)
    print('Creating new password entry.')
    newrecord = ['' for i in range(5)]
    newrecord[0] = input('Title: ')
    newrecord[1] = input('URL: ')
    newrecord[2] = input('Username: ')
    newrecord[3] = subprocess.check_output(['pwgen','-cn','12','1']).decode().strip()
    newrecord[4] = input('Other: ')
    conn.execute("create table passwords ('title', 'url', 'username', 'password', 'other')")
    conn.execute('insert into passwords values (?, ?, ?, ?, ?)', newrecord)
    conn.commit()
    for i in conn.execute('select * from passwords'):
        print(i)

def getCmd():
    pass

# pwSearch(input("Search: "))
newPassword()
