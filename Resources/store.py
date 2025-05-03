"""
resources/store.py - Defines RESTful API endpoints for managing stores.

This file provides all the logic for creating, retrieving, and deleting stores via HTTP requests.
It uses Flask-Smorest for structuring API routes, and SQLAlchemy for interacting with the database.
"""

# ----------------------------------
# 📦 Importing required dependencies
# ----------------------------------

from flask import request  # Used to access incoming request data (e.g., JSON payloads)
from flask.views import MethodView  # Lets us create class-based views for organizing HTTP methods
from flask_smorest import Blueprint, abort  # Blueprint helps group related routes; abort is used to return errors
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # Helps catch errors when working with the database

from db import db  # The SQLAlchemy instance used to access the database
from models import StoreModel  # The StoreModel class that maps to the "stores" table
from schemas import StoreSchema  # Marshmallow schema to validate and serialize store data

# -----------------------------------------------
# 🏗️ Define a Blueprint for store-related endpoints
# -----------------------------------------------
blup = Blueprint("stores", __name__, description="Operations on stores")

# --------------------------------------------------------
# 📂 /store/<store_id> endpoint — GET and DELETE requests
# --------------------------------------------------------

@blup.route("/store/<int:store_id>")  # Route to access a single store by ID (ID must be an integer)
class Store(MethodView):
    """
    Handles retrieving a single store and deleting it from the database.
    """

    @blup.response(200, StoreSchema)  # Serialize the returned store using StoreSchema
    def get(self, store_id):
        """
        GET /store/<store_id>
        Finds a store by its ID. If not found, it automatically sends a 404 error.
        """
        store = StoreModel.query.get_or_404(store_id)  # SQLAlchemy helper that returns 404 if store not found
        return store  # Return the store data if found

    def delete(self, store_id):
        """
        DELETE /store/<store_id>
        Deletes a store by its ID. If found, removes it from the database.
        """
        store = StoreModel.query.get_or_404(store_id)  # Check if the store exists or return 404
        db.session.delete(store)  # Remove the store from the session (not yet committed)
        db.session.commit()  # Finalize deletion in the database
        return {"message": "Store deleted"}  # Return a confirmation message

# ---------------------------------------------------
# 📂 /store endpoint — GET and POST for all stores
# ---------------------------------------------------

@blup.route("/store")  # Route for managing all stores at once
class StoreList(MethodView):
    """
    Handles listing all stores and creating a new one.
    """

    @blup.response(200, StoreSchema(many=True))  # many=True means return a list of serialized store objects
    def get(self):
        """
        GET /store
        Returns all stores in the database.
        """
        return StoreModel.query.all()  # Return a list of all store records

    @blup.arguments(StoreSchema)  # Validate incoming JSON data before using it
    @blup.response(201, StoreSchema)  # Serialize and return the new store with HTTP 201 Created
    def post(self, store_data):
        """
        POST /store
        Creates a new store using the provided JSON data.
        """
        store = StoreModel(**store_data)  # Unpack validated input into a StoreModel instance

        try:
            db.session.add(store)  # Add the new store to the database session
            db.session.commit()  # Commit the changes to persist the new store
        except IntegrityError:
            # This error usually means the store name is already in use (violates a uniqueness constraint)
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            # Catch any other general database errors (e.g., connection issues)
            abort(500, message="An error occurred when creating the store")

        return store, 201  # Return the created store with HTTP status code 201 (Created)
