# src/backend/routes/add_book_logic.py

from backend.Save_Data.save_book import save_book, load_books

######### Add book logic

def get_next_id(books):
    if not books:
        return "0000"
    max_id = max(int(book["id"]) for book in books)
    return f"{max_id + 1:04d}"  # Ensure ID is 4 digits

def add_book(title, author, description, published_date, isbn, category, language,
             pages, publisher, rating, download_url):
    books = load_books()

    if any(book["title"].lower() == title.lower() for book in books):
        return False, "Book already exists."

    next_id = get_next_id(books)

    new_book = {
        "id": next_id,
        "title": title,
        "author": author,
        "description": description,
        "published_date": published_date,
        "isbn": isbn,
        "category": category,
        "language": language,
        "pages": pages,
        "publisher": publisher,
        "rating": rating,
        "download_url": download_url
    }

    books.append(new_book)
    save_book(books)
    return True, "Book added successfully."
