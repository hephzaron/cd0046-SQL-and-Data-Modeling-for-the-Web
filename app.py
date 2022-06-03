#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from zoneinfo import available_timezones
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select, case
from logging import Formatter, FileHandler
from werkzeug.datastructures import MultiDict
from forms import *
from flask_migrate import Migrate
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone, date
import logging
import dateutil.parser
import babel

#----------------------------------------------------------------------------#
# Import Models.
#----------------------------------------------------------------------------#

from models.models import Venue, Artist, Show, TimeAvailability, Album, Song, db
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
SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO')

app.config[
  'SQLALCHEMY_DATABASE_URI'
  ] = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_ECHO'] = eval(SQLALCHEMY_ECHO)

db.init_app(app)
migrate = Migrate(app, db)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium', period=False):
      parsed_date = dateutil.parser.parse(value) if isinstance(value, str) else value
      if period:
            # format time delta object to return the closest time tick
            delta = (datetime.now(timezone.utc) - parsed_date)
            return babel.dates.format_timedelta(delta, threshold=1, granularity='second',locale='en')
      if format == 'full':
            format="EEEE MMMM, d, y 'at' h:mma"
      elif format == 'medium':
            format="EE MM, dd, y h:mma"
      elif format == 'small':
            format="MMMM, y"
      return babel.dates.format_datetime(parsed_date, format, locale='en')
    


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# Get home page
@app.route('/')
def index():
  
  # Show recently added artists and venues
  artists = db.session.query(Artist).order_by(Artist.created_at.desc()).limit(10).all()  
  venues = db.session.query(Venue).order_by(Venue.created_at.desc()).limit(10).all()
  return render_template('pages/home.html', artists=artists, venues=venues)


#  Venues
#  ----------------------------------------------------------------
# Get list of venues
@app.route('/venues', methods=['GET'])
def venues():
  # TODO: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  # Query to fetch venues and number of upcoming shows
  # SQL Equivalent:
  # SELECT venue.id AS venue_id, venue.name AS venue_name, 
  # count(CASE WHEN (date(show.start_time) > %(date_1)s) THEN %(param_1)s END) AS num_upcoming_shows, 
  # venue.city AS venue_city
  # FROM venue LEFT OUTER JOIN show ON venue.id = show.venue_id GROUP BY venue.id, venue.name
  venues = db.session.query(
    Venue.id,
    Venue.name,
    func.count(case([
      (func.date(Show.start_time)>date.today(),1)
      ])).label('num_upcoming_shows')
    ).add_columns(Venue.city).outerjoin(Show).group_by(Venue.id, Venue.name).all()
  
  # Query to group Venues by city
  # SQL Equivalent:
  # SELECT venue.city AS venue_city, venue.state AS venue_state 
  # FROM venue GROUP BY venue.city, venue.state
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

# Route to search venue from the venues table
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  
  # Query to search by Venue names
  # SQL Equivalent:
  # SELECT venue.id AS venue_id, venue.name AS venue_name,
  # count(CASE WHEN (date(show.start_time) > GETDATE()) THEN %(param_1)s END) AS num_upcoming_shows
  # FROM venue LEFT OUTER JOIN show ON venue.id = show.venue_id
  # WHERE venue.name ILIKE %(search_term)s GROUP BY venue.id, venue.name ORDER BY venue.name
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

