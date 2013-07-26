import flask.ext.wtf
import wtforms
from wtforms import validators


class LoginForm(flask.ext.wtf.Form):
    username = wtforms.TextField(
        'Username',
        validators=[
            validators.DataRequired()])
