from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
from re import fullmatch
import dateutil.parser

db = SQLAlchemy()

# Association table between Artist and Venue
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())   
    
    # Venue relationship with Artist
    artists = db.relationship('Show', back_populates='venue')
    
    @validates('name')
    def validate_venue_name(self, _, venue_name):
        if venue_name is None or venue_name =="":
            raise AssertionError(
                'The venue name field is required'
                )
        if Venue.query.filter(Venue.name == venue_name).first():
            raise AssertionError(
                'Venue: {} already exist'.format(venue_name)
            )
        return venue_name
    
    @validates('city')
    def validate_venue_city(self, _, venue_city):
        if venue_city is None or venue_city =="":
            raise AssertionError(
                'The city name field is required'
                )
        if not (fullmatch('^(\w\s?)+$', venue_city)):
            raise AssertionError(
                'City name can contain alphanumeric characters only'
                )
        return venue_city
    
    @validates('state')
    def validate_venue_state(self, _, venue_state):
        if venue_state is None or venue_state =="":
            raise AssertionError(
                'The state name field is required'
                )
        if not (fullmatch('^[A-Z]{2}$', venue_state)):
            raise AssertionError(
                'The name of state should be all capital letter and 2 letters'
                )
        return venue_state
    
    @validates('address')
    def validate_venue_address(self, _, venue_address):
        if venue_address is None or venue_address =="":
            raise AssertionError(
                'Address field is required'
                )
        if not (fullmatch('^(\w\s?)+$', venue_address)):
            raise AssertionError(
                'The address can be alphanumeric charcters only'
                )
        return venue_address
    
    @validates('phone')
    def validate_venue_phone(self, _, venue_phone):
        if venue_phone is None or venue_phone =="":
            raise AssertionError(
                'Phone number is required'
                )
        if not (fullmatch('^\d{10}$', venue_phone)):
            raise AssertionError(
                'Phone should be exactly ten digit in mumber'
                )
        return venue_phone
    
    @validates('image_link')
    def validate_venue_image_link(self, _, venue_image_link):
        if venue_image_link is None or venue_image_link =="":
            raise AssertionError(
                "Enter the URL of your venue's image"
                )
        return venue_image_link
    
    @validates('facebook_link')
    def validate_venue_facebook_link(self, _, venue_facebook_link):
        if not (fullmatch(
            '^(?:https:\/\/)?(?:web\.)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)$',
            venue_facebook_link)):
            raise AssertionError(
                'URL must be a facebook link'
                )
        return venue_facebook_link
    
    @validates('website_link')
    def validate_venue_website_link(self, _, venue_website_link):
        if not (fullmatch('^(?:http:\/\/)?(?:https:\/\/)?(?:web\.)?(?:www\.)?\w+\\.\w*', venue_website_link)):
            raise AssertionError(
                'A valid URL must be entered'
                )
        return venue_website_link
    
    @validates('seeking_description')
    def validate_venue_seeking_description(self, _, venue_seeking_descriptiuon):
        if len(venue_seeking_descriptiuon) >= 250:
            raise AssertionError(
                'venue description should not exceed 250 characters'
            )
        return venue_seeking_descriptiuon

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.state}>'   
    
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Artist relationship with Venue
    venues = db.relationship('Show', back_populates = 'artist')
    # Artist relationship with Album
    albums = db.relationship('Album', backref='artist')
    # Artist relationship with time_availability
    time_availabilities = db.relationship('TimeAvailability', backref='time_availability')
    
    @validates('name')
    def validate_artist_name(self, _, artist_name):
        if artist_name is None or artist_name =="":
            raise AssertionError(
                'The artist name field is required'
                )
        if Artist.query.filter(Artist.name == artist_name).first():
            raise AssertionError(
                'Artist: {} already exist'.format(artist_name)
            )
        return artist_name
    
    @validates('city')
    def validate_artist_city(self, _, artist_city):
        if artist_city is None or artist_city =="":
            raise AssertionError(
                'The city name field is required'
                )
        if not (fullmatch('^(\w\s?)+$', artist_city)):
            raise AssertionError(
                'City name can contain alphanumeric characters only'
                )
        return artist_city
    
    @validates('state')
    def validate_artist_state(self, _, artist_state):
        if artist_state is None or artist_state =="":
            raise AssertionError(
                'The state name field is required'
                )
        if not (fullmatch('^[A-Z]{2}$', artist_state)):
            raise AssertionError(
                'The name of state should be all capital letter and 2 letters'
                )
        return artist_state
        
    @validates('phone')
    def validate_artist_phone(self, _, artist_phone):
        if artist_phone is None or artist_phone =="":
            raise AssertionError(
                'Phone number is required'
                )
        if not (fullmatch('^\d{10}$', artist_phone)):
            raise AssertionError(
                'Phone should be exactly ten digit in mumber'
                )
        return artist_phone
    
    @validates('image_link')
    def validate_artist_image_link(self, _,artist_image_link):
        if artist_image_link is None or artist_image_link =="":
            raise AssertionError(
                "Enter the URL of your artist's image"
                )
        return artist_image_link
    
    @validates('facebook_link')
    def validate_artist_facebook_link(self, _, artist_facebook_link):
        if not (fullmatch(
            '^(?:https:\/\/)?(?:web\.)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)$',
            artist_facebook_link)):
            raise AssertionError(
                'URL must be a facebook link'
                )
        return artist_facebook_link
    
    @validates('website_link')
    def validate_artist_website_link(self, _, artist_website_link):
        if not (fullmatch('^(?:http:\/\/)?(?:https:\/\/)?(?:web\.)?(?:www\.)?\w+\\.\w*', artist_website_link)):
            raise AssertionError(
                'A valid URL must be entered'
                )
        return artist_website_link
    
    @validates('seeking_description')
    def validate_artist_seeking_description(self, _, artist_seeking_descriptiuon):
        if len(artist_seeking_descriptiuon) >= 250:
            raise AssertionError(
                'artist description should not exceed 250 characters'
            )
        return artist_seeking_descriptiuon

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.state}>'
    

