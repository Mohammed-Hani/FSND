#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from appFactory import create_app
from models import *

app = create_app()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
  if (isinstance(value, datetime)):
    str_value = value.strftime('%Y-%m-%dT%H:%M:%S.000Z')
  else:
    str_value = value
  date = dateutil.parser.parse(str_value)
  if format == 'full':
      format = "EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format = "EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en_US')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per
  #       venue.
  data = []
  for city, state in db.session.query(Venue.city, Venue.state).distinct().all():
      city_state = { 'city': city, 'state': state}
      city_state['venues'] = db.session.query(Venue.id, Venue.name).filter_by(city = city, state = state).all()
      data.append(city_state)
  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on venues with partial string search.  Ensure it is
  # case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live
  # Music & Coffee"
  search_trm = request.form.get('search_term', '')
  
  #using ORM
  data = db.session.query(Venue.id, Venue.name).filter(Venue.name.ilike('%'+ search_trm +'%')).all()
  
  #using SQL statement
  #data = db.session.execute("SELECT id, name FROM venues WHERE name ILIKE :search_term;", {'search_term':'%'+search_trm+'%'}).fetchall()
  
  response = {
    "count": len(data),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_trm)

def get_shows_sql(sign, model_id, out_model_type, in_model_type):
  
  str_stmt = """
    SELECT shows.{model_type}_id, {model_type}s.name, {model_type}s.image_link, shows.start_time
    FROM shows JOIN {model_type}s
    ON shows.{model_type}_id = {model_type}s.id
    WHERE shows.{cmp_model_type}_id = :cmp_model_id AND shows.start_time {compare_sign} NOW();
    """
  shows_stmt = db.text(str_stmt.format(model_type=out_model_type, compare_sign=sign, cmp_model_type=in_model_type))
  return db.session.execute(shows_stmt, {'cmp_model_id':model_id}).fetchall()


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  
  # using ORM
  vn = Venue.query.get(venue_id)
  past_shows_list = db.session.query(Show.artist_id, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Show.start_time).join(Artist)\
    .filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()

  upcoming_shows_list = db.session.query(Show.artist_id, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Show.start_time).join(Artist)\
    .filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all()
  
  #using SQL statement
  # past_shows_list = get_shows_sql('<', venue_id, 'artist', 'venue')
  # upcoming_shows_list = get_shows_sql('>', venue_id, 'artist', 'venue')

  data = vars(vn)
  data["genres"] = list(map(lambda genre: genre.name ,vn.genres))
  data["past_shows"] = past_shows_list
  data["upcoming_shows"] = upcoming_shows_list
  data["past_shows_count"] = len(past_shows_list)
  data["upcoming_shows_count"] = len(upcoming_shows_list)
    
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  error = False
  deassociatedDict = {}
  req = request.form
  form = VenueForm(req)
  if form.validate():
    try:
        venue = Venue()
        form.populate_obj(venue)
        #venue.genres.extend(Genre.query.filter(Genre.name.in_(req.getlist('genres'))).all())
        deassociatedDict = { 'name': venue.name}
        db.session.add(venue)
        db.session.commit()
    except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            flash('Venue ' + deassociatedDict['name'] + ' cannot be listed!', 'error')
            abort(500)
        else:
            # on successful db insert, flash success
            flash('Venue ' + deassociatedDict['name'] + ' was successfully listed!')
            # on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred.  Venue ' + data.name + ' could not be
            # listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            return render_template('pages/home.html')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    return render_template('pages/home.html')

