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
        return flask.redirect(flask.url_for('meta',
                                            row_id=form.row_id.data))

    return flask.render_template('index.html',
                                 title='Metadata Key Search',
                                 form=form)
