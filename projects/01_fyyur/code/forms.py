from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
from appFactory import create_app
from models import Genre

app = create_app()
with app.app_context():
    
    class ShowForm(Form):
        artist_id = StringField('artist_id')
        venue_id = StringField('venue_id')
        start_time = DateTimeField('start_time',
            validators=[DataRequired()],
            default= datetime.today())

    class VenueForm(Form):
        name = StringField('name', validators=[DataRequired()])
        city = StringField('city', validators=[DataRequired()])
        state = SelectField('state', validators=[DataRequired()],
            choices=[('AL', 'AL'),
                ('AK', 'AK'),
                ('AZ', 'AZ'),
                ('AR', 'AR'),
                ('CA', 'CA'),
                ('CO', 'CO'),
                ('CT', 'CT'),
                ('DE', 'DE'),
                ('DC', 'DC'),
                ('FL', 'FL'),
                ('GA', 'GA'),
                ('HI', 'HI'),
                ('ID', 'ID'),
                ('IL', 'IL'),
                ('IN', 'IN'),
                ('IA', 'IA'),
                ('KS', 'KS'),
                ('KY', 'KY'),
                ('LA', 'LA'),
                ('ME', 'ME'),
                ('MT', 'MT'),
                ('NE', 'NE'),
                ('NV', 'NV'),
                ('NH', 'NH'),
                ('NJ', 'NJ'),
                ('NM', 'NM'),
                ('NY', 'NY'),
                ('NC', 'NC'),
                ('ND', 'ND'),
                ('OH', 'OH'),
                ('OK', 'OK'),
                ('OR', 'OR'),
                ('MD', 'MD'),
                ('MA', 'MA'),
                ('MI', 'MI'),
                ('MN', 'MN'),
                ('MS', 'MS'),
                ('MO', 'MO'),
                ('PA', 'PA'),
                ('RI', 'RI'),
                ('SC', 'SC'),
                ('SD', 'SD'),
                ('TN', 'TN'),
                ('TX', 'TX'),
                ('UT', 'UT'),
                ('VT', 'VT'),
                ('VA', 'VA'),
                ('WA', 'WA'),
                ('WV', 'WV'),
                ('WI', 'WI'),
                ('WY', 'WY'),])
        try:
            genres_choices = [(genre.name, genre.name) for genre in Genre.query.all()]
        except:
            genres_choices = []
        address = StringField('address', validators=[DataRequired()])
        phone = StringField('phone')
        seeking_talent = BooleanField('seeking_talent')
        seeking_description = StringField('seeking_description')
        web_link = StringField('web_link', validators=[URL()])
        image_link = StringField('image_link', validators=[URL()])
        genres = SelectMultipleField(# implement enum restriction
            'genres', validators=[DataRequired()],
            choices=genres_choices)
        facebook_link = StringField('facebook_link', validators=[URL()])

    class ArtistForm(Form):
        name = StringField('name', validators=[DataRequired()])
        city = StringField('city', validators=[DataRequired()])
        try:
            genres_choices = [(genre.name, genre.name) for genre in Genre.query.all()]
        except:
            genres_choices = []
        state = SelectField('state', validators=[DataRequired()],
            choices=[('AL', 'AL'),
                ('AK', 'AK'),
                ('AZ', 'AZ'),
                ('AR', 'AR'),
                ('CA', 'CA'),
                ('CO', 'CO'),
                ('CT', 'CT'),
                ('DE', 'DE'),
                ('DC', 'DC'),
                ('FL', 'FL'),
                ('GA', 'GA'),
                ('HI', 'HI'),
                ('ID', 'ID'),
                ('IL', 'IL'),
                ('IN', 'IN'),
                ('IA', 'IA'),
                ('KS', 'KS'),
                ('KY', 'KY'),
                ('LA', 'LA'),
                ('ME', 'ME'),
                ('MT', 'MT'),
                ('NE', 'NE'),
                ('NV', 'NV'),
                ('NH', 'NH'),
                ('NJ', 'NJ'),
                ('NM', 'NM'),
                ('NY', 'NY'),
                ('NC', 'NC'),
                ('ND', 'ND'),
                ('OH', 'OH'),
                ('OK', 'OK'),
                ('OR', 'OR'),
                ('MD', 'MD'),
                ('MA', 'MA'),
                ('MI', 'MI'),
                ('MN', 'MN'),
                ('MS', 'MS'),
                ('MO', 'MO'),
                ('PA', 'PA'),
                ('RI', 'RI'),
                ('SC', 'SC'),
                ('SD', 'SD'),
                ('TN', 'TN'),
                ('TX', 'TX'),
                ('UT', 'UT'),
                ('VT', 'VT'),
                ('VA', 'VA'),
                ('WA', 'WA'),
                ('WV', 'WV'),
                ('WI', 'WI'),
                ('WY', 'WY'),])
        phone = StringField(# implement validation logic for state
            'phone')
        image_link = StringField('image_link')
        genres = SelectMultipleField(# implement enum restriction
            'genres', validators=[DataRequired()],
            choices=genres_choices)
        facebook_link = StringField(# implement enum restriction
            'facebook_link', validators=[URL()])

    # IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
