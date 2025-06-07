# src/frontend/all_users_page.py

import flet as ft
from backend.Save_Data.save_user import load_users as backend_load_users
from backend.routes.signup_Logic import signup as backend_add_user
from backend.routes.remove_user_logic import remove_user as backend_remove_user


def all_users_view(page: ft.Page):
    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Number")),
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Username")),
            ft.DataColumn(label=ft.Text("Password")),
        ],
        rows=[]
    )

    # Text fields and result display for dialogs
    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    id_field_user = ft.TextField(label="User ID", width=300)
    result_text = ft.Text(value="", color="green")

    # ------------------ Add User Dialog ------------------ #
    def open_add_user_dialog(e=None):
        page.dialog = add_user_dialog
        add_user_dialog.open = True
        page.update()

    def submit_add_user(e=None):
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not username or not password:
            result_text.value = "Please fill in all fields."
            result_text.color = "red"
        else:
            success, message = backend_add_user(username, password)
            result_text.value = message
            result_text.color = "green" if success else "red"
            if success:
                username_field.value = ""
                password_field.value = ""
                load_users_to_table()
                add_user_dialog.open = False
        page.update()

    def close_add_user_dialog(e=None):
        add_user_dialog.open = False
        result_text.value = ""
        page.update()

    add_user_dialog = ft.AlertDialog(
        title=ft.Text("Add New User"),
        content=ft.Column([username_field, password_field, result_text], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_add_user_dialog),
            ft.ElevatedButton("Add", on_click=submit_add_user),
        ],
        actions_alignment="end",
    )
    page.overlay.append(add_user_dialog)

    # ------------------ Remove User Dialog ------------------ #
    def open_remove_user_dialog(e=None):
        page.dialog = remove_user_dialog
        remove_user_dialog.open = True
        page.update()

    def submit_remove_user(e=None):
        user_id = id_field_user.value.strip()

        if not user_id:
            result_text.value = "Please enter a valid User ID."
            result_text.color = "red"
        else:
            success, message = backend_remove_user(user_id)
            result_text.value = message
            result_text.color = "green" if success else "red"
            if success:
                id_field_user.value = ""
                load_users_to_table()
                remove_user_dialog.open = False
        page.update()

    def close_remove_user_dialog(e=None):
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

    # ------------------ Load Users into Table ------------------ #
    def load_users_to_table():
        users = backend_load_users()
        users_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(index + 1))),
                    ft.DataCell(ft.Text(user["id"])),
                    ft.DataCell(ft.Text(user["username"])),
                    ft.DataCell(ft.Text(user["password"]))  # Consider hashing in production
                ]
            )
            for index, user in enumerate(users)
        ]
        page.update()

    load_users_to_table()

    # ------------------ Navigation ------------------ #
    def go_back(e):
        page.go("/home")

    return ft.View(
        "/users",
        controls=[
            ft.AppBar(
                title=ft.Text("All Users"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.BLUE_800,
                actions=[
                    ft.IconButton(icon=ft.Icons.ADD, on_click=open_add_user_dialog),
                    ft.IconButton(icon=ft.Icons.REMOVE, on_click=open_remove_user_dialog),
                ]
            ),
            ft.Container(
                expand=True,
                padding=20,
                bgcolor="#000000",
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[users_table],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True
                ),
            ),
        ],
        bgcolor="#000000"
    )
