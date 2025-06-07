# src/frontend/signup.py

import flet as ft
from backend.routes.signup_Logic import signup   # import signup logic

def signup_view(page: ft.Page):
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    message = ft.Text("", color="red", size=16)

    def signup_clicked(e):
        uname = username.value.strip()
        pwd = password.value.strip()
        if uname and pwd:
            success, msg = signup(uname, pwd)
            message.value = f"✅ {msg}" if success else f"{msg}"
            message.color = "green" if success else "red"
            if success:
                page.go("/home")
        else:
            message.value = "Both fields are required."
            message.color = "red"
        page.update()

    return ft.View(
        route="/signup",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Welcome again to SmartShelf", size=32, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Create your account below.", size=16, color="white"),
                        ft.Container(height=40),
                        username,
                        password,
                        ft.ElevatedButton(text="Signup", on_click=signup_clicked, width=300),
                        ft.Row(
                            controls=[
                                ft.Text("Already have an account?", color="white"),
                                ft.TextButton(
                                    text="Login",
                                    on_click=lambda e: page.go("/"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        message,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        bgcolor="#000000"
    )
