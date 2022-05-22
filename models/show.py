from config.base import db

class Show(db.Model):
    __tablename__ = "Show"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', onupdate='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', onupdate="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f'<Show {self.id} {self.booked_date}>'
    