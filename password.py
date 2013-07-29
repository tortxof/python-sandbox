#! /usr/bin/env python3

import sqlite3

pwdatabase = '/home/tortxof/private/passwords.db'

def pwSearch(query):
    conn = sqlite3.connect(pwdatabase)
    result = conn.execute("select * from passwords where name like '%{}%'".format(query))
    showResult(result)

def showResult(result):
    for row in result:
        for field in row:
            print(field)
        print()

def getCmd():
    pass

pwSearch(input("Search: "))
