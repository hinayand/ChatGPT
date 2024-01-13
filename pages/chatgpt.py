import json
import os
import threading
import traceback

import flet as ft
import openai
import requests

from widgets import MessageView

with open("resource/System Prompt.md", encoding="utf-8", mode="r") as f:
    default_sys_prompt = f.read()


def chatgpt(page: ft.Page):
    if (
        page.client_storage.get("system_prompt") is None
        or page.client_storage.get("system_prompt") == ""
    ):
        messages = [{"role": "system", "content": default_sys_prompt}]
    else:
        messages = [
            {"role": "system", "content": page.client_storage.get(
                "system_prompt")}
        ]
    messages_to_show = ft.ListView(spacing=5, expand=1, auto_scroll=True)
    messages_to_show.controls.append(
        MessageView.MessageView("S", "SYSTEM", "# 欢迎使用", page).get_widget()
    )

    message_to_send = ft.TextField(
        label="提示词", expand=True, multiline=True, hint_text="请输入提示词"
    )

    model_will_use = ft.Dropdown(label="模型选择", options=[], expand=True)

    def refresh_api_info():
        """
        刷新API信息函数
        """

        def get_models():
            """
            获取模型信息函数
            """

            print(openai.api_base)  # 打印API基础地址
            try:
                # 发送GET请求获取模型信息
                models = requests.get(
                    openai.api_base + "/models",
                    headers={"Authorization": "Bearer " + openai.api_key},
                ).json()
                print(models)  # 打印模型信息
                model_will_use.options.clear()  # 清空下拉菜单选项
                for model in models["data"]:
                    model_will_use.options.append(
                        ft.dropdown.Option(model["id"], model["id"])
                    )  # 添加模型选项到下拉菜单
                page.update()  # 更新页面
            except:
                try:
                    # 发送GET请求获取模型信息
                    models = requests.get(
                        openai.api_base + "/models",
                        headers={"Authorization": "Bearer " + openai.api_key},
                    ).json()
                    print(models)  # 打印模型信息
                    model_will_use.options.clear()  # 清空下拉菜单选项
                    for model in models:
                        model_will_use.options.append(
                            ft.dropdown.Option(model["id"], model["id"])
                        )  # 添加模型选项到下拉菜单
                    page.update()  # 更新页面
                except:
                    def close_dialog():
                        page.dialog.open = False
                        page.update()

                    # 弹出对话框提示无法获取API模型信息
                    page.dialog = ft.AlertDialog(
                        title=ft.Text("我们无法获取你的API模型信息！"),
                        content=ft.ListView([ft.Text(traceback.format_exc())]),
                        actions=[ft.TextButton("好的", on_click=lambda _: close_dialog())]
                    )
                    page.dialog.open = True  # 打开对话框
                    page.update()  # 更新页面

        try:
            openai.api_key = page.client_storage.get("openai_api_key")  # 获取存储的API密钥
            openai.api_base = (
                "http://" +
                page.client_storage.get("openai_api_host") + "/v1"
            )  # 根据API主机名设置API基础地址
            get_models()  # 调用获取模型信息函数
        except Exception:
            print(traceback.format_exc())  # 打印异常信息
            if (
                os.environ.get("OPENAI_API_KEY") is not None
                and os.environ.get("OPENAI_API_HOST") is not None
            ):
                openai.api_key = os.environ.get("OPENAI_API_KEY")  # 获取环境变量中的API密钥
                openai.api_base = "http://" + \
                    os.environ.get("OPENAI_API_HOST") + "/v1"  # 获取环境变量中的API基础地址
                get_models()  # 调用获取模型信息函数
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text(
                        "请在环境变量中设置OPENAI_API_KEY和OPENAI_API_HOST，又或者在设置中设置API和API Key\n当然，也请检查您设置的API地址是否有效、密钥是否有效"
                    ),
                    show_close_icon=True,
                )  # 显示提示信息
                page.snack_bar.open = True  # 打开提示信息
                page.update()  # 更新页面


    refresh_api_info()

    def _send_msg():
        refresh_api_info()

        def close_dialog():
            page.dialog.open = False
            page.update()

        reply = ""

        # 当发生错误时，对话框的Action
        actions_list = [
            ft.TextButton("我知道了", on_click=lambda _: close_dialog()),
            ft.TextButton("复制错误日志", on_click=lambda _: page.set_clipboard(page.dialog.content.controls[0].value))
        ]

        try:
            nonlocal messages_to_show
            messages.append(
                {"role": "user", "content": str(message_to_send.value)})
            response = openai.ChatCompletion.create(
                model=model_will_use.value, messages=messages, stream=True
            )
            messages_to_show.controls.append(
                MessageView.MessageView("R", "ROBOT", reply, page).get_widget()
            )
            for chunk in response:
                try:
                    message_to_send.disabled = True
                    reply += chunk.choices[0].delta.content
                    messages_to_show.controls[-1] = MessageView.MessageView(
                        "R", "ROBOT", reply, page
                    ).get_widget()
                    page.update()
                except AttributeError:
                    messages.append(
                        {"role": "assistant", "content": str(reply)})
                    message_to_send.value = ""
                    message_to_send.disabled = False
                    page.update()
                    print(messages)
        except openai.error.APIError:
            page.dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.ListView(
                    [
                        ft.Text(
                            "很抱歉，出错了！\n您的OpenAI API返回了一个错误！\n" + traceback.format_exc(),
                            expand=True,
                        )
                    ],
                    expand=True,
                ),
                actions=actions_list,
                modal=True,
            )
            page.dialog.open = True
            page.update()
        except openai.error.InvalidRequestError:
            page.dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.ListView(
                    [
                        ft.Text(
                            "很抱歉，出错了！\n您可能没有选择模型又或者是你的API不支持你选择的模型！\n"
                            + traceback.format_exc(),
                            expand=True,
                        )
                    ],
                    expand=True,
                ),
                actions=actions_list,
                modal=True,
            )
            page.dialog.open = True
            page.update()
        except openai.error.APIConnectionError:
            page.dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.ListView(
                    [
                        ft.Text(
                            "很抱歉，出错了！\n您的OpenAI API可能格式有误或不存在，请检查您的API地址。\n如果API地址确认无误，但您仍然能看到这个错误窗口，那么请询问API提供者！\n"
                            + traceback.format_exc(),
                            expand=True,
                        )
                    ],
                    expand=True,
                ),
                actions=actions_list,
                modal=True,
            )
            page.dialog.open = True
            page.update()
        except openai.error.AuthenticationError:
            page.dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.ListView(
                    [
                        ft.Text(
                            "很抱歉，出错了！\n您的API Key可能有误、无效、不存在，又可能是API提供者跑路了。\n如果API Key确认无误，但您仍然能看到这个错误窗口，那么请询问API提供者！\n"
                            + traceback.format_exc(),
                            expand=True,
                        )
                    ],
                    expand=True,
                ),
                actions=actions_list,
                modal=True,
            )
            page.dialog.open = True
            page.update()
        except Exception:
            page.dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.ListView(
                    [
                        ft.Text(
                            "很抱歉，出错了！\n这可能是由代码产生的错误，如果您见到了这个弹窗，请截图发给开发者！\n"
                            + str(traceback.format_exc()),
                            expand=True,
                        )
                    ],
                    expand=True,
                ),
                actions=actions_list,
                modal=True,
            )
            page.dialog.open = True
            page.update()
        finally:
            message_to_send.disabled = False
            page.update()

    def send_message():
        if not message_to_send.value == "":
            threading.Thread(target=_send_msg).start()
            messages_to_show.controls.append(
                MessageView.MessageView(
                    "U", "USER", message_to_send.value, page
                ).get_widget()
            )
            page.update()

    def clear_context():
        refresh_api_info()
        nonlocal messages, messages_to_show
        if (
            page.client_storage.get("system_prompt") is None
            or page.client_storage.get("system_prompt") == ""
        ):
            messages = [{"role": "system", "content": default_sys_prompt}]
        else:
            messages = [
                {"role": "system", "content": page.client_storage.get(
                    "system_prompt")}
            ]
        messages_to_show.controls = []
        messages_to_show.controls.append(
            MessageView.MessageView("S", "SYSTEM", "# 欢迎使用", page).get_widget()
        )
        page.update()

    def set_system_prompt():
        def on_dialog_ok():
            nonlocal messages
            page.client_storage.set(
                "system_prompt", system_prompt_will_use.value)
            page.dialog.open = False
            if (
                page.client_storage.get("system_prompt") is None
                or page.client_storage.get("system_prompt") == ""
            ):
                messages = [{"role": "system", "content": default_sys_prompt}]
            else:
                messages = [
                    {
                        "role": "system",
                        "content": page.client_storage.get("system_prompt"),
                    }
                ]
            messages_to_show.controls = [
                MessageView.MessageView(
                    "S", "SYSTEM", "# 欢迎使用", page).get_widget()
            ]
            refresh_api_info()
            page.update()

        def on_dialog_cancel():
            page.dialog.open = False
            page.update()

        system_prompt_will_use = ft.TextField(
            label="提示词", value=page.client_storage.get("system_prompt"), multiline=True
        )
        page.dialog = ft.AlertDialog(
            title=ft.Text("设置系统提示词"),
            content=system_prompt_will_use,
            actions=[
                ft.TextButton("完成", on_click=lambda _: on_dialog_ok()),
                ft.TextButton("取消", on_click=lambda _: on_dialog_cancel()),
            ],
        )
        page.dialog.open = True
        page.update()

    def export_chat():
        page.set_clipboard(json.dumps(messages))
        page.snack_bar = ft.SnackBar(
            content=ft.Text("已经将聊天数据复制到了剪贴板"), show_close_icon=True
        )
        page.snack_bar.open = True
        page.update()

    def import_chat():
        def action_import_chat():
            nonlocal messages
            messages = json.loads(page.dialog.content.value)
            messages_to_show.controls.clear()
            messages_to_show.controls.append(
                MessageView.MessageView(
                    "S", "SYSTEM", "# 欢迎使用", page).get_widget()
            )

            page.dialog.open = False

            try:
                for i in messages:
                    if i["role"] == "system":
                        continue
                    else:
                        match i["role"]:
                            case "user":
                                messages_to_show.controls.append(
                                    MessageView.MessageView(
                                        "U", "USER", i["content"], page
                                    ).get_widget()
                                )
                            case "assistant":
                                messages_to_show.controls.append(
                                    MessageView.MessageView(
                                        "R", "ROBOT", i["content"], page
                                    ).get_widget()
                                )
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("导入成功！"), show_close_icon=True
                )
                page.snack_bar.open = True
                page.update()
            except:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("导入失败！"), show_close_icon=True
                )
                page.snack_bar.open = True
                page.update()

        def action_exit():
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("导入聊天数据"),
            content=ft.TextField(
                multiline=True, min_lines=1, hint_text="请将聊天数据粘贴至此", label="聊天数据"
            ),
            actions=[
                ft.TextButton("导入", on_click=lambda _: action_import_chat()),
                ft.TextButton("取消", on_click=lambda _: action_exit()),
            ],
        )
        page.dialog.open = True
        page.update()

    view = ft.View(
        "/chatgpt",
        controls=[
            ft.Row(
                [
                    model_will_use,
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="设置预设文本", on_click=lambda _: set_system_prompt()),
                            ft.PopupMenuItem(
                                text="刷新API信息", on_click=lambda _: refresh_api_info()),
                            ft.PopupMenuItem(text="导出",
                                             icon=ft.icons.IMPORT_EXPORT,
                                             on_click=lambda _: export_chat()),
                            ft.PopupMenuItem(text="导入",
                                             icon=ft.icons.IMPORT_EXPORT_ROUNDED,
                                             on_click=lambda _: import_chat())
                        ], tooltip="打开二级菜单"
                    )
                ]
            ),
            messages_to_show,
            ft.Row(
                [
                    message_to_send,
                    ft.IconButton(
                        icon=ft.icons.SEND, on_click=lambda _: send_message()
                    ),
                    ft.IconButton(
                        icon=ft.icons.CLEAR, on_click=lambda _: clear_context()
                    ),
                ]
            )
        ],
    )

    return view
