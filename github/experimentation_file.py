from github_interface.github_interface import GithubInterface

g = GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")
# for repo in g.get_repos():
#     print(repo.get_full_name())
#     print(repo.get_root_files()[0].get_type())
    # print(g.get_repo_file(repo.full_name, "README.md"))

print(g.get_repo("saturnin13/tech-company-documentation")
      .get_file("src/github_interface/github_interface.py")
      .get_lines(start=3, stop=5))