# frontend/components/item_card.py

import flet as ft

class ItemCard(ft.Card):
    def __init__(self, item_data):
        super().__init__(elevation=3, width=600)
        self.item = item_data
        self.content = self._build_content()
    
    def _build_content(self):
        status_color = ft.Colors.GREEN_700 if self.item['status'] == 'found' else ft.Colors.RED_700
        
        return ft.Container(
            padding=15,
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text(self.item['title'], weight=ft.FontWeight.BOLD, size=18),
                        ft.Container(
                            content=ft.Text(self.item['status'].upper(), color=ft.Colors.WHITE, size=12),
                            bgcolor=status_color,
                            padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                            border_radius=5
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Category: {self.item.get('category_name', 'N/A')}"),
                    ft.Text(self.item['description'][:100] + ('...' if len(self.item['description']) > 100 else '')),
                    ft.Divider(),
                    ft.Row([
                        ft.Text(f"Reported by: {self.item['reporter_name']}", size=12, italic=True),
                        ft.ElevatedButton("File Claim", on_click=lambda e: print(f"Claiming item {self.item['item_id']}"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]
            )
        )
