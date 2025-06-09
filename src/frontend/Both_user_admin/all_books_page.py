import flet as ft
from backend.Save_Data.save_book import load_books as backend_load_books
from backend.routes.suggest_book_logic import add_suggested_book


def all_books_view(page: ft.Page):
    # ------------------ Book Card Grid ------------------ #
    books_grid = ft.ResponsiveRow(
        spacing=15,
        run_spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # ------------------ Search Field ------------------ #
    search_field = ft.TextField(
        hint_text="Search by title or author...",
        width=400,
        suffix_icon=ft.Icons.SEARCH,
    )

    # ------------------ Suggest Book Dialog ------------------ #
    suggest_result_text = ft.Text(value="", color="green")

    suggest_title_field = ft.TextField(label="Book Title", width=300)
    suggest_author_field = ft.TextField(label="Author", width=300)

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

    # ------------------ Load Books to Grid ------------------ #
    def load_books_to_grid(filtered_books=None):
        books = filtered_books if filtered_books is not None else backend_load_books()
        books_grid.controls.clear()

        for book in books:
            def go_to_detail(book=book):
                def handler(e):
                    page.session.set("selected_book", book)
                    page.go("/book_detail")
                return handler

            card = ft.Container(
                width=250,
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                border_radius=12,
                border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                ink=True,
                on_click=go_to_detail(),
                content=ft.Column(
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(book["title"], size=16, weight="bold", overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(f"by {book['author']}", size=14, italic=True, color=ft.Colors.GREY_400),
                        ft.Text(f"ID: {book['id']}", size=12, color=ft.Colors.GREY_600),
                    ]
                )
            )

            books_grid.controls.append(
                ft.ResponsiveRow(
                    controls=[ft.Container(card, col={"sm": 12, "md": 6, "lg": 4})]
                )
            )

        page.update()

    # ------------------ Search Logic ------------------ #
    def search_books(e=None):
        keyword = search_field.value.strip().lower()
        if not keyword:
            load_books_to_grid()
        else:
            books = backend_load_books()
            filtered_books = [
                book for book in books
                if keyword in book["title"].lower() or keyword in book["author"].lower()
            ]
            load_books_to_grid(filtered_books)

    search_field.on_change = search_books

    # ------------------ Navigation ------------------ #
    def go_back(e):
        page.go("/home")

    # ------------------ Load Initially ------------------ #
    load_books_to_grid()

    # ------------------ View Layout ------------------ #
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
                                    on_click=lambda e: [setattr(search_field, "value", ""), load_books_to_grid()]
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Divider(),
                        books_grid,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
        ],
        bgcolor="#000000",
    )
