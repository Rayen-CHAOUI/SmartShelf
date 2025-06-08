# src/frontend/book_detail_page.py

import flet as ft

def book_detail_view(page: ft.Page):
    selected_book = page.session.get("selected_book")

    if not selected_book:
        page.go("/books")  # Redirect if no book is selected
        return

    def download_book(e):
        book_url = selected_book.get("download_url")
        if book_url:
            page.launch_url(book_url)

    return ft.View(
        route="/book_detail",
        controls=[
            ft.AppBar(
                title=ft.Text("Book Details"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/home")),
                bgcolor=ft.Colors.BLUE_800,
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                bgcolor="#000000",
                content=ft.Column(
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(f"Title: {selected_book['title']}", size=24, color="white"),
                        ft.Text(f"Author: {selected_book['author']}", size=20, color="white"),
                        ft.Text(f"ID: {selected_book['id']}", size=18, color="white"),
                        ft.ElevatedButton("Download", icon=ft.Icons.DOWNLOAD, on_click=download_book)
                    ]
                )
            )
        ],
        bgcolor="#000000"
    )
