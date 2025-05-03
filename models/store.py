# models/store.py - This file defines the StoreModel, which represents a store in the database.

from db import db  # Imports the SQLAlchemy database instance from db.py

class StoreModel(db.Model):  # Defines a model for stores, inheriting from SQLAlchemy's base model
    __tablename__ = "stores"  # Specifies the name of the table in the database

    # Defines the columns for the 'stores' table
    id = db.Column(db.Integer, primary_key=True)  
    # 'id' column as an integer, serves as the primary key (unique identifier for each store)

    name = db.Column(db.String(80), unique=True, nullable=False)  
    # 'name' column with a max length of 80 characters, must be unique, and cannot be null

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")  
    # Establishes a one-to-many relationship with ItemModel:
    # - 'back_populates="store"' allows bi-directional access (StoreModel -> ItemModel and vice versa)
    # - 'lazy="dynamic"' means items are loaded only when needed, improving performance
    # - 'cascade="all, delete"' ensures that deleting a store deletes all its associated items

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    # Establishes a one-to-many relationship with TagModel:
    # - 'back_populates="store"' allows bi-directional access (StoreModel -> TagModel and vice versa)
    # - 'lazy="dynamic"' means tags are loaded only when needed, improving performance