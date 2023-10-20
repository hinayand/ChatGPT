import os

import flet as ft

from pages import chatgpt, setting


def index(page: ft.Page):
    page.window_width = 1024
    page.window_height = 768
    page.title = "ChatGPT"

    views = [setting.setting(page).controls, chatgpt.chatgpt(page).controls]

    current_view = ft.Column(
        views[0], alignment=ft.MainAxisAlignment.START, expand=True
    )

    def _switch_view(e: int):
        current_view.controls = views[e]
        page.update()

    def switch_view(e: int):
        _switch_view(e)

    action_list = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label="设置",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CHAT_OUTLINED,
                selected_icon=ft.icons.CHAT,
                label="ChatGPT",
            ),
        ],
        on_change=lambda e: switch_view(e.control.selected_index),
        visible=True,
    )

    def sidebar():
        action_list.visible = not action_list.visible
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
            ft.Row([action_list, current_view], expand=True),
        ],
    )
    return view
