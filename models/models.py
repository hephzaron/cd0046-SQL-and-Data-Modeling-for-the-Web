from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Show(db.Model):
    __tablename__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=True)
    
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
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    
    
    artists = db.relationship('Show', back_populates='venue')
    genres = db.relationship('MusicGenre', back_populates = 'venue')

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
    facebook_link = db.Column(db.String(120))
    
    venues = db.relationship('Show', back_populates = 'artist')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.state}>'
    
class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    
    venues = db.relationship('MusicGenre', back_populates='genre')
    
    def __repr__(self):
        return f'<Genre {self.id} {self.name}>'
    
class MusicGenre(db.Model):
    __tablename__ = 'musicgenre'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    
    genre = db.relationship('Genre', back_populates = 'venues')
    venue = db.relationship('Artist', back_populates = 'genres')
    
    def __repr__(self):
        return f'<MusicGenre {self.id} {self.venue_id} {self.genre_id}>'