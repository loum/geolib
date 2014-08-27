#!/usr/bin/python

import sys
sys.path.insert(1, '/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg')

from geolib import app
app.run(host='0.0.0.0', debug=True)
