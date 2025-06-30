from app import app
from models import db, Episode, Guest, Appearance
import csv
import os

def seed_database():
    """
    Seed the database with initial data
    """
    with app.app_context():
      
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
      
        print("Creating episodes...")
        episodes = [
            Episode(date="1/11/99", number=1),
            Episode(date="1/12/99", number=2),
            Episode(date="1/13/99", number=3),
            Episode(date="1/14/99", number=4),
            Episode(date="1/15/99", number=5),
        ]
        
        for episode in episodes:
            db.session.add(episode)
        
      
        print("Creating guests...")
        guests = [
            Guest(name="Michael J. Fox", occupation="actor"),
            Guest(name="Sandra Bernhard", occupation="Comedian"),
            Guest(name="Tracey Ullman", occupation="television actress"),
            Guest(name="Jon Stewart", occupation="comedian"),
            Guest(name="Julia Roberts", occupation="actress"),
        ]
        
        for guest in guests:
            db.session.add(guest)
        
      
        db.session.commit()
        
     
        print("Creating appearances...")
        appearances = [
            Appearance(episode_id=1, guest_id=1, rating=4),
            Appearance(episode_id=1, guest_id=2, rating=5),
            Appearance(episode_id=2, guest_id=3, rating=3),
            Appearance(episode_id=2, guest_id=4, rating=5),
            Appearance(episode_id=3, guest_id=5, rating=4),
        ]
        
        for appearance in appearances:
            db.session.add(appearance)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()