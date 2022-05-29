#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template, jsonify, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, alias, func, select, case
from sqlalchemy.sql import label
from logging import Formatter, FileHandler
from werkzeug.datastructures import MultiDict
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from decouple import config
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
import sys
import logging
import json
import dateutil.parser
import babel

#----------------------------------------------------------------------------#
# Import Models.
#----------------------------------------------------------------------------#

from models.models import Venue, Artist, Show, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)

# TODO: connect to a local postgresql database

DATABASE_USERNAME=config('DATABASE_USERNAME')
DATABASE_PASSWORD=config('DATABASE_PASSWORD')
DATABASE_SERVER=config('DATABASE_SERVER')
DATABASE_NAME=config('DATABASE_NAME')
SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS')
SECRET_KEY = config('SECRET_KEY')

app.config[
  'SQLALCHEMY_DATABASE_URI'
  ] = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

migrate = Migrate(app, db)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues', methods=['GET'])
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  # Query to fetch venues and number of upcoming shows
  venues = db.session.query(
    Venue.id,
    Venue.name,
    func.count(case([
      (func.date(Show.start_time)>date.today(),1)
      ])).label('num_upcoming_shows')
    ).add_columns(Venue.city).outerjoin(Show).group_by(Venue.id, Venue.name).all()
  
  # Query to group Venues by city
  venue_groups = db.session.query(
    Venue.city,
    Venue.state
  ).group_by(Venue.city, Venue.state).all()
  
  data = []
  for group in venue_groups:
        obj={}
        obj['city'] = group.city
        obj['state'] = group.state
        obj['venues'] = [venue for venue in venues if venue.city==group.city]
        data.append(obj)
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  
  # Query to search by Venue names
  found_venues = db.session.query(
    Venue.id,
    Venue.name,
    func.count(case([(func.date(Show.start_time)>date.today(),1)])).label('num_upcoming_shows')
    ).outerjoin(Show).filter(
      Venue.name.ilike('%'+search_term+'%')
      ).group_by(Venue.id, Venue.name).order_by(Venue.name).all()
  
  num_of_found_venues = len(found_venues)
  response= { 
    "count": num_of_found_venues,
    "data": found_venues
  }
  
  return render_template(
    'pages/search_venues.html',results=response, search_term=request.form.get('search_term', '')
    )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # Get the queries of all required columns
  all_columns = select(Venue).where(Venue.id==venue_id).subquery() 
  venue = db.session.query(all_columns).first()
  
  # Convert into a readable dict format
  venue = dict(venue)
  
  # Get a list of past shows in a venue by various artist
  past_shows = db.session.query(
    Artist.id.label('artist_id'),
    Artist.name.label('artist_name'),
    Artist.image_link.label('artist_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.venue_id==venue_id, func.date(Show.start_time)<date.today()).all()
    
    
  
  # Get a list of upcoming shows in a venue by various artist
  upcoming_shows = db.session.query(
    Artist.id.label('artist_id'),
    Artist.name.label('artist_name'),
    Artist.image_link.label('artist_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.venue_id==venue_id, func.date(Show.start_time)>=date.today()).all()
    
  past_shows_count = len(past_shows)
  upcoming_shows_count = len(upcoming_shows)
  
  venue['past_shows'] = list(past_shows)
  venue['upcoming_shows'] = list(upcoming_shows)
  venue['past_shows_count'] = past_shows_count
  venue['upcoming_shows_count'] = upcoming_shows_count
          
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
 
  venue = Venue(**formdata)
  try:
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' +request.form['name']  + ' was successfully listed!')
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')
  finally:
    db.session.close()
  # on successful db insert, flash success
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except SQLAlchemyError as e:
    error = True
    db.session.rollback()
    flash('An error occurred venue could not be deleted')
  finally:
    db.session.close()
  if not error:
        return render_template('pages/home.html')
  else:
        return render_template('errors/505.html')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = db.session.query(
    Artist.id,
    Artist.name
  ).order_by('name').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  
  # Query to search by Artist names
  found_artists = db.session.query(
    Artist.id,
    Artist.name,
    func.count(case([(func.date(Show.start_time)>date.today(),1)])).label('num_upcoming_shows')
    ).outerjoin(Show).filter(
      Artist.name.ilike('%'+search_term+'%')
      ).group_by(Artist.id, Artist.name).order_by(Artist.name).all()
  
  num_of_found_artists = len(found_artists)
  response= { 
    "count": num_of_found_artists,
    "data": found_artists
  }
  return render_template(
    'pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  all_columns = select(Artist).where(Artist.id==artist_id).subquery()
  artist = db.session.query(all_columns).first()
  
  # Convert into a readable dict format
  artist = dict(artist)
  
  # Get a list of past shows by an artist in various venues
  past_shows = db.session.query(
    Venue.id.label('venue_id'),
    Venue.name.label('venue_name'),
    Venue.image_link.label('venue_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.artist_id==artist_id, func.date(Show.start_time)<date.today()).all()
    
  
  # Get a list of upcoming shows by an artist in various venues
  upcoming_shows = db.session.query(
    Venue.id.label('venue_id'),
    Venue.name.label('venue_name'),
    Venue.image_link.label('venue_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.artist_id==artist_id, func.date(Show.start_time)>=date.today()).all()
    
  past_shows_count = len(past_shows)
  upcoming_shows_count = len(upcoming_shows)
  
  artist['past_shows'] = list(past_shows)
  artist['upcoming_shows'] = list(upcoming_shows)
  artist['past_shows_count'] = past_shows_count
  artist['upcoming_shows_count'] = upcoming_shows_count
  
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):  
  # TODO: populate form with fields from artist with ID <artist_id>
  # Get all columns from artist
  all_columns = select(Artist).where(Artist.id==artist_id).subquery()
  artist = db.session.query(all_columns).first()
  
  # Populate form fileds from artist with ID <artis_id>
  form = ArtistForm(obj=artist)
 
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
  
  db.session.query(Artist).filter(Artist.id==artist_id).update({**formdata})
    
  artist = None
  try:
    db.session.commit()
    # Query edited artist information
    artist = db.session.query(
      Artist.id,
      Artist.name
      ).filter(Artist.id==artist_id).first()
    
    flash('Artist ' +artist['name']  + ' was edited succssfully')
  except SQLAlchemyError as e:
    db.session.rollback()    
    flash('An error occurred. Artist ' + artist['name'] + ' could not be updated.', 'error')
  finally:
    db.session.close()
    
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  
  # Get all columns from venues
  all_columns = select(Venue).where(Venue.id==venue_id).subquery()
  venue = db.session.query(all_columns).first()
  
  # Populate form fileds from venue with ID <venue_id>
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
  
  db.session.query(Venue).filter(Venue.id==venue_id).update({**formdata})
    
  venue = None
  try:
    db.session.commit()
    # Query edited venue information
    venue = db.session.query(
      Venue.id,
      Venue.name
      ).filter(Venue.id==venue_id).first()
    
    flash('Venue ' +venue['name']  + ' was edited succssfully')
  except SQLAlchemyError as e:
    db.session.rollback()    
    flash('An error occurred. Venue ' + venue['name'] + ' could not be updated.', 'error')
  finally:
    db.session.close()
  
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
      form = ArtistForm()
      return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
 
  artist = Artist(**formdata)
  try:
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' +request.form['name']  + ' was successfully listed!')
  except SQLAlchemyError as e:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', 'error')
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = db.session.query(
    Show.venue_id,
    Venue.name.label('venue_name'),
    Show.artist_id,
    Artist.name.label('artist_name'),
    Artist.image_link.label('artist_image_link'),
    Show.start_time    
    ).join(Artist).join(Venue).all()
  
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
 
  show = Show(**formdata)
  try:
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except SQLAlchemyError as e:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
