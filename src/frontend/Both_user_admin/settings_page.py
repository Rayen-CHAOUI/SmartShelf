import flet as ft

def settings_view(page: ft.Page):
    return ft.View(
        route="/settings",
        controls=[
            ft.AppBar(
                title=ft.Text("Settings"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/home")),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(ft.Icons.HELP, on_click="9iiiiw"),                ]
            ),
            ft.Column(
                controls=[
                    ft.Text("This is the Settings page.")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        bgcolor="#000000"
    )
