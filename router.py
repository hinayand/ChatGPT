import flet as ft
from pages import index, setting, chatgpt


def router_func(route_str: str, page: ft.Page):
    page.on_resize = lambda _: ...
    page.views.append(index.index(page))
    
    if route_str.split("/")[1] == "":
        pass
    elif route_str.split("/")[1] == "setting":
        page.views.append(setting.setting(page))
    elif route_str.split("/")[1] == "chatgpt":
        page.views.append(chatgpt.chatgpt(page))
