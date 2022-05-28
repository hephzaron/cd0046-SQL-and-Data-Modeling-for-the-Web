##Run this file to persist second set of data into the database after initial data that was sent
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Artist, Genre, MusicGenre
from decouple import config
import sys

app = Flask(__name__)
DATABASE_USERNAME=config('DATABASE_USERNAME')
DATABASE_PASSWORD=config('DATABASE_PASSWORD')
DATABASE_SERVER=config('DATABASE_SERVER')
DATABASE_NAME=config('DATABASE_NAME')
SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS')

app.config[
  'SQLALCHEMY_DATABASE_URI'
  ] = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

genre1 = Genre(name='Alternative'),
genre2 = Genre(name='Blues'),
genre3 = Genre(name='Classical'),
genre4 = Genre(name='Country'),
genre5 = Genre(name='Electronic'),
genre6 = Genre(name='Folk'),
genre7 = Genre(name='Funk'),
genre8 = Genre(name='Hip-Hop'),
genre9 = Genre(name='Heavy Metal'),
genre10 = Genre(name='Instrumental'),
genre11 = Genre(name='Jazz'),
genre12 = Genre(name='Musical Theatre'),
genre13 = Genre(name='Pop'),
genre14 = Genre(name='Punk'),
genre15 = Genre(name='R&B'),
genre16 = Genre(name='Reggae'),
genre17 = Genre(name='Rock n Roll'),
genre18 = Genre(name='Soul'),
genre19 = Genre(name='Other'),

musicgenre1 = MusicGenre(venue_id=18, genre_id=1)
musicgenre2 = MusicGenre(venue_id=18, genre_id=5)
musicgenre3 = MusicGenre(venue_id=18, genre_id=6)
musicgenre4 = MusicGenre(venue_id=18, genre_id=7)
musicgenre5 = MusicGenre(venue_id=18, genre_id=8)
musicgenre6 = MusicGenre(venue_id=19, genre_id=1)
musicgenre7 = MusicGenre(venue_id=19, genre_id=2)
musicgenre8 = MusicGenre(venue_id=19, genre_id=3)
musicgenre9 = MusicGenre(venue_id=20, genre_id=1)
musicgenre10 = MusicGenre(venue_id=20, genre_id=4)
musicgenre11 = MusicGenre(venue_id=20, genre_id=5)
musicgenre12 = MusicGenre(venue_id=20, genre_id=6)

try:
    db.session.add_all([ genre1, genre2, genre3, genre4, genre5, genre6, genre7, genre8,genre9, genre10, 
                        genre11, genre12, genre13, genre14, genre15, genre16, genre17, genre18, genre19])
    db.session.add_all([musicgenre1, musicgenre2, musicgenre3, musicgenre4, musicgenre5,
                        musicgenre6, musicgenre7, musicgenre8, musicgenre9, musicgenre10,
                        musicgenre11, musicgenre12])
    db.session.commit()
except:
    print(sys.exc_info())
    db.session.rollback()
    print('failed')
finally:
    db.session.close()