# GET request to show a venue using venue Id
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # Get the queries of all required columns
  # SQL Equivalent:
  # SELECT * FROM venue
  # WHERE venue.id = @venue_id
  # LIMIT 1
  all_columns = select(Venue).where(Venue.id==venue_id).subquery() 
  
  venue = db.session.query(all_columns).first()
  
  # Convert into a readable dict format
  venue = dict(venue)
  
  # Get a list of past shows in a venue by various artist
  # SQL Equivalent:
  # SELECT artist.id AS artist_id, artist.name AS artist_name, artist.image_link AS artist_image_link, show.start_time AS show_start_time
  # FROM artist LEFT OUTER JOIN show ON artist.id = show.artist_id
  # WHERE show.venue_id = @venue_id AND date(show.start_time) <= GETDATE();
  past_shows = db.session.query(
    Artist.id.label('artist_id'),
    Artist.name.label('artist_name'),
    Artist.image_link.label('artist_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.venue_id==venue_id, func.date(Show.start_time)<date.today()).all()
    
    
  
  # Get a list of upcoming shows in a venue by various artist
  # SQL Equivalent:
  # SELECT artist.id AS artist_id, artist.name AS artist_name, artist.image_link AS artist_image_link, show.start_time AS show_start_time
  # FROM artist LEFT OUTER JOIN show ON artist.id = show.artist_id
  # WHERE show.venue_id = @venue_id AND date(show.start_time) >= GETDATE();
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
  
  # Validate form entries before submission
  if form.validate():
        formdata = form.data
        # Remove csrf_token from data to be persisted to db
        formdata.pop('csrf_token')
        venue = Venue(**formdata)
        
        try:
          db.session.add(venue)
          db.session.commit()
          flash('Venue ' +request.form['name']  + ' was successfully listed!','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          # TODO: on unsuccessful db insert, flash an error instead.
          flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')
          return render_template('forms/new_venue.html', form=form)
        finally:
          db.session.close()
          # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
          # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return redirect(url_for('index'))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>/delete')
def delete_venue(venue_id):
      # TODO: Complete this endpoint for taking a venue_id, and using
      # # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
      try:
        venue = Venue.query.get(venue_id)
        venue_shows = db.session.query(Show).filter(Show.venue_id == venue_id).all()
        # Delete venue associations in shows table to enforce not null venue_id in show
        for show in venue_shows:
              db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue {} was deleted successfully'.format(venue.name),'success')
      except SQLAlchemyError as e:
        db.session.rollback()
        return not_found_error(e)
      finally:
        db.session.close()  
        
      return redirect(url_for('index'))
      

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
# Get list of created artists
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # SQL Equivalent
  # SELECT artist.id AS artist_id, artist.name AS artist_name 
  # FROM artist ORDER BY artist.name
  data = db.session.query(
    Artist.id,
    Artist.name
  ).order_by('name').all()
  return render_template('pages/artists.html', artists=data)

# Route to search for an artist from the artist table
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term', '')
  
  # Query to search by Artist names
  # SQL Equivalent: 
  # SELECT artist.id AS artist_id, artist.name AS artist_name, count(CASE WHEN (date(show.start_time) > GETDATE()) THEN %(param_1)s END) AS num_upcoming_shows
  # FROM artist LEFT OUTER JOIN show ON artist.id = show.artist_id
  # WHERE artist.name ILIKE %(@search_item)s GROUP BY artist.id, artist.name ORDER BY artist.name
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
  # SQL Equivalent:
  # SELECT * FROM artist
  # WHERE artist.id = artist_id
  # LIMIT 1;
  all_columns = select(Artist).where(Artist.id==artist_id).subquery()
  artist = db.session.query(all_columns).first()
  
  # Convert into a readable dict format
  artist = dict(artist)
  
  # Get a list of past shows by an artist in various venues
  # SQL Equivalents:
  # SELECT venue.id AS venue_id, venue.name AS venue_name, venue.image_link AS venue_image_link, show.start_time AS show_start_time
  # FROM venue LEFT OUTER JOIN show ON venue.id = show.venue_id
  # WHERE show.artist_id = artist_id AND date(show.start_time) < GETDATE();
  past_shows = db.session.query(
    Venue.id.label('venue_id'),
    Venue.name.label('venue_name'),
    Venue.image_link.label('venue_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.artist_id==artist_id, func.date(Show.start_time)<date.today()).all()
    
  
  # Get a list of upcoming shows by an artist in various venues
  # SQL Equivalents:
  # SELECT venue.id AS venue_id, venue.name AS venue_name, venue.image_link AS venue_image_link, show.start_time AS show_start_time
  # FROM venue LEFT OUTER JOIN show ON venue.id = show.venue_id
  # WHERE show.artist_id = artist_id AND date(show.start_time) > GETDATE();
  upcoming_shows = db.session.query(
    Venue.id.label('venue_id'),
    Venue.name.label('venue_name'),
    Venue.image_link.label('venue_image_link'),
    Show.start_time).outerjoin(Show).filter(
    Show.artist_id==artist_id, func.date(Show.start_time)>=date.today()).all()
   
  # Get a list of albums by an artist
  # SQL Equivalents:
  # SELECT album.id AS album_id, album.title AS album_title, Album.image_link AS album_image_link, Album.released_date AS album_released_date
  # FROM album
  # WHERE album.artist_id = artist_id 
  # SORT BY album.released_date DESC; 
  albums = db.session.query(
    Album.id.label('album_id'),
    Album.title.label('album_title'),
    Album.image_link.label('album_image_link'),
    Album.released_date.label('album_released_date')
    ).filter(Album.artist_id == artist_id).order_by(Album.released_date.desc()).all()
  
    
  total_albums_count = len(albums)
  
  data = []
  for album in albums:
        obj={}
        obj['album_id'] = album.album_id
        obj['album_title'] = album.album_title
        obj['album_image_link'] = album.album_image_link
        obj['album_released_date'] = album.album_released_date
        obj['total_albums_count'] = total_albums_count
        data.append(obj)
    
  past_shows_count = len(past_shows)
  upcoming_shows_count = len(upcoming_shows)

  artist['past_shows'] = list(past_shows)
  artist['upcoming_shows'] = list(upcoming_shows)
  artist['past_shows_count'] = past_shows_count
  artist['upcoming_shows_count'] = upcoming_shows_count
  artist['total_albums_count'] = total_albums_count
  artist['albums'] = data
  
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
    
  artist = db.session.query(Artist).filter(Artist.id==artist_id).first()
  
  # Validate artist entry form before submission
  if form.validate():
        try:
          db.session.query(Artist).filter(Artist.id==artist_id).update({**formdata})
          db.session.commit()
          # Query edited artist information
          artist = db.session.query(
            Artist.id,
            Artist.name
            ).filter(Artist.id==artist_id).first()
          
          flash('Artist ' +artist['name']  + ' was edited succssfully','success')
        except SQLAlchemyError as e:
          db.session.rollback()    
          flash('An error occurred. Artist ' + artist['name'] + ' could not be updated.', 'error')
          return server_error(e)
        finally:
          db.session.close()    
        return redirect(url_for('show_artist', artist_id=artist_id))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/edit_artist.html', form=form, artist=artist)       

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
  
  if form.validate():
        try:
          db.session.commit()
          # Query edited venue information
          venue = db.session.query(
            Venue.id,
            Venue.name
            ).filter(Venue.id==venue_id).first()
          flash('Venue ' +venue['name']  + ' was edited succssfully','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          flash('An error occurred. Venue ' + venue['name'] + ' could not be updated.', 'error')
          return server_error(e)
        finally:
          db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/edit_venue.html', form=form, venue=venue)

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
  
  if form.validate():
        formdata = form.data
        # Remove csrf_token from data to be persisted to db
        formdata.pop('csrf_token')
        artist = Artist(**formdata)
        
        try:
          db.session.add(artist)
          db.session.commit()
          flash('Artist ' +request.form['name']  + ' was successfully listed!','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          # TODO: on unsuccessful db insert, flash an error instead.
          flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', 'error')
          return server_error(e)
        finally:
          db.session.close()
        return redirect(url_for('index'))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # SQL Equivalent:
  # SELECT show.venue_id, venue.name AS venue_name, show.artist_id, artist.name AS artist_name,
  # artist.image_link AS artist_image_link, show.start_time AS show_start_time 
  # FROM show JOIN artist ON artist.id = show.artist_id JOIN venue ON venue.id = show.venue_id
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
  
  time_availability = db.session.query(TimeAvailability).filter(
    TimeAvailability.artist_id==formdata['artist_id']).first()
  
  # Disallow booking an artist outside his schedule provided he has atleast  an available time
  if (time_availability != None and time_availability != formdata['start_time'] ):
        flash('This artist is not available on '+ format_datetime(formdata['start_time']),'info')
        return render_template('forms/new_show.html', form=form)
      
      
  show = Show(**formdata)
  
  # Validate Show form entry before submission
  if form.validate():
        try:
          db.session.add(show)
          db.session.commit()
          flash('Show was successfully listed!','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          # TODO: on unsuccessful db insert, flash an error instead.
          flash('An error occurred. Show could not be listed.','error')
          return render_template('forms/new_show.html', form=form)
        finally:
          db.session.close()
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return redirect(url_for('index'))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/new_show.html', form=form)
      
# Add: Display form to create available times
@app.route('/available/create')
def create_available_time():
      
  # renders availability form
  form = TimeAvailabilityForm()
  return render_template('forms/new_time_availability.html', form=form)

# Add: An artist can create time to be avialble for booking
@app.route('/available/create', methods=['POST'])
def create_available_time_submission():
      
  form = TimeAvailabilityForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
  
  time_availability = TimeAvailability(**formdata)
  
  # Validate available time entry before submission
  if form.validate():
        try:
          db.session.add(time_availability)
          db.session.commit()
          flash('Available time was successfully added!','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          # TODO: on unsuccessful db insert, flash an error instead.
          flash('An error occurred. Time scheduled could not be listed.','error')
          return render_template('forms/new_time_availability.html', form=form)
        finally:
          db.session.close()
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('forms/new_time_availability.html', form=form)
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/new_time_availability.html', form=form)
      
# Add: Display form to create an album
@app.route('/album/create')
def create_album():
      
  # renders album form
  form = AlbumForm()
  return render_template('forms/new_album.html', form=form)

# Add: An album can be created for an artist
@app.route('/album/create', methods=['POST'])
def create_album_submission():
  # called to create new album in the db, upon submitting new album form
  form = AlbumForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
  
  album = Album(**formdata)
  
  # Validate Album form entry before submission
  if form.validate():
        try:
          db.session.add(album)
          db.session.commit()
          flash(album.title + ' was successfully created!','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          
          flash('An error occurred. {} could not be created'.format(album.title),'error')
          return render_template('forms/new_album.html', form=form)
        finally:
          db.session.close()
        return redirect(url_for('show_artist', artist_id=album.artist_id))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/new_album.html', form=form)
      
# Add: Display form to create a song
@app.route('/song/create')
def create_song():
      
  # renders song form
  form = SongForm()
  return render_template('forms/new_song.html', form=form)

# Add: A song can be created for an album
@app.route('/song/create', methods=['POST'])
def create_song_submission():
  # called to create new song in the db, upon submitting new song form
  form = SongForm(formdata=MultiDict(request.form))
  formdata = form.data
  # Remove csrf_token from data to be persisted to db
  formdata.pop('csrf_token')
  
  song = Song(**formdata)
  # Query to get artist id 
  album = db.session.query(
    Album.artist_id).filter(
      Album.id==form.album_id.data).first()
  
  # Validate Song form entry before submission
  if form.validate():
        try:
          db.session.add(song)
          db.session.commit()
          flash(song.name + ' was successfully created!','success')
        except SQLAlchemyError as e:
          db.session.rollback()
          flash('An error occurred. {} could not be created'.format(song.name),'error')
          return render_template('forms/new_song.html', form=form)
        finally:
          db.session.close()
          return redirect(url_for('show_artist', artist_id=album.artist_id))
  else:
        flash(sum(form.errors.values(),[]),'error')
        return render_template('forms/new_song.html', form=form)
      

@app.route('/album/<int:album_id>/songs')
def show_album_songs(album_id):
      
  album = db.session.query(
    Album.title.label('album_title'),
    Album.artist_id
    ).filter(Album.id==album_id).first()
  
  songs = db.session.query(
    Album,
    Song.genre.label('song_genre'),
    Song.duration_seconds.label('song_duration_seconds'),
    Song.name.label('song_name'),
    Song.composer.label('song_composer')
    ).join(Song).filter(Album.id==album_id).all()
  
  print('album', album)
  print('songs', songs)
  return render_template('/pages/songs.html',album=album, songs=songs)
      
      

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
