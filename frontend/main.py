# frontend/main.py

import sys
sys.path.insert(0, '..')

import flet as ft
from frontend.api_client import set_auth
from frontend.views.login_view import LoginView
from frontend.views.signup_view import SignupView
from frontend.views.home_view import HomeView
from frontend.views.report_item_view import ReportItemView
from frontend.views.admin_dashboard import AdminDashboard

# Global State
app_state = {"token": None, "role": None}

def main(page: ft.Page):
    page.title = "Back2U - Lost and Found Management System"
    page.theme_mode = ft.ThemeMode.DARK 
    page.padding = 0
    page.spacing = 0
    
    # --- Theme Mode Toggle ---
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        # Update the icon in the navbar
        route_change(None)
        
    # --- Navbar ---
    def create_navbar():
        is_logged_in = app_state["token"] is not None
        is_admin = app_state["role"] == "admin"
        
        def logout(e):
            app_state["token"] = None
            app_state["role"] = None
            set_auth(None, None)  # Clear API client token
            page.go("/")

        # Build actions list
        actions = [
            ft.TextButton(
                text="Home", 
                on_click=lambda e: page.go("/"),
                style=ft.ButtonStyle(color=ft.Colors.WHITE)
            ),
        ]
        
        if is_logged_in:
            actions.append(
                ft.TextButton(
                    text="Report Item", 
                    on_click=lambda e: page.go("/report"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE)
                )
            )
            
            if is_admin:
                actions.append(
                    ft.TextButton(
                        text="Admin Dashboard", 
                        on_click=lambda e: page.go("/admin"),
                        style=ft.ButtonStyle(color=ft.Colors.WHITE)
                    )
                )
            
            actions.append(
                ft.IconButton(
                    icon=ft.Icons.LOGOUT, 
                    tooltip="Logout", 
                    on_click=logout,
                    icon_color=ft.Colors.WHITE
                )
            )
        else:
            actions.append(
                ft.TextButton(
                    text="Signup",
                    on_click=lambda e: page.go("/signup"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE)
                )
            )
            actions.append(
                ft.TextButton(
                    text="Login",
                    on_click=lambda e: page.go("/login"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE)
                )
            )
        
        # Theme toggle icon
        theme_icon = ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE
        actions.append(
            ft.IconButton(
                icon=theme_icon,
                tooltip="Toggle Theme",
                on_click=toggle_theme,
                icon_color=ft.Colors.WHITE
            )
        )

        return ft.AppBar(
            title=ft.Text("Back2U Portal", size=20, weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.Colors.BLUE_700,
            actions=actions,
            toolbar_height=60
        )

    # --- Routing Logic ---
    def route_change(route):
        page.views.clear()
        
        # Always add home as base view
        page.views.append(
            ft.View(
                "/",
                controls=[
                    create_navbar(),
                    HomeView(page)
                ],
                padding=0,
                spacing=0
            )
        )
        
        # Login View
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    controls=[
                        create_navbar(),
                        LoginView(page, app_state)
                    ],
                    padding=0,
                    spacing=0
                )
            )

        # Signup View
        elif page.route == "/signup":
            page.views.append(
                ft.View(
                    "/signup",
                    controls=[
                        create_navbar(),
                        SignupView(page)
                    ],
                    padding=0,
                    spacing=0
                )
            )
        
        # Report Item View (Protected)
        elif page.route == "/report":
            if app_state["token"]:
                page.views.append(
                    ft.View(
                        "/report",
                        controls=[
                            create_navbar(),
                            ReportItemView(page)
                        ],
                        padding=0,
                        spacing=0
                    )
                )
            else:
                # Redirect to login if not authenticated
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please login to report items"),
                    bgcolor=ft.Colors.RED_400
                )
                page.snack_bar.open = True
                page.go("/login")
        
        # Admin Dashboard View (Protected - Admin Only)
        elif page.route == "/admin":
            if app_state["token"] and app_state["role"] == "admin":
                page.views.append(
                    ft.View(
                        "/admin",
                        controls=[
                            create_navbar(),
                            AdminDashboard(page)
                        ],
                        padding=0,
                        spacing=0
                    )
                )
            elif app_state["token"]:
                # Logged in but not admin
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Admin access required"),
                    bgcolor=ft.Colors.RED_400
                )
                page.snack_bar.open = True
                page.go("/")
            else:
                # Not logged in
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please login as admin"),
                    bgcolor=ft.Colors.RED_400
                )
                page.snack_bar.open = True
                page.go("/login")
        
        page.update()

    def view_pop(view):
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/")

    # Set up routing handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Navigate to initial route
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)