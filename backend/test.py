import json
import sys
import time

from github_interface.interface import GithubInterface
from utils.json.custom_json_encoder import CustomJsonEncoder

start = time.time()

# repo_name = "saturnin13/tech-company-documentation"
repo_name = "louisblin/LondonHousingForecast-Backend"
# repo_name = "paulvidal/1-week-1-tool"

g = GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")
repo = g.get_repo(repo_name)
repo_root = repo.root_directory

print("It took " + str(time.time() - start) + " to download " + repo_name)

start = time.time()
print(sys.getsizeof(json.dumps(repo_root, cls=CustomJsonEncoder)))
print("It took " + str(time.time() - start) + " to dump the json")

# print(repo_root.subfiles["backend"])

# print(repo_root.subfiles["frontend"].subfiles["README.md"].content)

# for key, file in repo_root.subfiles["backend"].subfiles.items():
#         print(file.path)



# print(g.get_repos()[18].get_directory_or_file("api").get_content())

# for file in g.get_repos()[18].root_directory:
#         print(file.get_path())

# for repo in g.get_repos():
#     print(repo.full_name)
#     print(g.get_repo(repo.full_name))


# print(repo
#       .get_file("website/src/App.vue")
#       .get_lines())


## Getting last commit file change
# self.__repo_object.get_commit(sha="ba419d2c64f3c813aa1823705e50f22a2fd94cbb")

commit_files = repo.get_commit_files("master", sha=None)

for commit_file in commit_files:
        print()
        print(commit_file.calculate_updated_line_range(3, 50))
        print(commit_file.has_path_changed())
        print(commit_file.previous_path)
        print(commit_file.path)



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

# patch = "@@ -1,6 +1,6 @@\n" \
#         " #!/usr/bin/env bash\n" \
#         " \n" \
#         "-apt-get update\n" \
#         "+sudo apt-get update\n" \
#         " \n" \
#         " wget -qO- https://raw.githubusercontent.com/...\n" \
#         " \n" \
#         "@@ -9,3 +9,4 @@\n" \
#         " source /home/vagrant/.profile\n" \
#         " \n" \
#         " nvm install node\n" \
#         "+nvm alias default node\n"
#
# patch2 = "@@ -1,6 +1,6 @@\n" \
#         " #!/usr/bin/env bash\n" \
#         " e\n" \
#         " apt-get update\n" \
#         " sudo apt-get update\n" \
#         " e\n" \
#         " wget -qO- https://raw.githubusercontent.com/...\n" \
#         " e\n" \
#         "@@ -9,3 +9,4 @@\n" \
#         " source /home/vagrant/.profile\n" \
#         " e\n" \
#         " nvm install node\n" \
#         " nvm alias default node\n"
#
# diff_parser = GitDiffParser(patch2)
#
# print(diff_parser.calculate_updated_line_range(8, 11))
#
# #TODO check why the second part is not being taken into account by the range (fix for diff_parser.calculate_updated_line_range(2, 11))

