from config.base import db

class Venue(db.Model):
    __tablename__ = 'Venue'

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
    seeking_description = db.Column(db.String(120), nullable=False)
    
    
    artist = db.relationship('Artist', secondary='Show', backref=db.backref('venue', lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.state}>'