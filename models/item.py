# models/item.py - This file defines the ItemModel, which represents an item in the database.

from db import db  # Imports the SQLAlchemy database instance from db.py

class ItemModel(db.Model):  # Defines a model for items, inheriting from SQLAlchemy's base model
    __tablename__ = "items"  # Specifies the name of the table in the database

    # Defines the columns for the 'items' table
    id = db.Column(db.Integer, primary_key=True)  # Creates an 'id' column as an integer and sets it as the primary key which is a unique identifier
    name = db.Column(db.String(80), nullable=False)  # 'name' column with a max length of 80 characters, cannot be null
    description = db.Column(db.String) # 'description' column can be anything as long as it's a string
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)  # 'price' column as a float with 2 decimal places, required
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)  
    # 'store_id' is a foreign key referencing 'id' in the 'stores' table, linking items to stores

    store = db.relationship("StoreModel", back_populates="items")  
    # Establishes a relationship with StoreModel, allowing each item to be associated with a store
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    # Establishes a relationship with TagModel, allowing each item to be associated with many tags