class Show(db.Model):
    __tablename__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    
    venue = db.relationship('Venue', back_populates = 'artists')
    artist = db.relationship('Artist', back_populates = 'venues')
    
    @validates('artist_id')
    def validate_show_artist_id(self, _, show_artist_id):
        if show_artist_id is None or show_artist_id =="":
            raise AssertionError(
                'The artist id field is required'
                )
        if not Artist.query.filter(Artist.id == show_artist_id).first():
            raise AssertionError(
                'Artist with ID: {} does not exist'.format(show_artist_id)
            )
        if not (show_artist_id > 0):
            raise AssertionError(
                'Artist ID must be a positive number, you entered ID: {}'.format(show_artist_id)
            )
        return show_artist_id
    
    @validates('venue_id')
    def validate_show_venue_id(self, _, show_venue_id):
        if show_venue_id is None or show_venue_id =="":
            raise AssertionError(
                'The venue id field is required'
                )
        if not Venue.query.filter(Venue.id == show_venue_id).first():
            raise AssertionError(
                'Venue with ID: {} does not exist'.format(show_venue_id)
            )
        if not (show_venue_id > 0):
            raise AssertionError(
                'Venue ID must be a positive number, you entered ID: {}'.format(show_venue_id)
            )
        return show_venue_id
    
    @validates('start_time')
    def validate_show_start_time(self, _, show_start_time):
                
        if show_start_time is None or show_start_time =="":
            raise AssertionError(
                'The show start time field is required'
                )
        if not (show_start_time >= datetime.utcnow()):
            raise AssertionError(
                'Show can only be booked not earlier than today'
            )
        return show_start_time
        
    
    def __repr__(self):
        return f'<Show {self.id} {self.start_time}>'
    
class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(500))
    released_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Album relationship with Song
    songs = db.relationship('Song', backref='album')
    
    @validates('artist_id')
    def validate_album_artist_id(self, _, album_artist_id):
        if album_artist_id is None or album_artist_id =="":
            raise AssertionError(
                'The artist id field is required'
                )
        if not (album_artist_id > 0):
            raise AssertionError(
                'Artist ID must be a positive number, you entered ID: {}'.format(album_artist_id)
            )
        if not Artist.query.filter(Artist.id == album_artist_id).first():
            raise AssertionError(
                'Artist with ID: {} does not exist'.format(album_artist_id)
            )
        return album_artist_id
    
    @validates('title')
    def validate_album_title(self, _, album_title):
        if album_title is None or album_title =="":
            raise AssertionError(
                'The album title field is required'
                )
        return album_title
    
    @validates('image_link')
    def validate_album_image_link(self, _,album_image_link):
        if album_image_link is None or album_image_link =="":
            raise AssertionError(
                "Enter the URL of your album's image"
                )
        return album_image_link
    
    def __repr__(self):
        return f'<Album {self.id} {self.title}>'


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    composer = db.Column(db.String(), nullable=False)
    
    @validates('album_id')
    def validate_song_album_id(self, _, song_album_id):
        if song_album_id is None or song_album_id =="":
            raise AssertionError(
                'The album id field is required'
                )
        if not (song_album_id > 0):
            raise AssertionError(
                'Album ID must be a positive number, you entered ID: {}'.format(song_album_id)
            )
        if not Album.query.filter(Album.id == song_album_id).first():
            raise AssertionError(
                'Album with ID: {} does not exist'.format(song_album_id)
            )
        return song_album_id
    
    @validates('name')
    def validate_song_name(self, _, song_name):
        if song_name is None or song_name =="":
            raise AssertionError(
                'The song name field is required'
                )
        return song_name
    
    @validates('genre')
    def validate_song_genre(self, _, song_genre):
        if song_genre is None or song_genre =="":
            raise AssertionError(
                'The genre name field is required'
                )
        return song_genre
    
    @validates('duration_seconds')
    def validate_song_duration_seconds(self, _, song_duration_seconds):
        if song_duration_seconds is None or song_duration_seconds =="":
            raise AssertionError(
                'The song duration in seconds is required'
                )
        if not (song_duration_seconds > 0):
            raise AssertionError(
                'Song duration must be a positive number, you entered : {}'.format(song_duration_seconds)
            )
        return song_duration_seconds
    
    @validates('composer')
    def validate_song_composer(self, _, song_composer):
        if song_composer is None or song_composer =="":
            raise AssertionError(
                'The song composer name field is required'
                )
        return song_composer
    
    def __repr__(self):
        return f'<Song {self.id} {self.name} {self.composer}>'
    
class TimeAvailability(db.Model):
    __tablename__ = 'time_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    available_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    @validates('artist_id')
    def validate_available_artist_id(self, _, available_artist_id):
        if available_artist_id is None or available_artist_id =="":
            raise AssertionError(
                'The artist id field is required'
                )
        if not Artist.query.filter(Artist.id == available_artist_id).first():
            raise AssertionError(
                'Artist with ID: {} does not exist'.format(available_artist_id)
            )
        if not (available_artist_id > 0):
            raise AssertionError(
                'Artist ID must be a positive number, you entered ID: {}'.format(available_artist_id)
            )
        return available_artist_id
    
    def __repr__(self):
        return f'<TimeAvailability {self.id} {self.artist_id} {self.available_date}>'