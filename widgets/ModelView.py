import flet as ft


class ModelView(ft.UserControl):
    def __init__(self, model_page_path: str, model_name: str, model_description: str, current_page: ft.Page,
                 expand: bool | int = 1):
        super().__init__()
        self.model_page_path = model_page_path
        self.model_name = model_name
        self.model_description = model_description
        self.current_page = current_page
        self.expand = expand

    def build(self):
        return ft.Card(
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.CircleAvatar(content=ft.Text(self.model_name[0]), tooltip=self.model_name),
                        ft.Text(self.model_name, style=ft.TextThemeStyle.TITLE_LARGE, expand=1)
                    ]),
                    ft.Row([
                        ft.Text(self.model_description, style=ft.TextThemeStyle.BODY_LARGE, expand=1)
                    ]),
                    ft.Row([
                        ft.TextButton(text="前往",
                                      icon=ft.icons.START,
                                      on_click=lambda _: self.current_page.go(self.model_page_path))
                    ])
                ], expand=self.expand)
            , expand=self.expand, margin=10)
        )
