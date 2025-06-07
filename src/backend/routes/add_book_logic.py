# src/backend/routes/add_book_logic.py

from backend.Save_Data.save_book import save_book, load_books

######### add book logic

def get_next_id(books):
    if not books:
        return "0000"
    max_id = max(int(book["id"]) for book in books)
    return f"{max_id + 1:04d}" # Ensure ID is 4 digits

def add_book(title, author):
    books = load_books()
    if any(u["title"] == title for u in books):
        return False, "Book already exists."
    
    next_id = get_next_id(books)
    books.append({"id": next_id, "title": title, "author": author})
    save_book(books)
    return True, "Add book successful."
