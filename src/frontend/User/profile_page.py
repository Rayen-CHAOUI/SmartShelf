import flet as ft

def profile_view(page: ft.Page):
    user_name = page.session.get("user_name") or "Guest"

    return ft.View(
        route="/user_profile",
        controls=[
            ft.AppBar(
                leading=ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            on_click=lambda e: page.go("/home")
                        ),
                        ft.CircleAvatar(
                            radius=15,
                            content=ft.Image(
                                src="src/assets/profile_pic.png",
                                fit=ft.ImageFit.COVER,
                                width=30,
                                height=30
                            )
                        ),
                        ft.Text(
                            user_name,
                            color=ft.Colors.WHITE,
                            size=14,
                            weight=ft.FontWeight.BOLD
                        )
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(
                        ft.Icons.HELP,
                        on_click=lambda e: page.go("https://flet.dev/docs/controls/")
                    )
                ]
            ),
            ft.Column(
                controls=[
                    ft.Text(
                        "This is the Profile page.",
                        color=ft.Colors.WHITE
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        bgcolor="#000000"
    )
