## Run this file to send first set of data into the database

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Venue, Artist, Show
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

venue1=Venue(
    name="The Musical Hop",
    address="1015 Folsom Street",
    city="San Francisco",
    state="CA",
    phone="123-123-1234",
    website_link="https://www.themusicalhop.com",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    seeking_talent=True,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
)

venue2= Venue(
    name="The Dueling Pianos Bar",
    address="335 Delancey Street",
    city="New York",
    state="NY",
    phone="914-003-1132",
    website_link="https://www.theduelingpianos.com",
    facebook_link="https://www.facebook.com/theduelingpianos",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
)

venue3=Venue(
    name="Park Square Live Music & Coffee",
    address="34 Whiskey Moore Ave",
    city="San Francisco",
    state="CA",
    phone="415-000-1234",
    website_link="https://www.parksquarelivemusicandcoffee.com",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
)
    
artist1 = Artist(
    name = "Guns N Petals",
    city = "San Francisco",
    state = "CA",
    phone = 0000000000,
    genres = "Jazz",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
)

artist2 = Artist(
    name = "Matt Quevedo",
    city = "San Francisco",
    state = "CA",
    phone = 0000000000,
    genres = "Rock n Roll",
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
)

artist3 = Artist(
    name = "The Wild Sax Band",
    city = "San Francisco",
    state = "CA",
    phone = 0000000000,
    genres = "Rock n Roll",
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
)

show1 = Show(start_time="2019-05-21T21:30:00.000Z")
show2 = Show(start_time="2019-06-15T23:00:00.000Z")
show3 = Show(start_time="2035-04-01T20:00:00.000Z")
show4 = Show(start_time="2035-04-08T20:00:00.000Z")
show5 = Show(start_time="2035-04-15T20:00:00.000Z")

try:
    show1.artist = artist1
    show2.artist = artist2
    show3.artist = artist3
    show4.artist = artist3
    show5.artist = artist3
    venue1.artists.append(show1)
    venue3.artists.append(show2)
    venue3.artists.append(show3)
    venue3.artists.append(show3)
    venue3.artists.append(show3)
    db.session.add_all([venue1, venue2, venue3])
    print('I am here before commit')

    db.session.commit()
    print('I am here after commit')
except:
    print(sys.exc_info())
    db.session.rollback()
    print('failed')
finally:
    db.session.close()
    



  
        
