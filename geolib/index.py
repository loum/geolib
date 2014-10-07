"""GeoLib index.

"""
import flask

from geolib import app
from geolib.forms.meta_search import MetaSearch


@app.route('/geolib/index.html', methods=['GET', 'POST'])
def index():
    form = MetaSearch()
    form_status = form.validate_on_submit()

    if form_status:
        app.logger.debug('float: %s' % str(form.latitude.data))
        if len(form.row_id.data):
            return flask.redirect(flask.url_for('meta',
                                                row_id=form.row_id.data))
        elif form.latitude.data is not None:
            query_terms = {'q': '%s,%s' % (form.latitude.data,
                                           form.longitude.data)}
            return flask.redirect(flask.url_for('points', **query_terms))

    return flask.render_template('index.html',
                                 title='Metadata Key Search',
                                 form=form)
