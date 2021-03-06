from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
from appFactory import create_app
from models import Genre
from enums import State


class SelectMultipleGenresField(SelectMultipleField):
    def __init__(self, label='', validators=None, **kwargs):
        super(SelectMultipleGenresField, self).__init__(label, validators, **kwargs)

    def post_validate(self, form, validation_stopped):
        super(SelectMultipleGenresField, self).post_validate(form, validation_stopped)
        
        if (not validation_stopped):
            self.data = Genre.query.filter(Genre.name.in_(self.data)).all()
    def process_data(self, value):
        try:
            if not value:
                value = None
            elif isinstance(value[0], Genre):
                value = list(map(lambda genr: genr.name, value))
            self.data = value
        except (ValueError, TypeError):
            self.data = None
        super(SelectMultipleGenresField, self).process_data(value)
        
        

    


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
            choices=State.choices())
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
        genres = SelectMultipleGenresField(# implement enum restriction
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
            choices=State.choices())
        phone = StringField(# implement validation logic for state
            'phone')
        web_link = StringField('web_link', validators=[URL()])
        image_link = StringField('image_link', validators=[URL()])
        genres = SelectMultipleGenresField(# implement enum restriction
            'genres', validators=[DataRequired()],
            choices=genres_choices)
        facebook_link = StringField(# implement enum restriction
            'facebook_link', validators=[URL()])
        seeking_venue = BooleanField('seeking_venue')
        seeking_description = StringField('seeking_description')

    # IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
