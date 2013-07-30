#! /usr/bin/env python3

import sqlite3
import subprocess

pwdatabase = '/home/tortxof/private/passwords.db'
# pwdatabase = ':memory:'

headers = ('Title','URL','Username','Password','Other')


def pwSearch(query):
    conn = sqlite3.connect(pwdatabase)
    result = conn.execute("select * from passwords where name like ?", ['%{}%'.format(query)])
    showResult(result)

def showResult(result):
    for row in result:
        i = 0
        for field in row:
            print(headers[i] + ': ' + field)
            i += 1
        print()

def newPassword():
    print('Creating new password entry.')
    newrecord = ['' for i in range(5)]
    newrecord[0] = input(headers[0] + ': ')
    newrecord[1] = input(headers[1] + ': ')
    newrecord[2] = input(headers[2] + ': ')
    newrecord[3] = subprocess.check_output(['pwgen','-cn','12','1']).decode().strip()
    newrecord[4] = input(headers[4] + ': ')
    print('Add this record to database?\n')
    for i in range(len(headers)):
        print(headers[i] + ': ' + newrecord[i])
    print()
    if input('?') == 'y':
        conn = sqlite3.connect(pwdatabase)
        conn.execute('insert into passwords values (?, ?, ?, ?, ?)', newrecord)
        conn.commit()
        conn.close()
    else:
        print('Aborted')

while True:
    print('(a)dd new password\n(s)earch for password\n(q)uit')
    cmd = input('?')

    if cmd == 'a':
        newPassword()
    elif cmd == 's':
        pwSearch(input('Search: '))
    else:
        break
