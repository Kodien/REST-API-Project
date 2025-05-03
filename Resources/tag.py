"""
resources/tag.py — Defines RESTful API endpoints for working with tags.

This file lets us:
- View and create tags under a store
- Attach tags to items or remove them
- Retrieve and delete individual tags

It uses Flask-Smorest for structuring the API, and SQLAlchemy for database interaction.
"""

# 🧱 These are the tools we import to build our API logic

from flask.views import MethodView  # Allows us to define GET, POST, etc., as methods inside a class
from flask_smorest import Blueprint, abort  # Blueprint groups API routes, abort stops execution and returns an error
from sqlalchemy.exc import SQLAlchemyError  # Helps catch database errors

from db import db  # This is the database instance used to run queries
from models import TagModel, StoreModel, ItemModel  # Models that represent our tables: tags, stores, and items
from schemas import TagSchema, TagAndItemSchema  # Used to validate and format incoming/outgoing data


# 🔗 This groups all our tag-related endpoints under one namespace ("tags")
blup = Blueprint("Tags", "tags", description="Operations on tags")

# -------------------------------------------------------------------------------------
# /store/<store_id>/tag - Lets us view or create tags under a specific store
# -------------------------------------------------------------------------------------
@blup.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):

    @blup.response(200, TagSchema(many=True))  # Returns a list of tags
    def get(self, store_id):
        """
        GET /store/<store_id>/tag
        Gets all tags that belong to the store with the provided ID.
        """
        store = StoreModel.query.get_or_404(store_id)  # Look for the store or return a 404 error if not found
        return store.tags.all()  # Return all tags related to this store

    @blup.arguments(TagSchema)  # Validate the input using the TagSchema
    @blup.response(201, TagSchema)  # Return the created tag with a 201 Created status
    def post(self, tag_data, store_id):
        """
        POST /store/<store_id>/tag
        Creates a new tag under the store, if a tag with the same name doesn't exist already.
        """
        # Check if a tag with the same name already exists in the store
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")  # Stop if it does

        # If not, create a new tag and assign it to the store
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)  # Add the tag to the current session
            db.session.commit()  # Save it to the database
        except SQLAlchemyError as e:  # Catch any database-related errors
            abort(500, message=str(e))  # Return a 500 error and show what went wrong

        return tag  # Return the newly created tag

# ----------------------------------------------------------------------------------------------------
# /item/<item_id>/tag/<tag_id> - Lets us attach a tag to an item (or remove the tag from an item)
# ----------------------------------------------------------------------------------------------------
@blup.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):

    @blup.response(201, TagSchema)  # Return the tag that was linked
    def post(self, item_id, tag_id):
        """
        POST /item/<item_id>/tag/<tag_id>
        Links an existing tag to an existing item.
        """
        item = ItemModel.query.get_or_404(item_id)  # Look for the item
        tag = TagModel.query.get_or_404(tag_id)  # Look for the tag

        item.tags.append(tag)  # Link the tag to the item (many-to-many relationship)

        try:
            db.session.add(item)  # Save the updated item
            db.session.commit()  # Commit the changes
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")  # Handle any errors

        return tag  # Return the tag that was just added

    @blup.response(200, TagAndItemSchema)  # Return a message with the tag and item that were unlinked
    def delete(self, item_id, tag_id):
        """
        DELETE /item/<item_id>/tag/<tag_id>
        Unlinks a tag from an item (removes the relationship).
        """
        item = ItemModel.query.get_or_404(item_id)  # Look for the item
        tag = TagModel.query.get_or_404(tag_id)  # Look for the tag

        item.tags.remove(tag)  # Remove the tag from the item's tag list

        try:
            db.session.add(item)  # Save the item
            db.session.commit()  # Commit the change
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")  # Error handling
        return {
            "message": "Item removed from tag",  # Confirmation message
            "item": item,  # The item we updated
            "tag": tag  # The tag we removed
        }

# -------------------------------------------------------------------------------------
# /tag/<tag_id> - Lets us view or delete a single tag
# -------------------------------------------------------------------------------------
@blup.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blup.response(200, TagSchema)  # Return the tag
    def get(self, tag_id):
        """
        GET /tag/<tag_id>
        Retrieves a tag by its ID.
        """
        tag = TagModel.query.get_or_404(tag_id)  # Look for the tag or raise 404
        return tag

    @blup.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blup.alt_response(404, description="Tag not found.")  # Docs for 404 error
    @blup.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        """
        DELETE /tag/<tag_id>
        Deletes a tag only if it's not associated with any items.
        """
        tag = TagModel.query.get_or_404(tag_id)  # Find the tag

        if not tag.items:  # Only delete the tag if it's not connected to any items
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}

        # Otherwise, return an error message
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )
