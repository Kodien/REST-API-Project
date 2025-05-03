# models/tag.py - Defines the TagModel for database interaction
# This file contains the TagModel class, which represents the 'tags' table in the database.
# It is used to store and manage tags that are associated with stores.

from db import db  # Import the SQLAlchemy database instance

class TagModel(db.Model):
    __tablename__ = "tags"  # Defines the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each tag
    name = db.Column(db.String(80), unique=False, nullable=False)  # Name of the tag, cannot be null
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)  # Foreign key linking to stores

    store = db.relationship("StoreModel", back_populates="tags")  # Establishes relationship with StoreModel
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags") # Establishes relationship with ItemModel
    