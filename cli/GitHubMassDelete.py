from github import Github
from github import Auth 
print("Provide token")
token = input().strip()
if not token:
    print("Token is required")
    exit(1)

auth = Auth.Token(token)
g = Github(auth=auth)
username = g.get_user()
allrepos = list(g.get_user().get_repos())
repos = [r for r in allrepos if getattr(getattr(r, "owner", None), "login", None) == username.login] 
for i, repo in enumerate(repos, start=1):
    flags = []
    if getattr(repo, "private", False):
        flags.append("private")
    if getattr(repo, "archived", False):
        flags.append("archived")
    if getattr(repo, "fork", False):
        flags.append("fork")
    flag_str = f" ({', '.join(flags)})" if flags else ""
    print(f"{i}. {repo.full_name} ({flag_str})")

selection = input("\nSelect repos (comma separated): ").strip()
    
for part in selection.split(","):
    part = part.strip()
    if not part.isdigit():
        print("invalid\n")
        continue
    index = int(part) -1
    if index < 0 or index >= len(repos):
        print("No such repo\n")
        continue
    repo = repos[index]
    confirm = input(f"Are you SURE you want to delete {repo.full_name}? (y/N): ").strip().lower()
    if confirm == "y":
        print(f"Deleting {repo.full_name}...")
        repo.delete()
        print(f"Deleted {repo.full_name}")
    else:
        print(f"Skipped {repo.full_name}")

g.close()