"""Geo library web interface.

"""
import Image
import os
import flask
import tempfile
from shutil import copyfileobj
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.patches
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import json

app = flask.Flask(__name__)


@app.route('/health')
def health():
    return 'OK!'


@app.route('/details')
def details():
    return flask.render_template('details.html')

@app.route('/nav')
def nav():
    return flask.render_template('nav.html')

@app.route('/meta')
def meta():
    meta_url = 'http://192.168.141.37:5150/geolib/meta/v0.1/i_3001a'
    response = requests.get(meta_url)

    print('response: %s' % dir(response))

    json_data = json.loads(response.text)
    
    return flask.render_template('meta.html', result=json_data)


@app.route('/footprints')
def footprints():
    m = Basemap(width=2500000,
                height=2000000,
                projection='lcc',
                resolution=None,
                lat_1=32.15,
                lat_2=32.1,
                lat_0=32.125,
                lon_0=84.5)
    m.bluemarble()

    lats = [32.8830554198, 32.9833334691, 32.9833334691, 32.8830554198]
    lons = [84.8999998642, 84.8999998642, 85.0002779135, 85.0002779135]

    x, y = m(lons, lats)
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
    m = Basemap(width=600000,
                height=600000,
                projection='lcc',
                resolution=None,
                lat_1=32.15,
                lat_2=32.1,
                lat_0=32.125,
                lon_0=84.5)
    m.bluemarble()

    lats = [32.8830554198, 32.9833334691, 32.9833334691, 32.8830554198]
    lons = [84.8999998642, 84.8999998642, 85.0002779135, 85.0002779135]

    x, y = m(lons, lats)
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
    fname = os.path.join(os.sep,
                         'media',
                         'sf_jp2044lm-dev',
                         'image50x50.png')

    return flask.send_file(fname, mimetype='image/png')

@app.route('/get_image300x300')
def get_image300x300():
    fname = os.path.join(os.sep,
                         'media',
                         'sf_jp2044lm-dev',
                         'image300x300.png')

    return flask.send_file(fname, mimetype='image/png')

@app.route('/get_image')
def get_image():
    fname = os.path.join(os.sep,
                         'media',
                         'sf_jp2044lm-dev',
                         'image.png')

    return flask.send_file(fname, mimetype='image/png')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
