import flet as ft
import zhipuai
import json
from widgets.MessageView import MessageView


def chat_glm(page: ft.Page):
    message_to_show = ft.ListView([
        MessageView("S", "SYSTEM", "# 欢迎使用全新的ChatGLM！\n目前仅支持SSE调用", page).get_widget()
    ], spacing=5, expand=1, auto_scroll=True)
    message_to_send = ft.TextField(label="提示词", hint_text="请输入提示词", multiline=True, max_lines=10, expand=True)
    history = []
    
    def refresh_api_info():
        try:
            zhipuai.api_key = page.client_storage.get("zhipu_chatglm_key")
        except Exception:
            page.snack_bar = ft.SnackBar(
                ft.Text("很抱歉，我们无法正常初始化ChatGLM API！\n可能是你没有设置API Key，请先前往设置界面进行设置。"),
                open=True,
                show_close_icon=True
            )
            page.update()
    
    def send_message():
        if not message_to_send.value == "":
            refresh_api_info()
            message_to_send.disabled = True
            _send_message()
            message_to_send.disabled = False
            message_to_send.value = ""
            page.update()
    
    def _send_message():
        history.append({"role": "user", "content": message_to_send.value})
        message_to_show.controls.append(MessageView("U", "USER", message_to_send.value, page).get_widget())
        page.update()
        
        response = zhipuai.model_api.sse_invoke(
            model="chatglm_turbo",
            prompt=history,
        )
        message_to_show.controls.append(MessageView("AI", "assistant", "", page).get_widget())
        page.update()
        
        reply = ""
        
        for event in response.events():
            if event.event == "add":
                reply = reply + event.data
                message_to_show.controls[-1] = MessageView("AI", "assistant", reply, page).get_widget()
                page.update()
            elif event.event == "error" or event.event == "interrupted":
                reply = reply + "\n```text\n[ERROR] 对话异常结束，可能是智谱AI的错误，也可能是触发违禁词了\n```"
                message_to_show.controls[-1] = MessageView("AI", "assistant", reply, page).get_widget()
                page.update()
                history.append({"role": "assistant", "content": reply})
            elif event.event == "finish":
                reply = reply + f"\n```text\n对话结束，本次对话消耗{str(json.loads(event.meta)['usage']['total_tokens'])}tokens\n```"
                message_to_show.controls[-1] = MessageView("AI", "assistant", reply, page).get_widget()
                message_to_send.disabled = False
                page.update()
                history.append({"role": "assistant", "content": reply})
            # else:
            #     ...
    
    def clear_history():
        history.clear()
        message_to_show.controls = [MessageView("S", "SYSTEM", "# 欢迎使用全新的ChatGLM！\n目前仅支持SSE调用", page).get_widget()]
        page.update()
    
    def set_api_info():
        def dialog_op(op_code: str):
            match op_code:
                case "save":
                    page.dialog.open = False
                    page.client_storage.set("zhipu_chatglm_key", page.dialog.content.controls[0].value)
                case "cancel":
                    page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("设置API Key"),
            content=ft.ListView([
                ft.TextField(label="API Key", hint_text="API Key", value=page.client_storage.get("zhipu_chatglm_key")),
            ], expand=1, spacing=5),
            actions=[
                ft.TextButton(text="保存", on_click=lambda _: dialog_op("save")),
                ft.TextButton(text="取消", on_click=lambda _: dialog_op("cancel"))
            ],
            open=True
        )
        page.update()
    
    view = ft.View("/chat-glm", [
        ft.AppBar(title=ft.Text("ChatGLM"),
                  actions=[ft.TextButton(text="设置API Key", on_click=lambda _: set_api_info())]),
        message_to_show,
        ft.Row([
            message_to_send,
            ft.IconButton(icon=ft.icons.SEND, tooltip="发送", on_click=lambda _: send_message()),
            ft.IconButton(icon=ft.icons.CLEAR, tooltip="清除上下文", on_click=lambda _: clear_history())
        ])
    ])
    
    return view
