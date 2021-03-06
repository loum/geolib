# pylint: disable=W0142
"""GeoLib index.

"""
import flask
import shlex

from geolib import app
import geolib.views
from geolib.forms.meta_search import MetaSearch


@app.route('/geolib/index.html', methods=['GET', 'POST'])
def index():
    """GeoLib landing page.

    """
    form = MetaSearch()
    form_status = form.validate_on_submit()

    if form_status:
        if len(form.row_id.data):
            return flask.redirect(flask.url_for('meta',
                                                row_id=form.row_id.data))
        elif form.latitude.data is not None:
            query_terms = {'q': '%s,%s' % (form.latitude.data,
                                           form.longitude.data)}
            return flask.redirect(flask.url_for('points', **query_terms))
        elif form.point_01_latitude.data is not None:
            points = []
            point_01 = '%s,%s' % (form.point_01_latitude.data,
                                  form.point_01_longitude.data)
            points.append(point_01)

            if form.point_02_latitude.data is not None:
                point_02 = '%s,%s' % (form.point_02_latitude.data,
                                      form.point_02_longitude.data)
                points.append(point_02)

            query_terms = {'q': points}

            return flask.redirect(flask.url_for('gdelt_points',
                                                **query_terms))
        else:
            title_data = form.image_title.data.encode('utf-8')
            title_data = shlex.split(title_data)

            image_rep = form.image_rep.data.encode('utf-8')
            image_rep = shlex.split(image_rep)

            image_source = form.image_source.data.encode('utf-8')
            image_source = shlex.split(image_source)

            image_comments = form.image_comments.data.encode('utf-8')
            image_comments = shlex.split(image_comments)

            terms = {'NITF_FTITLE': title_data,
                     'NITF_IREP': image_rep,
                     'NITF_ISORCE': image_source,
                     'NITF_IMAGE_COMMENTS': image_comments}

            return flask.redirect(flask.url_for('search', **terms))

    return flask.render_template('index.html',
                                 title='Metadata Key Search',
                                 form=form)
