import flet as ft
import json

from widgets.ModelView import ModelView


def models(page: ft.Page):
    model_list_view = ft.ListView(expand=1, spacing=5)
    with open("./resource/models.json", "r", encoding="utf-8") as f:
        model_list = json.load(f)
    for model in model_list:
        model_list_view.controls.append(ModelView(model_name=model["model_name"],
                                                  model_description=model["model_description"],
                                                  model_page_path=model["model_page_path"],
                                                  current_page=page))
    view = ft.View("/models", [
        ft.Text("更多模型", style=ft.TextThemeStyle.TITLE_LARGE),
        model_list_view
    ])
    return view
