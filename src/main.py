# src/main.py

import flet as ft

from frontend.Both_user_admin.all_books_page import all_books_view
from frontend.Admin.all_users_page import all_users_view
from frontend.Both_user_admin.book_details_page import book_detail_view
from frontend.Both_user_admin.login import login_view
from frontend.Both_user_admin.signup import signup_view
from frontend.Both_user_admin.settings_page import settings_view
from frontend.User.User_home_page import user_home_view
from frontend.User.profile_page import profile_view



def main(page: ft.Page):
    def route_change(e):
        page.views.clear()
        route = page.route
        if route == "/signup":
            page.views.append(signup_view(page))
        elif route == "/home":  
            page.views.append(user_home_view(page))
        elif route == "/settings":
            page.views.append(settings_view(page))
        elif route == "/books":
            page.views.append(all_books_view(page))
        elif route == "/users":
            page.views.append(all_users_view(page))
        elif page.route == "/book_detail":
            page.views.append(book_detail_view(page))
        elif page.route == "/user_profile":
            page.views.append(profile_view(page))
        else:
            page.views.append(login_view(page))
        page.update()


    page.on_route_change = route_change
    page.go(page.route) 

    page.title = "SmartShelf App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

if __name__ == "__main__":
 ft.app(target=main)  
  #ft.app(target=main, view=ft.WEB_BROWSER)    #   <----     OPEN IN WEB BROWSER    
