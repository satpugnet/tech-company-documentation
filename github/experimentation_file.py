from github_interface.github_interface import GithubInterface

g = GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")
# for repo in g.get_repos():
#     print(repo.get_full_name())
#     print(repo.get_root_files()[0].get_type())
    # print(g.get_repo_file(repo.full_name, "README.md"))

repo = g.get_repo("saturnin13/tech-company-documentation")

# print(repo
#       .get_file("github/github_interface/github_interface.py")
#       .get_lines(start=3, stop=5))


## Getting last commit file change
# self.__repo_object.get_commit(sha="ba419d2c64f3c813aa1823705e50f22a2fd94cbb")

commit_files = repo.get_commit_files("master", sha="ba419d2c64f3c813aa1823705e50f22a2fd94cbb")

for file in commit_files:
      print(file.get_path())

# test = repo.get_commit_files("master").files[0].filename
# print(dir(test))
# print(test)
#
# print(repo.get_file(test).get_lines())