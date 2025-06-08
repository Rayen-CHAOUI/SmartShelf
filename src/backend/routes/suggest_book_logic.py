#src/backend/routes/suggest_book_logic.py

from backend.Save_Data.save_suggested_books import load_suggested_books, save_suggested_books

def add_suggested_book(title, author):
    suggested_books = load_suggested_books()
    
    # Check if the suggestion already exists (optional)
    if any(book["title"].lower() == title.lower() and book["author"].lower() == author.lower() for book in suggested_books):
        return False, "Suggested book already exists."
    
    suggested_books.append({"title": title, "author": author})
    save_suggested_books(suggested_books)
    return True, "Book suggestion submitted successfully."
