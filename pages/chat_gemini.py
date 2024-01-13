import traceback

import flet as ft
import requests

from widgets.MessageView import MessageView


def chat_gemini(page: ft.Page):
    message_to_show = ft.ListView([
        MessageView("S", "SYSTEM", "# 欢迎使用全新的Gemini！", page).get_widget()
    ], spacing=5, expand=1, auto_scroll=True)
    message_to_send = ft.TextField(label="提示词", hint_text="请输入提示词", multiline=True, max_lines=10, expand=True)
    history = []
    api_key = ""
    api_url = ""

    def refresh_api_info():
        nonlocal api_key, api_url
        try:
            api_key = page.client_storage.get("google_gemini_key")
            api_url = page.client_storage.get("google_gemini_url")
        except Exception:
            page.snack_bar = ft.SnackBar(
                ft.Text("很抱歉，我们无法正常初始化Google API！\n可能是你没有设置API Key，请先前往设置界面进行设置。"),
                open=True,
                show_close_icon=True
            )
            page.update()

    def _send_message():
        def generate_response():
            refresh_api_info()
            nonlocal api_key, api_url
            url = api_url + api_key
            header = {
                "Content-Type": "application/json"
            }
            data = {
                "contents": history
            }
            request = requests.post(url=url, headers=header, json=data)

            if request.status_code == 200:
                return request.json()["candidates"][0]["content"]
            else:
                return history

        try:
            nonlocal history
            message_to_show.controls.append(
                MessageView("U", "USER", message_to_send.value, page).get_widget()
            )
            page.update()
            history.append({
                "role": "user",
                "parts": [{
                    "text": message_to_send.value
                }]
            })
            history.append(generate_response())
            print(history)
            message_to_show.controls.append(
                MessageView("AI", "GEMINI", history[-1]["parts"][-1]["text"], page).get_widget()
            )
            page.update()


        except Exception:
            page.snack_bar = ft.SnackBar(
                ft.Text("我们无法向Google正常发送请求！"),
                open=True,
                show_close_icon=True
            )
            print(str(traceback.format_exc()))
            page.update()

    def send_message():
        if not message_to_send.value == "":
            refresh_api_info()
            message_to_send.disabled = True
            _send_message()
            message_to_send.disabled = False
            message_to_send.value = ""
            page.update()

    def clear_history():
        history.clear()
        message_to_show.controls = [MessageView("S", "SYSTEM", "# 欢迎使用全新的Gemini！", page).get_widget()]
        page.update()

    def set_api_info():
        def dialog_op(op_code: str):
            match op_code:
                case "save":
                    page.dialog.open = False
                    page.client_storage.set("google_gemini_key", page.dialog.content.controls[0].value)
                    page.client_storage.set("google_gemini_url", page.dialog.content.controls[1].value)
                case "cancel":
                    page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("设置API Key"),
            content=ft.ListView([
                ft.TextField(label="API Key", hint_text="API Key", value=page.client_storage.get("google_gemini_key")),
                ft.TextField(label="API URL", hint_text="API URL", value=page.client_storage.get("google_gemini_url"))
            ], expand=1, spacing=5),
            actions=[
                ft.TextButton(text="保存", on_click=lambda _: dialog_op("save")),
                ft.TextButton(text="取消", on_click=lambda _: dialog_op("cancel"))
            ],
            open=True
        )
        page.update()

    view = ft.View("/chat-gemini", [
        ft.AppBar(title=ft.Text("ChatGemini"),
                  actions=[ft.TextButton(text="设置API Key", on_click=lambda _: set_api_info())]),
        message_to_show,
        ft.Row([
            message_to_send,
            ft.IconButton(icon=ft.icons.SEND, tooltip="发送", on_click=lambda _: send_message()),
            ft.IconButton(icon=ft.icons.CLEAR, tooltip="清除上下文", on_click=lambda _: clear_history())
        ])
    ])

    return view
