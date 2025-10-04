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
        
        self.message_text = ft.Text("", color=ft.Colors.RED_500)
        self.content = self._build_ui()
        self._load_pending_claims()

    def _load_pending_claims(self, e=None):
        self.claims_data_table.rows.clear()
        
        try:
            url = f"{API_BASE_URL}/admin/claims/pending"
            response = requests.get(url, headers=get_headers())
            
            if response.status_code == 200:
                claims = response.json()
                if not claims:
                    self.message_text.value = "No pending claims to review."
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
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Claim {resolution_type}d successfully!"), open=True)
                self.page.update()
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
                ft.Text("Admin Dashboard - Pending Claims", size=28, weight=ft.FontWeight.BOLD),
                self.message_text,
                ft.Container(self.claims_data_table, expand=True, padding=10, border=ft.border.all(1, ft.Colors.BLACK12)),
                ft.ElevatedButton("Refresh Claims", on_click=self._load_pending_claims)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )