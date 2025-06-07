import json
import os 

BOOKS_FILE = os.path.join(os.path.dirname(__file__), "books.json")

# Load all books
def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as f:
        return json.load(f)

# Save updated book list
def save_books(books):
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)

# Remove a book by ID
def remove_book_by_id(book_id):
    books = load_books()
    filtered_books = [book for book in books if book["id"] != book_id]
    if len(filtered_books) == len(books):
        return False, "Book ID not found."
    save_books(filtered_books)
    return True, "Book deleted successfully."
