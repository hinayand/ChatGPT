import flet as ft


class DialogTools(object):
    def __init__(self, page: ft.Page):
        self.page = page

    def open_dlg(self, dlg: ft.AlertDialog):
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close_dlg(self, dlg: ft.AlertDialog):
        dlg.open = False
        self.page.update()
