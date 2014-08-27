"""GeoLib metadata forms.

"""
from flask.ext.wtf import Form
from wtforms import TextField, validators


class MetaSearch(Form):
    row_id = TextField('row_id', [validators.Required()])
