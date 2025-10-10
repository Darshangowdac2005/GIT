# frontend/views/admin_dashboard.py

import flet as ft
from frontend.api_client import get_headers, API_BASE_URL
import requests

class AdminDashboard(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, padding=20)
        self.page = page
        self.claims_data_table = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Claim ID")),
            ft.DataColumn(ft.Text("Item Title")),
            ft.DataColumn(ft.Text("Claimant")),
            ft.DataColumn(ft.Text("Verification Details")),
            ft.DataColumn(ft.Text("Actions")),
        ], rows=[])
        # Categories management controls
        self.category_name_input = ft.TextField(label="New category name", width=300)
        self.categories_list = ft.ListView(expand=True, spacing=5, padding=10)
        self.edit_mode = None  # Track which category is being edited
        
        self.message_text = ft.Text("", color=ft.Colors.RED_500)
        self.content = self._build_ui()
        self._load_pending_claims()
        self._load_categories()

    def _load_pending_claims(self, e=None):
        self.claims_data_table.rows.clear()
        
        try:
            url = f"{API_BASE_URL}/admin/claims/pending"
            response = requests.get(url, headers=get_headers())
            
            if response.status_code == 200:
                claims = response.json()
                if not claims:
                    self.message_text.value = "No claims to review."
                else:
                    self.message_text.value = ""
                
                for claim in claims:
                    self.claims_data_table.rows.append(self._build_claim_row(claim))
            else:
                self.message_text.value = f"Error loading claims: {response.json().get('message', 'Auth failed.')}"
        except requests.exceptions.RequestException as err:
            self.message_text.value = f"Network error: API unreachable. {err}"
            
        self.page.update()
        
    def _handle_resolve_action(self, claim_id, resolution_type):
        try:
            url = f"{API_BASE_URL}/admin/claims/resolve"
            data = {"claim_id": claim_id, "resolution_type": resolution_type}
            response = requests.post(url, json=data, headers=get_headers())
            
            if response.status_code == 200:
                if self.page:
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"Claim {resolution_type}d successfully!"), open=True)
                # Notify other views (e.g., HomeView) to refresh their data
                if hasattr(self.page, "pubsub"):
                    self.page.pubsub.send_all("refresh_items")
                self._load_pending_claims()
            else:
                self.message_text.value = f"Failed to resolve claim: {response.json().get('error', 'API error.')}"
        except requests.exceptions.RequestException as err:
            self.message_text.value = f"Network error during resolution: {err}"
        self.page.update()


    def _build_claim_row(self, claim):
        claim_id = claim['claim_id']
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(claim_id))),
                ft.DataCell(ft.Text(claim['item_title'])),
                ft.DataCell(ft.Text(f"{claim['claimant_name']} ({claim['claimant_email']})")),
                ft.DataCell(ft.Text(claim['verification_details'][:30] + '...' if len(claim['verification_details']) > 30 else claim['verification_details'])),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(ft.Icons.CHECK, tooltip="Approve & Resolve", on_click=lambda e, cid=claim_id: self._handle_resolve_action(cid, 'approve'), icon_color=ft.Colors.GREEN_500),
                        ft.IconButton(ft.Icons.CLOSE, tooltip="Reject Claim", on_click=lambda e, cid=claim_id: self._handle_resolve_action(cid, 'reject'), icon_color=ft.Colors.RED_500),
                    ])
                ),
            ]
        )

    def _build_ui(self):
        return ft.Column(
            [
                ft.Text("Admin Dashboard - Claims Management", size=28, weight=ft.FontWeight.BOLD),
                self.message_text,
                ft.Container(self.claims_data_table, expand=True, padding=10, border=ft.border.all(1, ft.Colors.BLACK12)),
                ft.ElevatedButton("Refresh Claims", on_click=self._load_pending_claims),
                ft.Divider(height=20),
                ft.Text("Manage Categories", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.category_name_input,
                    ft.ElevatedButton("Add Category", icon=ft.Icons.ADD, on_click=self._handle_create_category)
                ]),
                ft.Container(self.categories_list, expand=True, padding=10, border=ft.border.all(1, ft.Colors.BLACK12))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

    # -----------------------------
    # Categories CRUD (UI logic)
    # -----------------------------

    def _load_categories(self, e: ft.ControlEvent | None = None):
        self.categories_list.controls.clear()
        try:
            url = f"{API_BASE_URL}/admin/categories"
            response = requests.get(url, headers=get_headers())
            if response.status_code == 200:
                categories = response.json() or []
                for cat in categories:
                    self.categories_list.controls.append(self._build_category_row(cat))
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Failed to load categories"), bgcolor=ft.Colors.RED_400, open=True)
        except requests.exceptions.RequestException as err:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Network error: {err}"), bgcolor=ft.Colors.RED_400, open=True)
        self.page.update()

    def _handle_create_category(self, e: ft.ControlEvent):
        name = (self.category_name_input.value or "").strip()
        if not name:
            self.page.snack_bar = ft.SnackBar(ft.Text("Enter category name"), bgcolor=ft.Colors.RED_400, open=True)
            return
        try:
            url = f"{API_BASE_URL}/admin/categories"
            response = requests.post(url, json={"name": name}, headers=get_headers())
            if response.status_code == 201:
                self.category_name_input.value = ""
                self.page.snack_bar = ft.SnackBar(ft.Text("Category created"), open=True)
                self._load_categories()
            else:
                try:
                    err_msg = response.json().get('error', 'Create failed')
                except Exception:
                    err_msg = f"Create failed (HTTP {response.status_code})"
                self.page.snack_bar = ft.SnackBar(ft.Text(err_msg), bgcolor=ft.Colors.RED_400, open=True)
        except requests.exceptions.RequestException as err:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Network error: {err}"), bgcolor=ft.Colors.RED_400, open=True)
        self.page.update()

    def _handle_delete_category(self, category_id: int):
        try:
            url = f"{API_BASE_URL}/admin/categories/{category_id}"
            response = requests.delete(url, headers=get_headers())
            if response.status_code == 200:
                self.page.snack_bar = ft.SnackBar(ft.Text("Category deleted"), open=True)
                self._load_categories()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(response.json().get('error', 'Delete failed')), bgcolor=ft.Colors.RED_400, open=True)
        except requests.exceptions.RequestException as err:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Network error: {err}"), bgcolor=ft.Colors.RED_400, open=True)
        self.page.update()

    def _save_edit_category(self, cid, name_field):
        new_name = (name_field.value or "").strip()
        if not new_name:
            self.page.snack_bar = ft.SnackBar(ft.Text("Name required"), bgcolor=ft.Colors.RED_400, open=True)
            self.page.update()
            return
        try:
            url = f"{API_BASE_URL}/admin/categories/{cid}"
            response = requests.put(url, json={"name": new_name}, headers=get_headers())
            if response.status_code == 200:
                self.page.snack_bar = ft.SnackBar(ft.Text("Category updated"), open=True)
                self.edit_mode = None
                self._load_categories()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(response.json().get('error', 'Update failed')), bgcolor=ft.Colors.RED_400, open=True)
        except requests.exceptions.RequestException as err:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Network error: {err}"), bgcolor=ft.Colors.RED_400, open=True)
        self.page.update()

    def _cancel_edit_category(self, e):
        self.edit_mode = None
        self._load_categories()

    def _on_edit_click(self, e, cid, name):
        self.edit_mode = cid
        self._load_categories()

    def _build_category_row(self, cat: dict) -> ft.Container:
        cid = cat.get('category_id')
        name = cat.get('name', '')
        if cid == self.edit_mode:
            name_field = ft.TextField(label="Category name", value=name, width=300)
            return ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(str(cid)), width=50),
                    ft.Container(name_field, expand=True),
                    ft.Row([
                        ft.ElevatedButton("Save", on_click=lambda e: self._save_edit_category(cid, name_field)),
                        ft.ElevatedButton("Cancel", on_click=self._cancel_edit_category),
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10,
                ink=True,
                border_radius=5,
                bgcolor=ft.Colors.WHITE10
            )
        else:
            return ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(str(cid)), width=50),
                    ft.Container(ft.Text(name), expand=True),
                    ft.Row([
                        ft.IconButton(ft.Icons.EDIT, tooltip="Edit", on_click=lambda e, _cid=cid, _name=name: self._on_edit_click(e, _cid, _name)),
                        ft.IconButton(ft.Icons.DELETE, tooltip="Delete", icon_color=ft.Colors.RED_400, on_click=lambda e, _cid=cid: self._handle_delete_category(_cid)),
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10,
                ink=True,
                border_radius=5,
                bgcolor=ft.Colors.WHITE10
            )
