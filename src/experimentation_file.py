from github_interface.github_interface import GithubInterface

g = GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")
for repo in g.get_repos():
    print(repo.full_name)
    # print(g.get_repo_file(repo.full_name, "README.md"))

print()
print(g.get_repo_file("saturnin13/tech-company-documentation", "src/github_interface/github_interface.py"))