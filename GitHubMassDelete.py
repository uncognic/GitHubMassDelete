from github import Github
from github import Auth 
print("Provide token")
token = input().strip()
if not token:
    print("Token is required")
    exit(1)

auth = Auth.Token(token)
g = Github(auth=auth)

repos = list(g.get_user().get_repos())
for repo in repos:
    flags = []
    if getattr(repo, "private", False):
        flags.append("private")
    if getattr(repo, "archived", False):
        flags.append("archived")
    if getattr(repo, "fork", False):
        flags.append("fork")
    flag_str = f" ({', '.join(flags)})" if flags else ""
    print(f"- {repo.full_name}{flag_str}")
g.close()