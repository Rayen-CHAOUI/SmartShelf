import flet as ft
from backend.routes.add_book_logic import add_book as backend_add_book
from backend.routes.remove_book_logic import remove_book as backend_remove_book
from backend.routes.signup_Logic import signup as backend_add_user
from backend.routes.remove_user_logic import remove_user as backend_remove_user
from backend.Save_Data.save_book import load_books as backend_load_books
from backend.Save_Data.save_user import load_users as backend_load_users


def Admin_home_view(page: ft.Page):
    title_field = ft.TextField(label="Book Title", width=300)
    author_field = ft.TextField(label="Author", width=300)
    download_url_field = ft.TextField(label="Download Link", width=300)
    description_field = ft.TextField(label="Description", width=300)
    published_date_field = ft.TextField(label="Published Date", width=300)
    isbn_field = ft.TextField(label="ISBN", width=300)
    category_field = ft.TextField(label="Category", width=300)
    language_field = ft.TextField(label="Language", width=300)
    pages_field = ft.TextField(label="Pages", width=300)
    publisher_field = ft.TextField(label="Publisher", width=300)
    rating_field = ft.TextField(label="Rating", width=300)

    result_text = ft.Text("", color="white")
    id_field_book = ft.TextField(label="Book ID", width=300)
    id_field_user = ft.TextField(label="User ID", width=300)
    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", width=300, password=True)

    books_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Number")),
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Title")),
            ft.DataColumn(label=ft.Text("Author")),
            ft.DataColumn(label=ft.Text("Download url"))
        ],
        rows=[]
    )

    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Number")),
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Username")),
            ft.DataColumn(label=ft.Text("Password")),
        ],
        rows=[]
    )

    def load_books_to_table():
        books = backend_load_books()
        limited_books = books[:5]
        books_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(index + 1))),
                    ft.DataCell(ft.Text(book["id"])),
                    ft.DataCell(ft.Text(book["title"])),
                    ft.DataCell(ft.Text(book["author"])),
                    ft.DataCell(ft.Text(book["download_url"]))
                ]
            )
            for index, book in enumerate(limited_books)
        ]
        page.update()

    def load_users_to_table():
        users = backend_load_users()
        limited_users = users[:5]
        users_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(index + 1))),
                    ft.DataCell(ft.Text(user["id"])),
                    ft.DataCell(ft.Text(user["username"])),
                    ft.DataCell(ft.Text(user["password"]))  # Should be encrypted
                ]
            )
            for index, user in enumerate(limited_users)
        ]
        page.update()

    def go_show_more_books(e):
        page.go("/books")

    def go_show_more_users(e):
        page.go("/users")

    def open_add_book_dialog(e):
        page.dialog = add_book_dialog
        add_book_dialog.open = True
        page.update()

    def submit_add_book(e):
        title = title_field.value.strip()
        author = author_field.value.strip()
        description = description_field.value.strip()
        published_date = published_date_field.value.strip()
        isbn = isbn_field.value.strip()
        category = category_field.value.strip()
        language = language_field.value.strip()
        pages = pages_field.value.strip()
        publisher = publisher_field.value.strip()
        rating = rating_field.value.strip()
        download_url = download_url_field.value.strip()

        if not title or not author or not download_url:
            result_text.value = "Please fill in required fields (title, author, download link)."
            result_text.color = "red"
        else:
            success, message = backend_add_book(
            title, author, description, published_date, isbn, category,
            language, pages, publisher, rating, download_url
        )
        result_text.value = message
        if success:
            for field in [title_field, author_field, description_field, published_date_field, isbn_field,
                          category_field, language_field, pages_field, publisher_field, rating_field, download_url_field]:
                field.value = ""
            load_books_to_table()
            add_book_dialog.open = False
    page.update()


    def close_add_book_dialog():
        add_book_dialog.open = False
        result_text.value = ""
        page.update()

    add_book_dialog = ft.AlertDialog(
        title=ft.Text("Add New Book"),
        content=ft.Column([
            title_field, author_field, description_field, published_date_field,
            isbn_field, category_field, language_field, pages_field,
            publisher_field, rating_field, download_url_field, result_text
        ], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_add_book_dialog),
            ft.ElevatedButton("Add", on_click=submit_add_book),
        ],
        actions_alignment="end",
    )

    page.overlay.append(add_book_dialog)

    def open_remove_book_dialog(e):
        page.dialog = remove_book_dialog
        remove_book_dialog.open = True
        page.update()

    def submit_remove_book(e):
        book_id = id_field_book.value.strip()

        if not book_id:
            result_text.value = "Please enter a valid Book ID."
            result_text.color = "red"
        else:
            success, message = backend_remove_book(book_id)
            result_text.value = message
            if success:
                id_field_book.value = ""
                load_books_to_table()
                remove_book_dialog.open = False
        page.update()

    def close_remove_book_dialog():
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

    def open_add_user_dialog(e):
        page.dialog = add_user_dialog
        add_user_dialog.open = True
        page.update()

    def submit_add_user(e):
        user_username = username_field.value.strip()
        user_password = password_field.value.strip()

        if not user_username or not user_password:
            result_text.value = "Please fill in all fields."
            result_text.color = "red"
        else:
            success, message = backend_add_user(user_username, user_password)
            result_text.value = message
            if success:
                username_field.value = ""
                password_field.value = ""
                load_users_to_table()
                add_user_dialog.open = False
        page.update()

    def close_add_user_dialog():
        add_user_dialog.open = False
        result_text.value = ""
        page.update()

    add_user_dialog = ft.AlertDialog(
        title=ft.Text("Add a User"),
        content=ft.Column([username_field, password_field, result_text], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_add_user_dialog),
            ft.ElevatedButton("Add", on_click=submit_add_user),
        ],
        actions_alignment="end",
    )
    page.overlay.append(add_user_dialog)

    def open_remove_user_dialog(e):
        page.dialog = remove_user_dialog
        remove_user_dialog.open = True
        page.update()

    def submit_remove_user(e):
        user_id = id_field_user.value.strip()

        if not user_id:
            result_text.value = "Please enter a valid User ID."
            result_text.color = "red"
        else:
            success, message = backend_remove_user(user_id)
            result_text.value = message
            if success:
                id_field_user.value = ""
                load_users_to_table()
                remove_user_dialog.open = False
        page.update()

    def close_remove_user_dialog():
        remove_user_dialog.open = False
        result_text.value = ""
        page.update()

    remove_user_dialog = ft.AlertDialog(
        title=ft.Text("Delete a User"),
        content=ft.Column([id_field_user, ft.Text("Enter the User ID to remove."), result_text], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_remove_user_dialog),
            ft.ElevatedButton("Remove", on_click=submit_remove_user),
        ],
        actions_alignment="end",
    )
    page.overlay.append(remove_user_dialog)

    logout_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to logout?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: page.go("/")),
            ft.TextButton("No", on_click=lambda e: (
                setattr(logout_modal, "open", False),
                setattr(page, "dialog", None),
                page.update()
            )),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    page.overlay.append(logout_modal)

    def open_logout_dialog(e):
        page.dialog = logout_modal
        logout_modal.open = True
        page.update()

    load_books_to_table()
    load_users_to_table()

    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(
                title=ft.Text(
                    "Welcome to Admin SmartShelf",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    style=ft.TextStyle(font_family="Times New Roman", letter_spacing=1.5)
                ),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Add Book", on_click=open_add_book_dialog),
                            ft.PopupMenuItem(text="Remove Book", on_click=open_remove_book_dialog),
                            ft.PopupMenuItem(text="Add User", on_click=open_add_user_dialog),
                            ft.PopupMenuItem(text="Remove User", on_click=open_remove_user_dialog),
                            ft.PopupMenuItem(text="Settings", on_click=lambda e: page.go("/settings")),
                            ft.PopupMenuItem(text="Logout", on_click=open_logout_dialog),
                        ]
                    )
                ],
            ),
            ft.Container(
                expand=True,
                padding=20,
                bgcolor="#000000",
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Books available in the Library", color="white", size=20),
                        ft.Row(
                            controls=[
                                ft.Row(controls=[books_table], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                                ft.TextButton(
                                    "Show more..", on_click=go_show_more_books,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(
                                            color=ft.Colors.BLUE_300,
                                            decoration=ft.TextDecoration.UNDERLINE
                                        )
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Text("Users Registered in the Library", color="white", size=20),
                        ft.Row(
                            controls=[
                                ft.Row(controls=[users_table], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                                ft.TextButton(
                                    "Show more..", on_click=go_show_more_users,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(
                                            color=ft.Colors.BLUE_300,
                                            decoration=ft.TextDecoration.UNDERLINE
                                        )
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ]
                )
            )
        ],
        bgcolor="#000000"
    )


if __name__ == "__main__":
    def main(page: ft.Page):
        page.views.append(Admin_home_view(page))
        page.go("/home")

    ft.app(target=main)
