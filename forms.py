from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, InputRequired, URL, Regexp, Length

## Declare choices for states and genres
genres = [
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]

states = [
            ('AL', 'AL'),
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
            ('WY', 'WY'),
        ]

class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id',
        validators=[InputRequired(message='Artist ID field is required')]
    )
    venue_id = IntegerField(
        'venue_id',
        validators=[InputRequired(message='Venue ID field is required')]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(message='Invalid entry: correct time for show is required')],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired(message='Name field of venue cannot be empty')]
    )
    city = StringField(
        'city', validators=[DataRequired(message='City field of venue cannot be empty')]
    )
    state = SelectField(
        'state', validators=[DataRequired(message='Select one or more from the list of state')],
        choices= states
    )
    address = StringField(
        'address', validators=[DataRequired(message='Address field is required')]
    )
    phone = StringField(
        'phone', validators=[
            DataRequired(message='Your phone number is required'),
            Regexp('^\d{10}$',message='Invalid entry, enter a correct 10-digit phone number')
            ]
        )
    image_link = StringField(
        'image_link', validators=[
            URL(require_tld=False, message='Invalid entry, an image URL is required')
            ]
        )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(message='Select one or more of the list of genres')], choices=genres)
    
    facebook_link = StringField(
        'facebook_link', validators=[Regexp(
            '^(?:https:\/\/)?(?:web\.)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)$',
            message='Invalid entry, enter a facebook url')]
        )
    website_link = StringField(
        'website_link', validators=[Regexp(
            '^(?:http:\/\/)?(?:https:\/\/)?(?:web\.)?(?:www\.)?\w+',
            message='Enter a valid web address'
            )]
        )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description', validators=[
            Length(min=1, max=250, message='Description should be kept at 1-250 character')
            ]
        )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired(message='Name field is required')]
    )
    city = StringField(
        'city', validators=[DataRequired(message='City field is required')]
    )
    state = SelectField(
        'state', validators=[DataRequired(message='Select from the list of states')],
        choices=states
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[
            DataRequired(message='Your phone number is required'),
            Regexp('^\d{10}$',message='Invalid entry, enter a correct 10-digit phone number')
            ])
    image_link = StringField(
        'image_link', validators=[
            URL(require_tld=False, message='Invalid entry, an image URL is required')
            ]
        )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(message='Select from the list of genres')],
        choices=genres
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[Regexp(
            '^(?:https:\/\/)?(?:web\.)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)$',
            message='Invalid entry, enter a facebook url')]
        )

    website_link = StringField(
        'website_link', validators=[Regexp(
            '^(?:http:\/\/)?(?:https:\/\/)?(?:web\.)?(?:www\.)?\w+',
            message='Enter a valid web address')]
     )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
        'seeking_description', validators=[
            Length(min=1, max=250, message='Description should be kept at 1-250 character')
            ]
        )


class TimeAvailabilityForm(Form):
    artist_id = IntegerField(
        'artist_id',
        validators=[InputRequired(message='Artist ID field is required')]
    )
    available_date = DateTimeField(
        'available_date',
        validators=[DataRequired(message='Invalid entry: correct date/time is required')],
        default= datetime.today()
    )