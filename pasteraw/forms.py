import flask.ext.wtf
import wtforms
from wtforms import validators


class PasteForm(flask.ext.wtf.Form):
    content = wtforms.TextAreaField(
        'Content',
        validators=[
            validators.DataRequired()])
