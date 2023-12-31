import os

import flet as ft
from flet import ThemeMode

from router import router_func


def main(page: ft.Page):
    page.fonts = {
        "Harmony Sans": "./resource/HarmonyOS_Sans_SC_Regular.ttf",
        "Noto Mono": "./resource/NotoSansMonoCJKsc-Regular.otf"
    }
    page.theme = ft.Theme(use_material3=True, font_family="Harmony Sans")
    if page.client_storage.get("dark_mode"):
        page.theme_mode = ThemeMode.DARK
    else:
        page.theme_mode = ThemeMode.LIGHT

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def route_change(route: ft.RouteChangeEvent):
        # TODO: Add Route Change Function
        page.views.clear()

        # This is old current_page route_str codes.
        # match route_str.route_str:
        #     case "/sys":
        #         current_page.views.append(sys.sys(current_page))
        #     case "/tools":
        #         current_page.views.append(small_tools_picker.small_tools_picker(current_page))
        #     case "/tools/random_school_id":
        #         current_page.views.append(random_school_id.random_school_id(current_page))
        #     case "/tools/timer":
        #         current_page.views.append(timer.timer(current_page))
        #     case "/tools/clock":
        #         current_page.views.append(clock.clock(current_page))
        #     case "/dbg":
        #         current_page.views.append(dbg.dbg(current_page))
        #     case "/setting":
        #         current_page.views.append(setting.setting(current_page))

        router_func(route.route, page)

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


try:
    ft.app(target=main, port=int(os.environ.get("PORT")), view=ft.AppView.WEB_BROWSER, assets_dir="resource")
except TypeError:
    ft.app(target=main, port=7860, view=ft.AppView.WEB_BROWSER, assets_dir="resource")
# ft.app(target=main, assets_dir="resource")
