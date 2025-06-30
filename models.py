from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')
    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.number}: {self.date}>'

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')
    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.name}: {self.occupation}>'

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def __repr__(self):
        return f'<Appearance {self.guest.name} on Episode {self.episode.number}: Rating {self.rating}>'
