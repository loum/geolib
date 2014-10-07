"""GeoLib metadata forms.

"""
from flask.ext.wtf import Form
from wtforms import (validators,
                     TextField,
                     FloatField)

from geolib.forms import RequiredIf


class MetaSearch(Form):
    row_id = TextField('row_id')
    latitude = FloatField('latitude',
                          [RequiredIf('longitude'),
                           validators.Optional(),
                           validators.NumberRange(min=-90, max=90)])
    longitude = FloatField('longitude',
                           [RequiredIf('latitude'),
                            validators.Optional(),
                            validators.NumberRange(min=-180, max=180)])
