from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, HiddenField, validators
from wtforms.validators import DataRequired


class AddForm(FlaskForm):

    title = StringField(u'Movie Title')
    submit_button = SubmitField(u'Submit')


class EditForm(FlaskForm):

    rating = DecimalField(u'Your Rating out of 10 e.g. 7.5', places=1, validators=[validators.number_range(min=0.0, max=10.0)])
    review = StringField(u'Your Review')
    submit_button = SubmitField(u'Save')
