import flet as ft

def profile_view(page: ft.Page):
    return ft.View(
        route="/user_profile",
        controls=[
            ft.AppBar(
                title=ft.Text("Profile"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/home")),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(ft.Icons.HELP, on_click="clicked !"),         
                       ]
            ),
            ft.Column(
                controls=[
                    ft.Text("This is the Profile page.")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        bgcolor="#000000"
    )
