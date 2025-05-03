# Import necessary tools to create views, handle routing, auth, and password hashing
from flask.views import MethodView  # Lets us organize routes in classes like in MVC
from flask_smorest import Blueprint, abort  # Blueprint groups related routes, abort stops request with error
from flask_jwt_extended import (  # Handles JWT tokens for auth
    create_access_token,  # Creates a short-term token (access token)
    create_refresh_token,  # Creates a long-term token (refresh token)
    get_jwt_identity,  # Gets the current user's identity from their token
    get_jwt,  # Gets the entire token data
    jwt_required  # A decorator to require a valid token for a route
)
from passlib.hash import pbkdf2_sha256  # Hashes and verifies passwords securely
from db import db  # The SQLAlchemy database connection
from models import UserModel  # The user model that matches the user table
from schemas import UserSchema  # Defines how to validate and serialize user data
from models.blocklist import BlocklistModel  # Model to store revoked JWTs

# Create a Blueprint for user-related routes
blup = Blueprint("Users", "users", description="Operations on users")


# Route for logging out a user by revoking their JWT
@blup.route("/logout")
class UserLogout(MethodView):
    @jwt_required()  # Require a valid JWT to access
    def post(self):
        jti = get_jwt()["jti"]  # Extract the token ID (jti) from the user's JWT
        block = BlocklistModel(jti=jti)  # Create a new blocklist record with that token ID
        db.session.add(block)  # Add it to the database session
        db.session.commit()  # Save changes to the database
        return {"message": "Successfully logged out"}, 200


# Route to register a new user
@blup.route("/register")
class UserRegister(MethodView):
    @blup.arguments(UserSchema)  # Validate and parse incoming data using UserSchema
    def post(self, user_data):
        # Check if a user with the same username already exists
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        # Create a new user with the hashed password
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)  # Add to database
        db.session.commit()  # Save to database

        return {"message": "User created successfully."}, 201


# Route to get or delete a user by their ID
@blup.route("/user/<int:user_id>")
class User(MethodView):
    """
    This is mostly for testing — to fetch or delete a specific user.
    Not recommended for production use unless secured.
    """

    @blup.response(200, UserSchema)  # Return user data serialized with UserSchema
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)  # Get the user or return 404
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)  # Get the user or 404
        db.session.delete(user)  # Delete the user
        db.session.commit()  # Save changes
        return {"message": "User deleted."}, 200


# Route for logging in a user
@blup.route("/login")
class UserLogin(MethodView):
    @blup.arguments(UserSchema)  # Validate and parse input
    def post(self, user_data):
        # Search for the user by username
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        # If user exists and password matches
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)  # Token for short-term use
            refresh_token = create_refresh_token(identity=str(user.id))  # Long-term token
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        # If login fails
        abort(401, message="Invalid credentials.")


# Route to refresh an access token using a refresh token
@blup.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)  # Only allow access with a valid refresh token
    def post(self):
        current_user = get_jwt_identity()  # Get the user ID from token
        new_token = create_access_token(identity=current_user, fresh=False)  # New access token

        # Optional: Revoke the refresh token after use
        jti = get_jwt()["jti"]  # Get token ID
        block = BlocklistModel(jti=jti)  # Add to blocklist
        db.session.add(block)
        db.session.commit()

        return {"access_token": new_token}, 200
