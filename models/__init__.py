# models/__init__.py - This file makes the models package accessible for imports.
# It ensures that ItemModel and StoreModel can be imported easily from the models module.
# When we type import models (The folder) in another file, it imports everything from this file because of its name which is __init__.py

from models.user import UserModel  # Imports the UserModel from models/user.py
from models.item import ItemModel  # Imports the ItemModel from models/item.py
from models.store import StoreModel  # Imports the StoreModel from models/store.py
from models.tag import TagModel  # Imports the TagModel from models/tag.py
from models.item_tags import ItemTags # Impots the ItemTags from models/item_tags.py
from models.blocklist import BlocklistModel # Imports the BlocklistModel from models/blocklist.py
