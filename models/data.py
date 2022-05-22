from config.base import db
from  venue import Venue
from show import Show
from artist import Artist

venue1=Venue(
    id=1,
    name="The Musical Hop",
    address="1015 Folsom Street",
    city="San Francisco",
    state="CA",
    phone="123-123-1234",
    website="https://www.themusicalhop.com",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    seeking_talent=True,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
)

venue2= Venue(
    id = 2,
    name="The Dueling Pianos Bar",
    address="335 Delancey Street",
    city="New York",
    state="NY",
    phone="914-003-1132",
    website="https://www.theduelingpianos.com",
    facebook_link="https://www.facebook.com/theduelingpianos",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
)

venue3=Venue(
    id=3, 
    name="Park Square Live Music & Coffee",
    address="34 Whiskey Moore Ave",
    city="San Francisco",
    state="CA",
    phone="415-000-1234",
    website="https://www.parksquarelivemusicandcoffee.com",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
)
    
artist4 = Artist(
    id = 4,
    name = "Guns N Petals",
    city = "San Francisco",
    state = "CA",
    phone = 0000000000,
    genres = "Jazz",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
)

artist5 = Artist(
    id = 5,
    name = "Matt Quevedo",
    city = "San Francisco",
    state = "CA",
    phone = 0000000000,
    genres = "Rock n Roll",
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
)

artist6 = Artist(
    id = 6,
    name = "The Wild Sax Band",
    city = "San Francisco",
    state = "CA",
    phone = 0000000000,
    genres = "Rock n Roll",
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
)


show1 = Show(artist_id = 4, venue_id = 1, start_time="2019-05-21T21:30:00.000Z")
show2 = Show(artist_id = 5, venue_id = 3, start_time="2019-06-15T23:00:00.000Z")
show3 = Show(artist_id = 6, venue_id = 3, start_time="2035-04-01T20:00:00.000Z")
show4 = Show(artist_id = 6, venue_id = 3, start_time="2035-04-08T20:00:00.000Z")
show5 = Show(artist_id = 6, venue_id = 3, start_time="2035-04-15T20:00:00.000Z")

db.session.add(list)
db.session.commit()
db.session.close()
  
        
