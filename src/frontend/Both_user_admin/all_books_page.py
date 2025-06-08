import flet as ft
from backend.Save_Data.save_book import load_books as backend_load_books
from backend.routes.suggest_book_logic import add_suggested_book


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

    # Search field
    search_field = ft.TextField(
        hint_text="Search by title or author...",
        width=400,
        suffix_icon=ft.Icons.SEARCH,
    )

    # Result text for Suggest Book dialog
    suggest_result_text = ft.Text(value="", color="green")

    # Suggest Book input fields
    suggest_title_field = ft.TextField(label="Book Title", width=300)
    suggest_author_field = ft.TextField(label="Author", width=300)

    # --------------- Suggest Book Dialog --------------- #
    def open_suggest_book_dialog(e=None):
        page.dialog = suggest_book_dialog
        suggest_book_dialog.open = True
        page.update()

    def submit_suggest_book(e=None):
        title = suggest_title_field.value.strip()
        author = suggest_author_field.value.strip()

        if not title or not author:
            suggest_result_text.value = "Please fill in all fields."
            suggest_result_text.color = "red"
        else:
            success, message = add_suggested_book(title, author)
            suggest_result_text.value = message
            suggest_result_text.color = "green" if success else "red"
            if success:
                suggest_title_field.value = ""
                suggest_author_field.value = ""
                suggest_book_dialog.open = False
        page.update()

    def close_suggest_book_dialog(e=None):
        suggest_book_dialog.open = False
        suggest_result_text.value = ""
        page.update()

    suggest_book_dialog = ft.AlertDialog(
        title=ft.Text("Suggest a New Book"),
        content=ft.Column([suggest_title_field, suggest_author_field, suggest_result_text], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_suggest_book_dialog),
            ft.ElevatedButton("Submit", on_click=submit_suggest_book),
        ],
        actions_alignment="end",
    )
    page.overlay.append(suggest_book_dialog)

    # --------------- Load books into table --------------- #
    def load_books_to_table(filtered_books=None):
        books = filtered_books if filtered_books is not None else backend_load_books()

        def navigate_to_detail(book):
            def handler(e):
                page.session.set("selected_book", book)
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

    # --------------- Search logic --------------- #
    def search_books(e=None):
        keyword = search_field.value.strip().lower()
        if not keyword:
            load_books_to_table()
        else:
            books = backend_load_books()
            filtered_books = [
                book for book in books
                if keyword in book["title"].lower() or keyword in book["author"].lower()
            ]
            load_books_to_table(filtered_books)

    search_field.on_change = search_books

    # --------------- Navigation --------------- #
    def go_back(e):
        page.go("/home")

    # Load all books initially
    load_books_to_table()

    # --------------- View Definition --------------- #
    return ft.View(
        "/books",
        controls=[
            ft.AppBar(
                title=ft.Text("All Books"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(icon=ft.Icons.BOOK, tooltip="Suggest a Book", on_click=open_suggest_book_dialog),
                ]
            ),
            ft.Container(
                padding=20,
                bgcolor="#000000",
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    controls=[
                        ft.Row(
                            controls=[
                                search_field,
                                ft.TextButton(
                                    "Reset",
                                    on_click=lambda e: [setattr(search_field, "value", ""), load_books_to_table()]
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Divider(),
                        ft.Row(
                            controls=[books_table],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ),
        ],
        bgcolor="#000000",
    )