def delete_obj(modl, obj_id):
  error = False
  try:
    obj = modl.query.get(obj_id)
    #obj.shows = []
    db.session.delete(obj)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      print(1)
      abort(500)
      print(2)
    else:
      #return render_template('pages/home.html')
      return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # taking a venue_id, and using
  # SQLAlchemy ORM to delete a record.  Handle cases where the session commit
  # could fail.
    return delete_obj(Venue, venue_id)
  

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # taking an artist_id, and using
  # SQLAlchemy ORM to delete a record.  Handle cases where the session commit
  # could fail.
    return delete_obj(Artist, artist_id)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  
  data = db.session.query(Artist.id, Artist.name).all()
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search.  Ensure it is
  # case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild
  # Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_trm = request.form.get('search_term', '')
  
  #using ORM
  data = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike('%'+ search_trm +'%')).all()
  
  #using SQL statement
  #data = db.session.execute("SELECT id, name FROM artists WHERE name ILIKE :search_term;", {'search_term':'%'+search_trm+'%'}).fetchall()

  response = {
    "count": len(data),
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=search_trm)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  
  # using ORM 
  artist = Artist.query.get(artist_id)
  past_shows_list = db.session.query(Show.venue_id, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'), Show.start_time).join(Venue)\
    .filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).all()

  upcoming_shows_list = db.session.query(Show.venue_id, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'), Show.start_time).join(Venue)\
    .filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
  
  # using SQL
  # past_shows_list = get_shows_sql('<', artist_id, 'venue', 'artist')
  # upcoming_shows_list = get_shows_sql('>', artist_id, 'venue', 'artist')


  data = vars(artist)
  data["genres"] = list(map(lambda genre: genre.name ,artist.genres))
  data["past_shows"] = past_shows_list
  data["upcoming_shows"] = upcoming_shows_list
  data["past_shows_count"] = len(past_shows_list)
  data["upcoming_shows_count"] = len(upcoming_shows_list)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  # populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  deassociatedDict = {}
  req = request.form
  form = ArtistForm(req)
  if form.validate():
    try:
        artist = Artist.query.get(artist_id)
        form.populate_obj(artist)
        deassociatedDict = { 'name': artist.name}
        db.session.commit()
    except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            flash('Artist ' + deassociatedDict['name'] + ' cannot be editted!', 'error')
            abort(500)
        else:
            # on successful db insert, flash success
            flash('Artist ' + deassociatedDict['name'] + ' was successfully editted!')
            # on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred.  Venue ' + data.name + ' could not be
            # listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    return render_template('pages/home.html')
  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  # populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  deassociatedDict = {}
  req = request.form
  form = VenueForm(req)
  if form.validate():
    try:
        venue = Venue.query.get(venue_id)
        form.populate_obj(venue)
        deassociatedDict = { 'name': venue.name}
        db.session.commit()
    except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            flash('Venue ' + deassociatedDict['name'] + ' cannot be editted!', 'error')
            abort(500)
        else:
            # on successful db insert, flash success
            flash('Venue ' + deassociatedDict['name'] + ' was successfully editted!')
            # on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred.  Venue ' + data.name + ' could not be
            # listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    return render_template('pages/home.html')
  

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  error = False
  deassociatedDict = {}
  req = request.form
  form = ArtistForm(req)
  if form.validate():
    try:
        artist = Artist()
        form.populate_obj(artist)
        #artist.genres.extend(Genre.query.filter(Genre.name.in_(req.getlist('genres'))).all())
        deassociatedDict = { 'name': artist.name}
        db.session.add(artist)
        db.session.commit()
    except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            flash('Artist ' + deassociatedDict['name'] + ' could not be listed!', 'error')
            abort(500)
        else:
            # on successful db insert, flash success
            flash('Artist ' + deassociatedDict['name'] + ' was successfully listed!')
            # on unsuccessful db insert, flash an error instead.
            return render_template('pages/home.html')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per
  #       venue.
  shows = Show.query.all()
  data = list(map(lambda shw: {
    'venue_id': shw.venue_id,
    'venue_name': shw.venue.name,
    'artist_id': shw.artist_id,
    'artist_name': shw.artist.name,
    'artist_image_link': shw.artist.image_link,
    'start_time': shw.start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
  }, shows))
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form.  do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  error = False
  form = ShowForm(request.form)
  if form.validate():
    try:
        show = Show()
        form.populate_obj(show)
        db.session.add(show)
        db.session.commit()
    except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            flash('An error occurred.  Show could not be listed.', 'error')
            abort(500)
        else:
            # on successful db insert, flash success
            flash('Show was successfully listed!')
            # on unsuccessful db insert, flash an error instead.
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            return render_template('pages/home.html')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
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
