# item_tags.py - This file defines the item-tags relationship model, which represents the item-tag relationship

# Import the 'db' object from the 'db.py' file, which is responsible for setting up the database connection
# 'db' is an instance of SQLAlchemy, and it allows us to interact with the database using Python objects (models).
from db import db  

# Define the 'ItemTags' class, which is a database model representing the 'items_tags' table.
# This class allows us to store and manage the relationships between items and tags.
class ItemTags(db.Model):
    
    # '__tablename__' defines the name of the table in the database that this model will correspond to.
    # Here, we're using the table 'items_tags', which typically stores relationships between items and tags.
    __tablename__ = "items_tags"

    # 'id' is the primary key of the table. It uniquely identifies each row in the table.
    # 'db.Column(db.Integer)' defines the column as an integer type, and 'primary_key=True' makes it unique.
    id = db.Column(db.Integer, primary_key=True)

    # 'item_id' is a column that will store the ID of the associated item.
    # This creates a foreign key reference to the 'id' column in the 'items' table, linking the item to this table.
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    
    # 'tag_id' is a column that will store the ID of the associated tag.
    # It creates a foreign key reference to the 'id' column in the 'tags' table, linking the tag to this table.
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))