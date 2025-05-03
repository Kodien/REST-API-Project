## app.py - This file sets up and configures your Flask web application.
# It connects to the database, registers routes for different resources, and sets up the API documentation.

# ------------------------------
# 📦 Import necessary libraries
# ------------------------------

import os  # Used to access environment variables (like database URLs)

from flask import Flask, jsonify  # Imports the Flask class to create your web application
from flask_smorest import Api  # Used to organize your REST API using Blueprints and generate OpenAPI documentation
from flask_jwt_extended import JWTManager # Imports the flask jwt that creates an access token for your user when they logged in.
from flask_migrate import Migrate

from models import BlocklistModel
from models import ItemModel
from models import StoreModel
from models import TagModel
from models import ItemTags
from models import UserModel
from db import db  # Imports the SQLAlchemy instance from your db.py (used for database interaction)

# -------------------------------------
# 📦 Import your API Blueprints (routes)
# -------------------------------------

# Each blueprint handles a different part of your API (items, stores, tags)
from Resources.user import blup as UserBlueprint
from Resources.item import blup as ItemBlueprint
from Resources.store import blup as StoreBlueprint
from Resources.tag import blup as TagBlueprint

# ---------------------------------------------
# 🧠 Define the application factory function
# ---------------------------------------------
# This pattern is used so your app can be easily reused for testing or multiple environments
def create_app(db_url=None):
    """Creates and configures the Flask application."""

    # 1️⃣ Initialize the app
    app = Flask(__name__)  # Creates the Flask app object

    # 2️⃣ Configure Flask-Smorest for Swagger API documentation
    app.config["PROPAGATE_EXCEPTIONS"] = True  # Ensures all errors are shown during development
    app.config["API_TITLE"] = "First REST API"  # Title for the API docs
    app.config["API_VERSION"] = "v1"  # API version shown in docs
    app.config["OPENAPI_VERSION"] = "3.0.3"  # OpenAPI version used for documentation
    app.config["OPENAPI_URL_PREFIX"] = "/"  # API docs will be available at root URL
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # Path to open Swagger UI
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  
    # URL for Swagger UI frontend (uses CDN)

    # 3️⃣ Set up the database connection
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    )
    # If `db_url` is passed, use that.
    # Otherwise, check if there's an environment variable named DATABASE_URL.
    # If not, fall back to using a local SQLite file called data.db.

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Turn off tracking changes (saves memory)

    # 4️⃣ Initialize the database with the Flask app
    db.init_app(app)  # Connect the app to SQLAlchemy so it knows how to manage the database
    migrate = Migrate(app, db)
    

    # Set up the RESTful API
    api = Api(app)  # Creates a new API object tied to this app

    # 1. Set up the secret key used for creating and verifying JWT (JSON Web Token)
    app.config["JWT_SECRET_KEY"] = "261787263306589631644087030807851935536"
    # 2. Initialize the JWTManager for handling authentication with JWT tokens
    jwt = JWTManager(app)

    # This function adds extra data (claims) to the JWT when it's created
    @jwt.additional_claims_loader  
    def add_claims_to_jwt(identity):  
        # If the user's identity is 1 (usually the first user created)
        if identity == 1:  
            return {"is_admin": True}  # Add "is_admin: True" to the token
        return {"is_admin": False}    # For all other users, set "is_admin" to False

    
    # This function is called when a token is used after it has expired
    @jwt.expired_token_loader  
    def expired_token_callback(jwt_header, jwt_payload):  
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),  
            401,  # Return a 401 Unauthorized status code
        )


    # This function handles tokens that are invalid (for example, if someone tampers with them)
    @jwt.invalid_token_loader  
    def invalid_token_callback(error):  
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}  
            ),
            401,
        )

    # This function runs when a request is missing a token entirely
    @jwt.unauthorized_loader  
    def missing_token_callback(error):  
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    
    # This function checks if the token's ID (jti) is in the blocklist database
    @jwt.token_in_blocklist_loader  
    def check_if_token_in_blocklist(jwt_header, jwt_payload):  
        token_jti = jwt_payload["jti"]  # Get the unique token ID
        # Check if this jti exists in the blocklist table
        return BlocklistModel.query.filter_by(jti=token_jti).first() is not None



    # This function runs when a user tries to use a token that has been manually revoked (like after logout)
    @jwt.revoked_token_loader  
    def revoked_token_callback(jwt_header, jwt_payload):  
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}  
            ),
            401,
        )

    
    # This function handles tokens that aren't "fresh"
    # A fresh token means the user has just logged in, not just refreshed their old token
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )




    # Register route groups using Blueprints
    api.register_blueprint(UserBlueprint) # Registers routes for /user 
    api.register_blueprint(ItemBlueprint)  # Registers routes for /item
    api.register_blueprint(StoreBlueprint)  # Registers routes for /store
    api.register_blueprint(TagBlueprint)  # Registers routes for /tag

    # ✅ Done setting everything up — return the app object
    return app

# Actually create the app by calling the function above.
# This allows the app to run when you use `flask run`
app = create_app()