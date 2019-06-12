import re

from github_interface.git.git_diff_parser import GitDiffParser
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

# print(commit_files[0].calculate_updated_line_range(3, 7))



# print(commit_files[2].get_lines())

# for file in commit_files:
#       print(file.get_path())

# test = repo.get_commit_files("master").files[0].filename
# print(dir(test))
# print(test)
#
# print(repo.get_file(test).get_lines())

# test = "@@ -1,6 +1,6 @@"
# title_search = re.search('@@ -(\d+),(\d+) \\+(\d+),(\d+) @@', test)
#
# print(title_search.group(1))
# print(title_search.group(2))
# print(title_search.group(3))
# print(title_search.group(4))

# test = "@@ nopifnainfap yf@@ knpna@@\n "
#
# print([match.start() for match in re.finditer('@@ ', test)])
# print(test[0:18])

patch = "@@ -1,6 +1,6 @@\n" \
        " #!/usr/bin/env bash\n" \
        " \n" \
        "-apt-get update\n" \
        "+sudo apt-get update\n" \
        " \n" \
        " wget -qO- https://raw.githubusercontent.com/...\n" \
        " \n" \
        "@@ -9,3 +9,4 @@\n" \
        " source /home/vagrant/.profile\n" \
        " \n" \
        " nvm install node\n" \
        "+nvm alias default node\n"

patch2 = "@@ -1,6 +1,6 @@\n" \
        " #!/usr/bin/env bash\n" \
        " e\n" \
        " apt-get update\n" \
        " sudo apt-get update\n" \
        " e\n" \
        " wget -qO- https://raw.githubusercontent.com/...\n" \
        " e\n" \
        "@@ -9,3 +9,4 @@\n" \
        " source /home/vagrant/.profile\n" \
        " e\n" \
        " nvm install node\n" \
        " nvm alias default node\n"

diff_parser = GitDiffParser(patch2)

print(diff_parser.calculate_updated_line_range(8, 11))

#TODO check why the second part is not being taken into account by the range (fix for diff_parser.calculate_updated_line_range(2, 11))

