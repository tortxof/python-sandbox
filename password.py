#! /usr/bin/env python3

import sqlite3
import subprocess
import cherrypy

pwdatabase = '/home/tortxof/private/passwords.db'
# pwdatabase = ':memory:'

html_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Password Manager</title>
</head>
<body>
{content}
</body>
</html>
"""

html_searchform = """
<form name="search" action="/search" method="post">
<input type="text" name="query">
<input type="submit" value="Search">
</form>
"""

html_addform = """
<form name="add" action="/add" method="post">
<input type="text" name="title">
<input type="text" name="url">
<input type="text" name="username">
<input type="text" name="other">
<input type="submit" value="Add">
</form>
"""

html_results = """
<table>
<tr><td>{headers[0]}</td><td>{title}</td></tr>
<tr><td>{headers[1]}</td><td><a href="{url}">{url}</a></td></tr>
<tr><td>{headers[2]}</td><td>{username}</td></tr>
<tr><td>{headers[3]}</td><td>{password}</td></tr>
<tr><td>{headers[4]}</td><td>{other}</td></tr>
</table>
"""

prompt = '> '
headers = ('Title','URL','Username','Password','Other')


def pwSearch(query):
    conn = sqlite3.connect(pwdatabase)
    result = showResult(conn.execute("select * from passwords where name like ?", ['%{}%'.format(query)]))
    conn.close()
    return result

def showResult(result):
    out = ''
    for row in result:
        out += html_results.format(headers=headers,title=row[0],url=row[1],username=row[2],password=row[3],other=row[4])
    return out

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
    if input(prompt) == 'y':
        conn = sqlite3.connect(pwdatabase)
        conn.execute('insert into passwords values (?, ?, ?, ?, ?)', newrecord)
        conn.commit()
        conn.close()
    else:
        print('Aborted')



class Root(object):
    def index(self):
        return html_template.format(content=html_searchform)
    index.exposed = True
    def search(self, query):
        return html_template.format(content=pwSearch(query) + html_searchform)
    search.exposed = True

cherrypy.quickstart(Root())


'''
while True:
    print('(a)dd new password\n(s)earch for password\n(q)uit')
    cmd = input(prompt)

    if cmd == 'a':
        newPassword()
    elif cmd == 's':
        pwSearch(input('Search: '))
    else:
        break
'''
