#src/frontend/User/User_home_page.py

import flet as ft
from backend.Save_Data.save_book import load_books as backend_load_books


#############################################################################
def user_home_view(page: ft.Page):

    books_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Number")),
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Title")),
            ft.DataColumn(label=ft.Text("Author")),
        ],
        rows=[]
    )

    def load_books_to_table():
        books = backend_load_books()

        def navigate_to_detail(book):
            def handler(e):
                page.session.set("selected_book", book)  # Save book in session
                page.go("/book_detail")
            return handler
        
        limited_books = books[:10] # Limit to first 10 books for display

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
            for index, book in enumerate(limited_books)
        ]
        page.update()


    def go_show_more_books(e):
        page.go("/books")

######################################################################""
    # Logout Dialog
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
######################################################################""
    # Initial data load
    load_books_to_table()

    return ft.View(
        "/home",
        controls=[
            ft.AppBar(
                title=ft.Text(
                    "Welcome to SmartShelf !",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    style=ft.TextStyle(font_family="Times New Roman", letter_spacing=1.5)
                ),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.SEARCH,
                        tooltip="Search Book",
                        on_click=lambda e: page.go("/books")
                    ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Profile", on_click=lambda e: page.go("/user_profile")),
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
                    ft.Row(
                        controls=[books_table],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    ),
                    ft.TextButton(
                        "Show more..",
                        on_click=go_show_more_books,
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

        ]
    )
)


        ],
        bgcolor="#000000"
    )
