#! /usr/bin/env python3

import sqlite3
import subprocess
import cherrypy
import os
import datetime

pwdatabase = '/home/tortxof/private/passwords.db'
# pwdatabase = ':memory:'

# Set key expiration time in seconds
keyExpTime = 60 * 5

html_template = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
font-size:16px;
background-color:#666;
padding:16px;
}}
.password
{{
font-family:monospace;
}}
input, textarea
{{
font-family:monospace;
font-size:16px;
border:1px solid #666;
}}
.searchform, .addform, .results, .message, .confirmdelete
{{
background-color:#ccc;
border:1px solid #333;
margin:16px;
padding:16px;
float:left;
clear:both;
}}
</style>
<title>Password Manager</title>
</head>
<body>
<div class="message"><a href="/">Home</a></div>
{content}
<div class="message"><a href="/">Home</a></div>
</body>
</html>
"""

html_searchform = """\
<div class="searchform">
Search<br />
<form name="search" action="/search" method="get">
<input type="text" name="query">
<input type="submit" value="Search">
</form>
</div>
"""

html_addform = """\
<div class="addform">
Add<br />
<form name="add" action="/add" method="post">
<table>
<tr><td>Title:</td><td><input type="text" name="title"></td></tr>
<tr><td>URL:</td><td><input type="text" name="url"></td></tr>
<tr><td>Username:</td><td><input type="text" name="username"></td></tr>
<tr><td>Other:</td><td><textarea name="other"></textarea></td></tr>
</table>
<input type="submit" value="Add">
</form>
</div>
"""

html_results = """\
<div class="results">
<table>
<tr><td>{headers[0]}:</td><td>{title}</td></tr>
<tr><td>{headers[1]}:</td><td><a target="_blank" href="{url}">{url}</a></td></tr>
<tr><td>{headers[2]}:</td><td>{username}</td></tr>
<tr><td>{headers[3]}:</td><td class="password">{password}</td></tr>
<tr><td>{headers[4]}:</td><td><pre>{other}</pre></td></tr>
</table>
<a href="/delete?rowid={rowid}">Delete</a>
</div>
"""

html_message = """\
<div class="message">{message}</div>
"""

html_confirmdelete = """\
<div class="confirmdelete">
<form name="confirmdelete" action="/delete" method="post">
<input type="hidden" name="rowid" value="{rowid}">
<input type="hidden" name="confirm" value="true">
<input type="hidden" name="key" value="{key}">
<input type="submit" value="Confirm Delete">
</form>
</div>
"""

headers = ('Title','URL','Username','Password','Other')

def newKey():
    '''Creates new key, adds it to database with timestamp, and returns it.'''
    key = ''.join(['{:02x}'.format(x) for x in os.urandom(16)])
    date = int(datetime.datetime.timestamp(datetime.datetime.now()))
    conn = sqlite3.connect(pwdatabase)
    conn.execute("insert into keys values (?, ?)", (key, date))
    conn.commit()
    conn.close()
    return key

def keyValid(key):
    '''Return True if key is in database and is not expired.'''
    if key == '':
        return False
    conn = sqlite3.connect(pwdatabase)
    dates = [i for i in conn.execute("select date from keys where key=?", (key,))]
    conn.close()
    for date in dates:
        if (date[0] + keyExpTime) > int(datetime.datetime.timestamp(datetime.datetime.now())):
            return True
    return False

def clearKeys():
    '''Removes expired keys from database.'''
    exp_date = int(datetime.datetime.timestamp(datetime.datetime.now())) - keyExpTime
    conn = sqlite3.connect(pwdatabase)
    conn.execute("delete from keys where date < ?", (exp_date,))
    conn.commit()
    conn.close()

def pwSearch(query):
    conn = sqlite3.connect(pwdatabase)
    result = showResult(conn.execute("select *,rowid from passwords where name like ?", ['%{}%'.format(query)]))
    conn.close()
    return result

def showResult(result):
    out = ''
    for row in result:
        out += html_results.format(headers=headers,title=row[0],url=row[1],username=row[2],password=row[3],other=row[4],rowid=row[5])
    return out

def mkPasswd():
    return subprocess.check_output(['pwgen','-cn','12','1']).decode().strip()

class Root(object):
    def index(self):
        return html_template.format(content=html_searchform + html_addform)
    index.exposed = True
    def search(self, query=''):
        return html_template.format(content=pwSearch(query) + html_searchform + html_addform)
    search.exposed = True
    def add(self, title, url='', username='', other=''):
        out = ''
        newrecord = ['' for i in range(5)]
        newrecord[0] = title
        newrecord[1] = url
        newrecord[2] = username
        newrecord[3] = password = mkPasswd();
        newrecord[4] = other
        out += html_results.format(headers=headers,title=title,url=url,username=username,password=password,other=other,rowid='')
        out += html_searchform + html_addform
        conn = sqlite3.connect(pwdatabase)   
        conn.execute('insert into passwords values (?, ?, ?, ?, ?)', newrecord)
        conn.commit()
        conn.close()
        return html_template.format(content=out)
    add.exposed = True
    def delete(self, rowid, confirm='', key=''):
        clearKeys()
        out = ''
        if (confirm == 'true') and keyValid(key):
            conn = sqlite3.connect(pwdatabase)
            out += html_message.format(message="Record Deleted")
            out += showResult(conn.execute("select *,rowid from passwords where rowid=?", [rowid]))
            conn.execute("delete from passwords where rowid=?", [rowid])
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect(pwdatabase)
            out += html_message.format(message="Are you sure you want to delete this record?")
            out += showResult(conn.execute("select *,rowid from passwords where rowid=?", [rowid]))
            out += html_confirmdelete.format(rowid=rowid, key=newKey())
            conn.close()
        out += html_searchform + html_addform
        return html_template.format(content=out)
    delete.exposed = True

cherrypy.quickstart(Root())
