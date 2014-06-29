#! /usr/bin/env python3

import cherrypy
import os

urls = {'red': 'http://reddit.com/',
        'dj':  'http://djones.co/'}

html_addform = '''\
<div class="addform">
<form name="add" action="/add" method="post">
<table>
<tr><td>URL:</td><td><input type="text" name="url"></td></tr>
<tr><td>Key (optional):</td><td><input type="text" name="key"></td></tr>
</table>
<input type="submit" value="Add">
</form>
</div>
'''

class Root(object):
    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['key'] = vpath.pop()
            return self
        return vpath

    def index(self, key=''):
        if key in urls:
            raise cherrypy.HTTPRedirect(urls[key])
        else:
            return html_addform
    index.exposed = True

    def add(self, url, key=''):
        if key == '':
            while key == '' or key in urls:
                key = ''.join(['{:02x}'.format(x) for x in os.urandom(3)])
        if key in urls:
            return 'Key already in use.'
        urls[key] = url
        return key  + ' = ' + url
    add.exposed = True

    def list(self):
        out = ''
        for i in urls:
            out += i + ' = ' + urls[i] + '<br />'
        return out
    list.exposed = True

cherrypy.quickstart(Root())
