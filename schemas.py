# Importing necessary classes from the marshmallow library, which is used for data serialization and validation.
from marshmallow import Schema, fields

# ------------------------------
# This file defines different schema classes using Marshmallow.
# Schemas are used to serialize (convert to JSON) and deserialize (convert from JSON) data.
# They also help with validation to ensure incoming data follows the correct format.
# ------------------------------

# This schema represents an item with basic properties: id, name, and price.
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)  # The "id" field is a string and can only be outputted (not accepted as input).
    name = fields.Str(required=True)  # The "name" field is a required string.
    price = fields.Float(required=True)  # The "price" field is a required floating-point number.

# This schema represents a store with basic properties: id and name.
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)  # The "id" field is a string and is output-only.
    name = fields.Str(required=True)  # The "name" field is a required string.

# This schema represents a tag with basic properties: id and name.
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True) # The "id field is an integer and is output-only."
    name = fields.Str() # The "name" field is a string.

# This schema is used when updating an item, meaning all fields are optional.
class ItemUpdateSchema(Schema):
    price = fields.Float()  # The "price" field is a floating-point number (optional).
    name = fields.Str()  # The "name" field is a string (optional).
    store_id = fields.Int()  # The "store_id" field is an integer (optional).

# This schema extends PlainItemSchema and adds a "store_id" field and a nested "store" object.
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)  
    # The "store_id" field is required when receiving data (load_only=True means it won’t be included in output).
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  
    # The "store" field is a nested object of PlainStoreSchema, and it is output-only (dump_only=True).
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    # The "tags" field is a list object that contains a nested object of PlainTagSchema and it's output only.

# This schema extends PlainStoreSchema and adds an "items" field that lists all items in the store.
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  
    # The "items" field is a list of PlainItemSchema objects, and it is output-only.
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)  
    # The "tags" field is a list of PlainTagSchema objects, and it is output-only.

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)  
    # The "store_id" field is load_only=True because that means it won’t be included in output.
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  
    # The "store" field is a nested object of PlainStoreSchema, and it is output-only (dump_only=True).
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    # The "items" field is a list containing a nested object of PlainItemSchema and it's output-only.

# Define the 'TagAndItemSchema' class, which is used to serialize and deserialize data related to both a tag and an item.
class TagAndItemSchema:
    # 'message' is a string field that can be used to store any message (optional or required based on context).
    message = fields.Str()
    # 'item' is a nested field that refers to the 'ItemSchema'.
    # This means that an 'item' is expected to be a complex object (in this case, an instance of 'ItemSchema').
    # 'ItemSchema' defines how item data should be serialized/deserialized.
    item = fields.Nested(ItemSchema)
    # 'tag' is a nested field that refers to the 'TagSchema'.
    # This means that a 'tag' is expected to be a complex object (in this case, an instance of 'TagSchema').
    # 'TagSchema' defines how tag data should be serialized/deserialized.
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True) 
    # The 'id' field is an integer that is output-only
    username = fields.Str(required=True) 
    # The 'username' field is a string that is required
    password = fields.Str(required=True, load_only=True) 
    # The 'password' field is a string that is required