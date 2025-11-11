import flet as ft

def main(page: ft.Page):
    def show_dialog(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Test Dialog"),
            content=ft.Text("This should pop up!"),
            actions=[ft.TextButton("Close", on_click=lambda e: page.dialog.close())],
            modal=True
        )
        page.dialog.open = True
        page.update()

    page.add(ft.ElevatedButton("Show Dialog", on_click=show_dialog))

ft.app(target=main, view=ft.WEB_BROWSER)
