import flet as ft

from pages import chatgpt, setting, models


def index(page: ft.Page):
    page.window_width = 1024
    page.window_height = 768
    page.title = "ChatGPT"
    if page.client_storage.get("theme_color") is not None or not page.client_storage.get("theme_color") == "":
        page.theme.color_scheme_seed = page.client_storage.get("theme_color")

    views = [setting.setting(page).controls, chatgpt.chatgpt(page).controls, models.models(page).controls]

    current_view = ft.Column(
        views[0], alignment=ft.MainAxisAlignment.START, expand=True
    )

    action_list = ft.NavigationDrawer(
        selected_index=0,
        controls=[
            ft.Container(height=15),
            ft.NavigationDrawerDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label="设置",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.CHAT_OUTLINED,
                selected_icon=ft.icons.CHAT,
                label="ChatGPT",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.icons.MODEL_TRAINING_OUTLINED,
                selected_icon=ft.icons.MODEL_TRAINING,
                label="更多模型",
            )
        ],
        on_change=lambda e: switch_view(e.control.selected_index),
    )

    def _switch_view(e: int):
        current_view.controls = views[e]
        page.update()

    def switch_view(e: int):
        _switch_view(e)

    def sidebar():
        view.drawer.open = not view.drawer.open
        page.update()

    # Basic View
    view = ft.View(
        "/",
        controls=[
            ft.AppBar(
                title=ft.Text(value="ChatGPT"),
                leading=ft.IconButton(
                    ft.icons.MENU, on_click=lambda _: sidebar()),
            ),
            current_view
        ],
        drawer=action_list
    )
    return view
