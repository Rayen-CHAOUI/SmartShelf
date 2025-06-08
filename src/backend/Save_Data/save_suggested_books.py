#src/backend/Save_Data/save_suggested_books.py

import json
import os

SUGGESTED_BOOKS_FILE = os.path.join(os.path.dirname(__file__), "suggested_books.json")

# Load suggested books if the file exists
def load_suggested_books():
    if not os.path.exists(SUGGESTED_BOOKS_FILE):
        return []
    with open(SUGGESTED_BOOKS_FILE, "r") as f:
        return json.load(f)

# Save suggested books list to the JSON file
def save_suggested_books(suggested_books):
    with open(SUGGESTED_BOOKS_FILE, "w") as f:
        json.dump(suggested_books, f, indent=4)
