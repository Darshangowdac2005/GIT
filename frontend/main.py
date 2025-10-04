# frontend/main.py

import sys
sys.path.insert(0, '..')

import flet as ft
from frontend.api_client import set_auth
from frontend.views.login_view import LoginView
from frontend.views.home_view import HomeView
from frontend.views.report_item_view import ReportItemView

# Global State
app_state = {"token": None, "role": None}

def main(page: ft.Page):
    page.title = "Back2U - Lost and Found Management System"
    page.theme_mode = ft.ThemeMode.DARK 
    
    # --- Theme Mode Toggle ---
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        page.update()
        
    theme_icon = ft.Icon(ft.Icons.LIGHT_MODE)

    # --- Navbar ---
    def navbar_controls():
        is_logged_in = app_state["token"] is not None
        is_admin = app_state["role"] == "admin"
        
        def logout(e):
            app_state["token"] = None
            app_state["role"] = None
            set_auth(None, None) # Clear API client token
            page.go("/")

        return ft.AppBar(
            title=ft.Text("Back2U Portal"),
            actions=[
                ft.TextButton(text="Home", on_click=lambda e: page.go("/")),
                ft.TextButton(text="Report Item", on_click=lambda e: page.go("/report")),
                ft.TextButton(text="Admin Dashboard", on_click=lambda e: page.go("/admin")) if is_admin else ft.Container(),
                ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=logout) if is_logged_in else ft.TextButton(text="Login", on_click=lambda e: page.go("/login")),
                ft.IconButton(icon=theme_icon.icon, tooltip="Toggle Theme", on_click=toggle_theme)
            ]
        )

    # --- Routing Logic ---
    def route_change(route):
        page.views.clear()
        
        # Home View (Default)
        page.views.append(
            ft.View("/", [navbar_controls(), HomeView(page)])
        )
        
        if page.route == "/login":
            page.views.append(
                ft.View("/login", [navbar_controls(), LoginView(page, app_state)])
            )

        if page.route == "/report":
            if app_state["token"]:
                 page.views.append(
                    ft.View("/report", [navbar_controls(), ReportItemView(page)])
                )
            else:
                 page.go("/login")
        
        # Add /admin route here...
        
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = lambda view: (page.views.pop(), page.go(page.views[-1].route))
    
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)