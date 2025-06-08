#src/frontend/all_books_page.py

import flet as ft
from backend.Save_Data.save_book import load_books as backend_load_books
from backend.routes.add_book_logic import add_book as backend_add_book
from backend.routes.remove_book_logic import remove_book as backend_remove_book


def all_books_view(page: ft.Page):
    books_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Number")),
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Title")),
            ft.DataColumn(label=ft.Text("Author")),
        ],
        rows=[]
    )

    # Text fields and result display for dialogs
    title_field = ft.TextField(label="Book Title", width=300)
    author_field = ft.TextField(label="Author", width=300)
    id_field_book = ft.TextField(label="Book ID", width=300)
    result_text = ft.Text(value="", color="green")

    # ------------------ Add Book Dialog ------------------ #
    def open_add_book_dialog(e=None):
        page.dialog = add_book_dialog
        add_book_dialog.open = True
        page.update()

    def submit_add_book(e=None):
        title = title_field.value.strip()
        author = author_field.value.strip()

        if not title or not author:
            result_text.value = "Please fill in all fields."
            result_text.color = "red"
        else:
            success, message = backend_add_book(title, author)
            result_text.value = message
            result_text.color = "green" if success else "red"
            if success:
                title_field.value = ""
                author_field.value = ""
                load_books_to_table()
                add_book_dialog.open = False
        page.update()

    def close_add_book_dialog(e=None):
        add_book_dialog.open = False
        result_text.value = ""
        page.update()

    add_book_dialog = ft.AlertDialog(
        title=ft.Text("Add New Book"),
        content=ft.Column([title_field, author_field, result_text], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_add_book_dialog),
            ft.ElevatedButton("Add", on_click=submit_add_book),
        ],
        actions_alignment="end",
    )
    page.overlay.append(add_book_dialog)

    # ------------------ Remove Book Dialog ------------------ #
    def open_remove_book_dialog(e=None):
        page.dialog = remove_book_dialog
        remove_book_dialog.open = True
        page.update()

    def submit_remove_book(e=None):
        book_id = id_field_book.value.strip()

        if not book_id:
            result_text.value = "Please enter a valid Book ID."
            result_text.color = "red"
        else:
            success, message = backend_remove_book(book_id)
            result_text.value = message
            result_text.color = "green" if success else "red"
            if success:
                id_field_book.value = ""
                load_books_to_table()
                remove_book_dialog.open = False
        page.update()

    def close_remove_book_dialog(e=None):
        remove_book_dialog.open = False
        result_text.value = ""
        page.update()

    remove_book_dialog = ft.AlertDialog(
        title=ft.Text("Delete a Book"),
        content=ft.Column([id_field_book, ft.Text("Enter the Book ID to remove."), result_text], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_remove_book_dialog),
            ft.ElevatedButton("Remove", on_click=submit_remove_book),
        ],
        actions_alignment="end",
    )
    page.overlay.append(remove_book_dialog)

    # ------------------ Load Books into Table ------------------ #
    def load_books_to_table():
        books = backend_load_books()

        def navigate_to_detail(book):
            def handler(e):
                page.session.set("selected_book", book)  # Save book in session
                page.go("/book_detail")
            return handler

        books_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(index + 1))),
                    ft.DataCell(ft.Text(book["id"])),
                    ft.DataCell(ft.Text(book["title"])),
                    ft.DataCell(ft.Text(book["author"]))
                ],
                on_select_changed=navigate_to_detail(book)
            )
            for index, book in enumerate(books)
        ]
        page.update()

    load_books_to_table()

    # ------------------ Navigation ------------------ #
    def go_back(e):
        page.go("/home")

    return ft.View(
        "/books",
        controls=[
            ft.AppBar(
                title=ft.Text("All Books"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(icon=ft.Icons.ADD, on_click=open_add_book_dialog),
                    ft.IconButton(icon=ft.Icons.REMOVE, on_click=open_remove_book_dialog),
                ]
            ),
            ft.Container(
                expand=True,
                padding=20,
                bgcolor="#000000",
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[books_table],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True
                ),
            ),
        ],
        bgcolor="#000000"
    )
