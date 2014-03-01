#! /usr/bin/env python3

import sqlite3
import subprocess
import os
import cherrypy
import time
import config

pwdatabase = config.dbfile
# pwdatabase = ':memory:'

cherrypy.config.update({'server.socket_host': config.host,
                        'server.socket_port': config.port,
                        })

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
.searchform, .addform, .loginform, .results, .message, .confirmdelete
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
<form name="search" action="/search" method="get">
<input type="text" name="query">
<input type="submit" value="Search">
</form>
</div>
"""

html_addform = """\
<div class="addform">
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
<input type="submit" value="Confirm Delete">
</form>
</div>
"""

html_login = """\
<div class="loginform">
<form name="login" action="/login" method="post">
<input type="password" name="password">
<input type="submit" value="Login">
</form>
</div>
"""

headers = ('Title','URL','Username','Password','Other')

def loggedIn():
    '''Checks if current auth cookie is valid.'''
    cookie = cherrypy.request.cookie
    if 'auth' in cookie.keys():
        if keyValid(cookie['auth'].value):
            return True
    return False

def genHex(length=32):
    '''Generate random hex string.'''
    return ''.join(['{:02x}'.format(x) for x in os.urandom(length)])

def nowUnixInt():
    '''Return int unix time.'''
    return int(time.time())

def newKey():
    '''Creates new key, adds it to database with timestamp, and returns it.'''
    key = genHex()
    date = nowUnixInt()
    conn = sqlite3.connect(pwdatabase)
    conn.execute("insert into keys values (?, ?)", (key, date))
    conn.commit()
    conn.close()
    return key

def keyValid(key):
    '''Return True if key is in database and is not expired. Updates timestamp if key is valid.'''
    if key == '':
        return False
    now = nowUnixInt()
    exp_date = now - keyExpTime
    conn = sqlite3.connect(pwdatabase)
    conn.execute("delete from keys where date < ?", (exp_date,))
    dates = [i[0] for i in conn.execute("select date from keys where key=?", (key,))]
    for date in dates:
        if (date + keyExpTime) > now:
            conn.execute("update keys set date=? where key=?", (now,key))
            conn.commit()
            conn.close()
            return True
    conn.commit()
    conn.close()
    return False

def pwSearch(query):
    '''Returns results of search.'''
    conn = sqlite3.connect(pwdatabase)
    result = showResult(conn.execute("select *,rowid from passwords where title like ?", ['%{}%'.format(query)]))
    conn.close()
    return result

def showResult(result):
    '''Renders given results.'''
    out = ''
    for row in result:
        out += html_results.format(headers=headers,title=row[0],url=row[1],username=row[2],password=row[3],other=row[4],rowid=row[5])
    return out

def mkPasswd():
    '''Returns generated password from pwgen command line utility.'''
    return subprocess.check_output(['pwgen','-cn','12','1']).decode().strip()

class Root(object):
    def index(self):
        out = ''
        if not loggedIn():
            out += html_login
        else:
            out += html_searchform + html_addform
        return html_template.format(content=out)
    index.exposed = True

    def login(self, password=''):
        out = ''
        conn = sqlite3.connect(pwdatabase)
        passwords = [i[0] for i in conn.execute("select * from master_pass", ())]
        conn.close()
        if password in passwords:
            cookie = cherrypy.response.cookie
            cookie['auth'] = newKey()
            out += html_message.format(message='You are now logged in.') + html_searchform + html_addform
        else:
            out += html_message.format(message='Login failed.') + html_login
        return html_template.format(content=out)
    login.exposed = True

    def search(self, query=''):
        out = ''
        if not loggedIn():
            out += html_message.format(message='You are not logged in.') + html_login
        else:
            out += pwSearch(query) + html_searchform + html_addform
        return html_template.format(content=out)
    search.exposed = True

    def add(self, title, url='', username='', other=''):
        out = ''
        if not loggedIn():
            out += html_message.format(message='You are not logged in.') + html_login
        else:
            newrecord = ['' for i in range(5)]
            newrecord[0] = title
            newrecord[1] = url
            newrecord[2] = username
            newrecord[3] = password = mkPasswd()
            newrecord[4] = other
            out += html_results.format(headers=headers,title=title,url=url,username=username,password=password,other=other,rowid='')
            out += html_searchform + html_addform
            conn = sqlite3.connect(pwdatabase)   
            conn.execute('insert into passwords values (?, ?, ?, ?, ?)', newrecord)
            conn.commit()
            conn.close()
        return html_template.format(content=out)
    add.exposed = True

    def delete(self, rowid, confirm=''):
        out = ''
        if not loggedIn():
            out += html_message.format(message='You are not logged in.') + html_login
        else:
            if confirm == 'true':
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
                out += html_confirmdelete.format(rowid=rowid)
                conn.close()
            out += html_searchform + html_addform
        return html_template.format(content=out)
    delete.exposed = True

cherrypy.quickstart(Root())
