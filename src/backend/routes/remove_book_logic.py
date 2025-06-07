# src/backend/routes/remove_book_logic.py

from backend.Save_Data.delete_book import remove_book_by_id

######### remove book logic

def remove_book(book_id):
    return remove_book_by_id(book_id)