from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

class SearchForm(FlaskForm):
    query = StringField(_l('検索'), validators=[DataRequired()])
    submit = SubmitField(_l('検索'))

# app/admin/__init__.py - Admin blueprint
from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import routes
