import flet as ft
from flet import ThemeMode

from tools import DialogTools


def setting(page: ft.Page) -> ft.View:
    material3_switch = ft.Switch(label="使用新版本的Material Design（默认启用，仅在本次会话中保留）",
                                 on_change=lambda _: theme_change())
    dark_mode_switch = ft.Switch(label="暗色模式", on_change=lambda _: theme_change())
    openai_api_key = ft.TextField(label="API Key", on_change=lambda _: chatgpt_setting_change())
    openai_api_host = ft.TextField(label="API Host", prefix_text="https://", suffix_text="/v1",
                                   on_change=lambda _: chatgpt_setting_change())

    material3_switch.value = page.theme.use_material3
    dark_mode_switch.value = page.client_storage.get("dark_mode")
    openai_api_key.value = page.client_storage.get("openai_api_key")
    openai_api_host.value = page.client_storage.get("openai_api_host")

    def reset_openai_set():

        def close_dialog():
            page.dialog.open = False
            page.update()

        page.client_storage.remove("openai_api_host")
        page.client_storage.remove("openai_api_key")
        openai_api_key.value = ""
        openai_api_host.value = ""
        page.dialog = ft.AlertDialog(
            title=ft.Text("已清除"),
            content=ft.Text("最好刷新以应用更改"),
            actions=[ft.TextButton("好", on_click=lambda _: close_dialog())],
            modal=True
        )
        page.dialog.open = True
        page.update()

    view = ft.View("/setting", [
        # ft.AppBar(title=ft.Text("设置")),
        ft.ListView([
            ft.Text("界面设置", style=ft.TextThemeStyle.BODY_LARGE),
            material3_switch,
            dark_mode_switch,
            ft.Text("ChatGPT设置", style=ft.TextThemeStyle.BODY_LARGE),
            openai_api_host,
            openai_api_key,
            ft.TextButton(icon=ft.icons.REMOVE, text="重置ChatGPT设置", on_click=lambda _: reset_openai_set())
        ], expand=1, spacing=5),
        ft.TextButton(
            text="关于", icon=ft.icons.ACCOUNT_BOX, on_click=lambda _: about()
        )
    ])

    def theme_change():
        page.theme.use_material3 = material3_switch.value
        if dark_mode_switch.value:
            page.theme_mode = ThemeMode.DARK
        else:
            page.theme_mode = ThemeMode.LIGHT
        page.client_storage.set("dark_mode", dark_mode_switch.value)
        page.update()

    def chatgpt_setting_change():
        page.client_storage.set("openai_api_host", openai_api_host.value)
        page.client_storage.set("openai_api_key", openai_api_key.value)

    def about():
        dlg = ft.AlertDialog(title=ft.Text("关于", style=ft.TextThemeStyle.TITLE_LARGE),
                             content=ft.Text("作者：hinayand",
                                             style=ft.TextThemeStyle.BODY_LARGE),
                             actions=[
                                ft.TextButton("好的", on_click=lambda _:DialogTools.DialogTools(
                                    page).close_dlg(dlg))
        ])
        DialogTools.DialogTools(page).open_dlg(dlg)
        page.update()
    
    theme_change()

    return view
