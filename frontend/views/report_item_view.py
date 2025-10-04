# frontend/views/report_item_view.py

import flet as ft
from frontend.api_client import report_item_api, get_categories

class ReportItemView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        self.title_field = ft.TextField(label="Item Name", width=400)
        self.desc_field = ft.TextField(label="Detailed Description", multiline=True, min_lines=3, width=400)
        self.status_choice = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="lost", label="I Lost This Item"),
            ft.Radio(value="found", label="I Found This Item")
        ]), value="lost")
        
        categories = get_categories()
        self.category_options = [ft.dropdown.Option(str(c['category_id']), c['name']) for c in categories]
        self.category_choice = ft.Dropdown(label="Category", width=400, options=self.category_options, value=self.category_options[0].key)
        
        self.message_text = ft.Text("")
        
        self.content = self._build_ui()

    def _handle_report_submit(self, e):
        report_data = {
            "title": self.title_field.value,
            "description": self.desc_field.value,
            "status": self.status_choice.value,
            "category_id": int(self.category_choice.value),
        }
        
        if not all([self.title_field.value, self.desc_field.value, self.status_choice.value, self.category_choice.value]):
            self.message_text.value = "Please fill out all fields."
            self.page.update()
            return
            
        self.message_text.value = "Submitting report..."
        self.page.update()
        
        result = report_item_api(report_data)
        
        if 'id' in result:
            self.message_text.value = "Report submitted successfully! Check Home for listings."
            self.page.go("/")
        else:
            self.message_text.value = result.get('error', 'Report failed.')
            
        self.page.update()
        
    def _build_ui(self):
        return ft.Column(
            [
                ft.Text("Report Lost or Found Item", size=28, weight=ft.FontWeight.BOLD),
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.Row([ft.Text("Report Status:"), self.status_choice]),
                                self.title_field,
                                self.desc_field,
                                self.category_choice,
                                ft.ElevatedButton(text="Submit Report", on_click=self._handle_report_submit),
                                self.message_text
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        ),
                        padding=30
                    ),
                    elevation=10,
                    width=500
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )