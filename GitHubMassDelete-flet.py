import flet as ft
from github import Github, Auth

def main(page: ft.Page):
    page.title = "GitHub Mass Delete"
    page.scroll = ft.ScrollMode.AUTO

    tokenfield = ft.TextField(label="GitHub Token", password=True, width=400)
    loadbutton = ft.ElevatedButton(text="Load Repos")
    deletebutton = ft.ElevatedButton(text="Delete Selected Repos", disabled=True)
    output = ft.Text()
    repolist = ft.Column()
    repos = []
# function start
    def loadrepos(e):
        token = tokenfield.value.strip()
        if not token:
            output.value = "Token is required"
            page.update()
            return
        try:
            auth = Auth.Token(token)
            g = Github(auth=auth)
            user = g.get_user()
            allrepos = list(g.get_user().get_repos())
            owned = [r for r in allrepos if r.owner.login == user.login]
        except Exception as ex:
            output.value = f"Error loading repos: {ex}"
            page.update()
            return
    # function end

        repos.clear()
        repolist.controls.clear()
# private/archived/fork/owned logic
# for loop start
        for repo in owned:
            flags = []
            if repo.private:
                flags.append("private")
            if repo.archived:
                flags.append("archived")
            if repo.fork:
                flags.append("fork")
            
            label = f"{repo.full_name} ({', '.join(flags)})" if flags else repo.full_name
            cb = ft.Checkbox(label=label)
            cb.data = repo
            repos.append(cb)
            repolist.controls.append(cb)
# for loop end
        deletebutton.disabled = False
        output.value = f"Loaded {len(owned)} repos."
        page.update()
# function start
    
# function start 
    def deleterepos(e):
        selected = [cb.data for cb in repos if cb.value]
        if not selected:
            output.value = "No repos selected for deletion."
            page.update()
            return
        def confirmdelete(dialog):
            deleted = 0
            for repo in selected:
                try:
                    repo.delete()
                    deleted += 1
                    output.value = f"Deleted {repo.full_name}"
                except Exception as ex:
                    output.value = f"Error deleting {repo.full_name}: {ex}"
            output.value += f"Deletion complete. Total deleted: {deleted}"
            page.dialog = None
            page.update()

        page.dialog = ft.AlertDialog(
            modal = True,
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(f"Are you SURE you want to delete {len(selected)} repos?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.dialog.close()),
                ft.TextButton("Delete", on_click=lambda e: confirmdelete(page.dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            
        )
        page.dialog.open = True
        page.update()

    deletebutton.on_click = deleterepos
    loadbutton.on_click = loadrepos
# flutter layout
    page.add(
        ft.Column(
            [
                tokenfield,
                ft.Row([loadbutton, deletebutton], spacing=10),
                repolist,
                output,
            ],
            spacing=10,
        )
    )
# flutter run
ft.app(target=main)