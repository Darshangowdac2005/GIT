# frontend/views/home_view.py

import flet as ft
from frontend.api_client import get_items
from frontend.components.item_card import ItemCard

class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, padding=20)
        self.page = page
        
        self.search_field = ft.TextField(label="Search by keyword or location", width=500)
        self.items_list = ft.ListView(expand=True, spacing=10)
        self.status_filter = ft.Dropdown(
            label="Filter Status",
            width=200,
            options=[
                ft.dropdown.Option("all", "All Listings"),
                ft.dropdown.Option("lost", "Lost Items"),
                ft.dropdown.Option("found", "Found Items"),
            ],
            value="all",
            on_change=self._load_items
        )
        
        self.content = self._build_ui()
        # Initial load
        self._load_items(None)

    def _load_items(self, e):
        self.items_list.controls.clear()
        
        status = self.status_filter.value if self.status_filter.value != 'all' else None
        
        # Display loading spinner while fetching
        self.items_list.controls.append(ft.Container(ft.ProgressRing(), alignment=ft.alignment.center))
        self.page.update()

        all_items = get_items(status=status)
        self.items_list.controls.clear()

        if not all_items:
            self.items_list.controls.append(ft.Text("No items found. Report one!", size=16))
        else:
            for item in all_items:
                self.items_list.controls.append(ItemCard(item))
                
        self.page.update()

    def _build_ui(self):
        return ft.Column(
            [
                ft.Text("Lost & Found Listings", size=28, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        self.search_field,
                        ft.ElevatedButton(text="Search", icon=ft.Icons.SEARCH, on_click=self._load_items),
                        self.status_filter
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True
                ),
                ft.Divider(height=10),
                ft.Text("Recent Listings (Unresolved)", size=20),
                self.items_list
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )