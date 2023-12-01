import flet as ft
from flet import ThemeMode
from router import router_func


def main(page: ft.Page):
    page.fonts = {
        "Harmony Sans": "./resource/HarmonyOS_Sans_SC_Regular.ttf"
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

        # This is old page route_str codes.
        # match route_str.route_str:
        #     case "/sys":
        #         page.views.append(sys.sys(page))
        #     case "/tools":
        #         page.views.append(small_tools_picker.small_tools_picker(page))
        #     case "/tools/random_school_id":
        #         page.views.append(random_school_id.random_school_id(page))
        #     case "/tools/timer":
        #         page.views.append(timer.timer(page))
        #     case "/tools/clock":
        #         page.views.append(clock.clock(page))
        #     case "/dbg":
        #         page.views.append(dbg.dbg(page))
        #     case "/setting":
        #         page.views.append(setting.setting(page))

        router_func(route.route, page)

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

# ft.app(target=main, port=7860, view=ft.AppView.WEB_BROWSER, assets_dir="resource")
ft.app(target=main, assets_dir="resource", name="ChatGPT")