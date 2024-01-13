import flet as ft
from pages import index, setting, chatgpt, chat_gemini, chat_glm


def router_func(route_str: str, page: ft.Page):
    page.views.append(index.index(page))
    
    if route_str.split("/")[1] == "":
        pass
    elif route_str.split("/")[1] == "setting":
        page.views.append(setting.setting(page))
    elif route_str.split("/")[1] == "chatgpt":
        page.views.append(chatgpt.chatgpt(page))
    elif route_str.split("/")[1] == "chat-gemini":
        page.views.append(chat_gemini.chat_gemini(page))
    elif route_str.split("/")[1] == "chat-glm":
        page.views.append(chat_glm.chat_glm(page))
