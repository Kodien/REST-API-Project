"""
resources/item.py - Defines RESTful API endpoints for managing items.

This file creates the logic for your /item endpoints.
It uses Flask-Smorest for structuring API routes, and SQLAlchemy for interacting with the database.
Provides GET (read), POST (create), PUT (update), and DELETE (remove) functionality for items.
"""

# -------------------------
# 📦 Importing dependencies
# -------------------------

from flask import request  # Gives you access to request data like JSON payloads
from flask.views import MethodView  # Lets you create class-based views for cleaner API design
from flask_smorest import Blueprint, abort  # Blueprint groups routes; abort sends error responses
from flask_jwt_extended import jwt_required, get_jwt # jwt_required sets an endpoint to requiring a jwt, get_jwt checks if the user has a jwt or not
from sqlalchemy.exc import SQLAlchemyError  # Lets you catch and handle database-related errors

from db import db  # The SQLAlchemy database instance to interact with the database
from models import ItemModel  # Your item model that maps to the "items" table
from schemas import ItemSchema, ItemUpdateSchema  # Used to validate and format incoming/outgoing data

# -----------------------------------------------------
# 🏗️ Define a Blueprint for grouping item-related routes
# -----------------------------------------------------
# "blup" is a shortcut name used in the main app to register these routes
blup = Blueprint("items", __name__, description="Operations on items")

# -------------------------------
# 📂 /item endpoint (GET and POST)
# -------------------------------
@blup.route("/item")
class ItemList(MethodView):
    """
    Handles listing all items or creating a new item.
    """

    @jwt_required()
    @blup.response(200, ItemSchema(many=True))  # Output: a list of items, each validated by ItemSchema
    def get(self):
        """
        GET /item
        Retrieves all items from the database and returns them.
        """
        return ItemModel.query.all()  # Query all item records in the 'items' table

    @jwt_required(fresh=True)
    @blup.arguments(ItemSchema)  # Validates the request body before passing it into the method
    @blup.response(201, ItemSchema)  # Output: the created item, validated by ItemSchema
    def post(self, item_data):
        """
        POST /item
        Creates a new item with the provided JSON data.
        """
        item = ItemModel(**item_data)  # Unpack the JSON into an ItemModel instance

        try:
            db.session.add(item)  # Add the new item to the database session (not committed yet)
            db.session.commit()  # Save the changes to the database permanently
        except SQLAlchemyError:  # If something goes wrong (e.g., DB down, validation error)
            abort(500, message="An error occurred while inserting the item")  # Send a 500 response

        return item, 201  # Return the created item and HTTP status 201 (Created)

# -----------------------------------------------------
# 📂 /item/<item_id> endpoint (GET, DELETE, and PUT)
# -----------------------------------------------------
@blup.route("/item/<string:item_id>")
class Item(MethodView):
    """
    Handles retrieving, deleting, or updating a specific item based on its ID.
    """

    @jwt_required()
    @blup.response(200, ItemSchema)  # Output: a single item
    def get(self, item_id):
        """
        GET /item/<item_id>
        Looks for an item with the given ID. If found, return it. If not, raise a 404 error.
        """
        item = ItemModel.query.get_or_404(item_id)  # Find the item or return a 404 error automatically
        return item

    @jwt_required()
    def delete(self, item_id):  
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        """
        DELETE /item/<item_id>
        Deletes the item with the specified ID.
        """
        item = ItemModel.query.get_or_404(item_id)  # Find the item or raise 404 if not found
        db.session.delete(item)  # Mark the item for deletion
        db.session.commit()  # Save changes to the database
        return {"message": "Item deleted"}  # Return confirmation

    @blup.arguments(ItemUpdateSchema)  # Validates the incoming JSON data for update
    @blup.response(200, ItemSchema)  # Output: the updated or newly created item
    def put(self, item_data, item_id):
        """
        PUT /item/<item_id>
        Updates the existing item if found, or creates a new one if it doesn't exist.
        """
        item = ItemModel.query.get(item_id)  # Try to find the item

        if item: # If item is found
            # 🔄 Update the item with new values
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            # 🆕 If item doesn't exist, create a new one with that ID and the provided data
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)  # Add the new/updated item to the session
        db.session.commit()  # Save the changes
        return item  # Return the item data as confirmation
