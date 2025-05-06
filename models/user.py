# models/user.py - defines the user model and how it's stored in the database
# Allows us to store and manage user data

from db import db # Imports db which is a SQLAlchemy instance

class UserModel(db.Model): # Defines the user model and allows us to manage it
    __tablename__ = "users" # Defines the name for the table which is 'users'

    id = db.Column(db.Integer, primary_key=True) 
    # Creates a column in the database named 'id' which is an int and is set as a unique identifier (primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) 
    #Creates the username column which is a string with a max length of 80. Should be unique and can't be null
    password = db.Column(db.String(256), nullable=False) 
    # Creates the password column which is a string with a max length of 80 and can't be null
