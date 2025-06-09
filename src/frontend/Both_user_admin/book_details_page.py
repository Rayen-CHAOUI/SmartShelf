import flet as ft

def book_detail_view(page: ft.Page):
    selected_book = page.session.get("selected_book")

    if not selected_book:
        page.go("/books")
        return

    def download_book(e):
        book_url = selected_book.get("download_url")
        if book_url:
            page.launch_url(book_url)

    return ft.View(
        route="/book_detail",
        controls=[
            ft.AppBar(
                title=ft.Text("Book Details", size=22, weight="bold"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/books")),
                bgcolor=ft.Colors.BLUE_800,
            ),
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                padding=30,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Card(
                            elevation=8,
                            color=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                            shape=ft.RoundedRectangleBorder(radius=20),
                            content=ft.Container(
                                padding=30,
                                width=600,
                                content=ft.Column(
                                    spacing=15,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                    controls=[
                                        ft.Text(selected_book["title"], size=26, weight="bold", color="white"),
                                        ft.Text(f"by {selected_book['author']}", size=20, italic=True, color=ft.Colors.GREY_400),
                                        ft.Divider(height=10, color=ft.Colors.GREY_700),
                                        ft.Text(f"📅 Published: {selected_book['published_date']}", size=16, color="white"),
                                        ft.Text(f"📖 Pages: {selected_book['pages']} | 📚 Category: {selected_book['category']}", size=16, color="white"),
                                        ft.Text(f"🌐 Language: {selected_book['language']} | 🏢 Publisher: {selected_book['publisher']}", size=16, color="white"),
                                        ft.Text(f"⭐ Rating: {selected_book['rating']}", size=16, color=ft.Colors.YELLOW_600),
                                        ft.Text(f"🔢 ISBN: {selected_book['isbn']}", size=16, color=ft.Colors.GREY_300),
                                        ft.Text("📝 Description:", size=18, weight="bold", color="white"),
                                        ft.Text(selected_book['description'], size=15, color=ft.Colors.GREY_200),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            controls=[
                                                ft.ElevatedButton(
                                                    "Download",
                                                    icon=ft.Icons.DOWNLOAD,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.BLUE_700,
                                                        shape=ft.RoundedRectangleBorder(radius=12),
                                                        padding=20
                                                    ),
                                                    on_click=download_book
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        )
                    ]
                )
            )
        ],
        bgcolor=ft.Colors.BLACK
    )
