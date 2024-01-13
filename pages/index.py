import flet as ft

from pages import chatgpt, setting, models


def index(page: ft.Page):
    page.window_width = 1024
    page.window_height = 768
    page.title = "ChatGPT"
    if not page.client_storage.get("theme_color") is None or not page.client_storage.get("theme_color") == "":
        page.theme.color_scheme_seed = page.client_storage.get("theme_color")

    views = [setting.setting(page).controls, chatgpt.chatgpt(page).controls, models.models(page).controls]

    current_view = ft.Column(
        views[0], alignment=ft.MainAxisAlignment.START, expand=True
    )

    action_list = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
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
            ft.NavigationRailDestination(
                icon=ft.icons.MODEL_TRAINING_OUTLINED,
                selected_icon=ft.icons.MODEL_TRAINING,
                label="更多模型",
            )
        ],
        on_change=lambda e: switch_view(e.control.selected_index),
        visible=True
    )

    def _switch_view(e: int):
        current_view.controls = views[e]
        animated_action_list.content = nothing if animated_action_list.content == action_list else action_list
        page.update()

    def switch_view(e: int):
        _switch_view(e)

    def when_resize():
        if page.width <= 600:
            action_list.min_extended_width = page.width
        else:
            action_list.min_extended_width = 400
        page.update()

    animated_action_list = ft.AnimatedSwitcher(
        action_list,
        transition=ft.AnimatedSwitcherTransition.FADE,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
        duration=500,
        reverse_duration=500 // 2
    )

    when_resize()

    nothing = ft.VerticalDivider()

    page.on_resize = lambda _: when_resize()

    def sidebar():
        # action_list.visible = not action_list.visible
        animated_action_list.content = nothing if animated_action_list.content == action_list else action_list
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
            ft.Row([animated_action_list, current_view], expand=True),
        ],
    )
    return view
