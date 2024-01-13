import flet as ft


class NumberPicker(object):
    def __init__(self, page: ft.Page, max_number: int = 1, min_number: int = 1, label: str = None, default_value: int = None):
        self.widget = ft.Row()
        if default_value is None:
            self.text_field = ft.TextField(
                on_change=self._on_change, label=label, value=str(min_number), text_align=ft.TextAlign.CENTER)
        else:
            self.text_field = ft.TextField(
                on_change=self._on_change, label=label, value=str(default_value), text_align=ft.TextAlign.CENTER)
        self.max_num = max_number
        self.min_num = min_number
        self.page = page

    def _on_change(self, e):
        try:
            if int(e.control.value) > self.max_num:
                e.control.value = str(self.max_num)
            elif int(e.control.value) < self.min_num:
                e.control.value = str(self.min_num)
        except ValueError:
            e.control.value = str(self.min_num)
        finally:
            self.page.update()

    def _edit_value(self, num: int = 1):
        if (int(self.text_field.value) + num > self.max_num):
            self.text_field.value = str(self.max_num)
        elif (int(self.text_field.value) + num < self.min_num):
            self.text_field.value = str(self.min_num)
        else:
            self.text_field.value = str(int(self.text_field.value) + num)
        self.page.update()

    def get_value(self):
        return int(self.text_field.value)

    def get_widget(self):
        self.widget = ft.Row([
            ft.IconButton(icon=ft.icons.ADD,
                          on_click=lambda _: self._edit_value(num=1)),
            self.text_field,
            ft.IconButton(icon=ft.icons.REMOVE,
                          on_click=lambda _: self._edit_value(num=-1))
        ])
        return self.widget

    def disable(self):
        self.text_field.disabled = True
        self.widget.controls[0].disabled = True
        self.widget.controls[2].disabled = True
        self.page.update()

    def enable(self):
        self.text_field.disabled = False
        self.widget.controls[0].disabled = False
        self.widget.controls[2].disabled = False
        self.page.update()
