# src/backend/data/save_book.py

import json
import os 

BOOKS_FILE = os.path.join(os.path.dirname(__file__), "books.json")

# check books existance
def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as f:
        return json.load(f)

# add new book
def save_book(books):
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)
