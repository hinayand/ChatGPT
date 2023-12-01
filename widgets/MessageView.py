import flet as ft
import asyncio


class MessageView(object):
    def __init__(self, avatar_content: str, avatar_tooltip: str, message_content: str, page: ft.Page):
        self.avatar_content = avatar_content
        self.avatar_tooltip = avatar_tooltip
        self.message_content = message_content
        self.widget = ft.Card(
            ft.Container(
                ft.Row([
                    ft.CircleAvatar(content=ft.Text(self.avatar_content), tooltip=self.avatar_tooltip),
                    ft.Markdown(self.message_content, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                code_theme="atom-one-dark", code_style=ft.TextStyle(font_family="Noto Mono"), expand=1,
                                auto_follow_links=True)
                ])
                , padding=10, on_long_press=lambda _: self.long_press(page), ink=True)
        )

    def get_widget(self):
        return self.widget

    def long_press(self, page: ft.Page):
        async def show_snack_bar():
            page.snack_bar = ft.SnackBar(ft.Text("文本已复制"))
            page.snack_bar.open = True
            page.update()
            await asyncio.sleep(3)
            page.snack_bar.open = False
            page.update()

        page.set_clipboard(self.message_content)
        asyncio.run(show_snack_bar())

