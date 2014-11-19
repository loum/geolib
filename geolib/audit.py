# pylint: disable=W0142
"""GeoLib index.

"""
import flask
import requests
import json
import urlparse

from geolib import app


@app.route('/geolib/audit', methods=['GET', 'POST'])
def audit():
    """GeoLib audit page.

    """
    parser = urlparse.urlparse(flask.request.url)
    query_string = parser.query

    search_url = ('%s?%s' % (app.config['AUDIT_URL'], query_string))
    app.logger.debug('search_url: %s' % search_url)

    response = requests.get(search_url)
    json_data = json.loads(response.text)
    app.logger.debug('json_data: %s' % json_data)

    return flask.render_template('audit.html', result=json_data)
