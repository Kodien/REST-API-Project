# models/blocklist.py - stores the blocklist models for logged out jti's

# Import the SQLAlchemy object
from db import db
# Import necessary functions
from datetime import datetime

# Defines the blocklist class for the model
class BlocklistModel(db.Model): # Inherits from db.Model class
    __tablename__ = "blocklist" # Sets the name of the table

    id = db.Column(db.Integer, primary_key=True)
    # id is an integer which acts as a unique identifier
    jti = db.Column(db.String(36), unique=True, nullable=False)
    # jti is a string with a max length of 36 characters that has to be unique and can't be null
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # creates_at is a date and time based on the date and time of the user's logout