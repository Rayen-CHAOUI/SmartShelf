# src/frontend/login.py

import flet as ft
from backend.routes.login_Logic import login  # ✅ Import login logic

def login_view(page: ft.Page):
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    message = ft.Text("", color="red", size=16)

    def login_clicked(e):
        uname = username.value.strip()
        pwd = password.value.strip()
        if uname and pwd:
            success, msg = login(uname, pwd)
            message.value = f"✅ {msg}" if success else f"{msg}"
            message.color = "green" if success else "red"
            if success:
                page.go("/home")  
        else:
            message.value = "Both fields are required."
            message.color = "red"
        page.update()

    def forgot_password_clicked(e):
        message.value = "Please contact support."
        message.color = "yellow"
        page.update()

    login_btn = ft.ElevatedButton(text="Login", on_click=login_clicked, width=300)


    return ft.View(
        "/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Welcome to SmartShelf !", size=32, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Please enter your credentials to login.", size=16, color="white"),
                        ft.Container(height=40),
                        username,
                        password,
                        login_btn,
                        ft.TextButton(
                            text="Forgot Password ?",
                            on_click=forgot_password_clicked,
                            style=ft.ButtonStyle(
                                color={"": "white"},
                                text_style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                            )
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(" Don't have an account ? ", color="white"),
                                ft.TextButton(
                                    text="Sign Up",
                                    on_click=lambda e: page.go("/signup")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        message
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,  # Fills the screen
            )
        ],
        bgcolor="#000000"
    )
