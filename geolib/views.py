"""GeoLib views abstraction.

"""
import os
import json
import flask
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.patches
import matplotlib.pyplot as plt
import requests
import urllib
import urlparse

from geolib import app
from geolib.forms.meta_search import MetaSearch

# Import our views.
import geolib.index
import geolib.audit


@app.route('/health')
def health():
    return 'OK!'


@app.route('/geolib/meta/results?row_id=<row_id>')
def meta(row_id):
    app.logger.debug('search_row_id: %s' % row_id)
    meta_url = ('%s%s' % (app.config['META_REST_URL'], row_id))

    response = requests.get(meta_url)
    json_data = json.loads(response.text)

    return flask.render_template('meta.html', result=json_data)


@app.route('/geolib/search')
def search():
    parser = urlparse.urlparse(flask.request.url)
    query_string = parser.query

    search_url = ('%s%s' % (app.config['FREE_TEXT_URL'], query_string))
    app.logger.debug('search_url: %s' % search_url)

    response = requests.get(search_url)
    json_data = json.loads(response.text)
    app.logger.debug('json_data: %s' % json_data)

    return flask.render_template('results.html', result=json_data)


@app.route('/geolib/points')
def points():
    query_terms = {'q': flask.request.args.get('q')}
    params = urllib.urlencode(query_terms)

    points_url = ('%s%s' % (app.config['POINTS_API'], params))
    app.logger.debug('points_url: %s' % points_url)

    response = requests.get(points_url)
    json_data = json.loads(response.text)
    app.logger.debug('json_data: %s' % json_data)

    return flask.render_template('results2.html', result=json_data)


@app.route('/footprints')
def footprints():
    basem = Basemap(width=2500000,
                    height=2000000,
                    projection='lcc',
                    resolution=None,
                    lat_1=32.15,
                    lat_2=32.1,
                    lat_0=32.125,
                    lon_0=84.5)
    basem.bluemarble()

    lats = [32.8830554198, 32.9833334691, 32.9833334691, 32.8830554198]
    lons = [84.8999998642, 84.8999998642, 85.0002779135, 85.0002779135]

    x, y = basem(lons, lats)
    xy = zip(x, y)
    #poly = matplotlib.patches.Polygon(xy, facecolor='red', alpha=0.4)
    poly = matplotlib.patches.Polygon(xy, linewidth=0, facecolor='red')
    plt.gca().add_patch(poly)
    print('added patch')

    img_format = "png"
    import cStringIO
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=img_format)

    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>GeoLib</title>
</head>
  <body>
    <a href="/footprints/zoom">
        <img src="data:image/png;base64, %s"/>
    </a>
  </body>
</html>""" % sio.getvalue().encode("base64").strip()


@app.route('/footprints/zoom')
def footprints_zoom():
    basem = Basemap(width=600000,
                    height=600000,
                    projection='lcc',
                    resolution=None,
                    lat_1=32.15,
                    lat_2=32.1,
                    lat_0=32.125,
                    lon_0=84.5)
    basem.bluemarble()

    lats = [32.8830554198, 32.9833334691, 32.9833334691, 32.8830554198]
    lons = [84.8999998642, 84.8999998642, 85.0002779135, 85.0002779135]

    x, y = basem(lons, lats)
    xy = zip(x, y)
    #poly = matplotlib.patches.Polygon(xy, facecolor='red', alpha=0.4)
    poly = matplotlib.patches.Polygon(xy, linewidth=0, facecolor='red')
    plt.gca().add_patch(poly)
    print('added zoom patch')

    img_format = "png"
    import cStringIO
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=img_format)

    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>GeoLib</title>
</head>
  <body>
    <a href="http://192.168.141.37:5150/geolib/thumb/i_3001a.jpg">
        <img src="data:image/png;base64, %s"/>
    </a>
  </body>
</html>""" % sio.getvalue().encode("base64").strip()


@app.route('/get_image50x50')
def get_image50x50():
    fname = os.path.join('static', 'img', 'image50x50.png')

    return flask.send_file(fname, mimetype='image/png')


@app.route('/get_image300x300')
def get_image300x300():
    fname = os.path.join('static', 'img', 'image300x300.png')

    return flask.send_file(fname, mimetype='image/png')


@app.route('/get_image')
def get_image():
    fname = os.path.join('static', 'img', 'image.png')

    return flask.send_file(fname, mimetype='image/png')
