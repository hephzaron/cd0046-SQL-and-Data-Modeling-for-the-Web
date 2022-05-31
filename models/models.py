from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

# Association table between Artist and Venue
class Show(db.Model):
    __tablename__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    
    venue = db.relationship('Venue', back_populates = 'artists')
    artist = db.relationship('Artist', back_populates = 'venues')
    
    def __repr__(self):
        return f'<Show {self.id} {self.start_time}>'
    
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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.state}>'
    

class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(500))
    released_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Album relationship with Song
    songs = db.relationship('Song', backref='album')
    
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
    
    def __repr__(self):
        return f'<Song {self.id} {self.name} {self.composer}>'
    
class TimeAvailability(db.Model):
    __tablename__ = 'time_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    available_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)