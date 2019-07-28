import datetime
import json
import sys
import time

from github import Github, GithubIntegration, BadCredentialsException

from github_interface.git.git_diff_parser import GitDiffParser
from github_interface.interface import GithubInterface
from utils.json.custom_json_encoder import CustomJsonEncoder

# User.upsert_installation("saturnin13", "12342", "445sf475", "6")

github_account = Github("aed389484d26dd38496bea60762d699a33d37b29")

user = github_account.get_user()
print(user)

def decode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)

print(decode_flask_cookie("test", ".eJwNw20KgCAMANC7eII557QuE_tQiEAj-hfdvR68J2ynXDLm7ts9jzbCGpolL-qV0RlTzMDaBXJlSFG0VyEjbFQwcyyLuSlBlyr_okAY3g-RwhmK.XTpayQ.xL26gkdSVnilRz8srBTeqW8o2rU"))
print("la")

raw_patch = "@@ -1,4 +1,5 @@\n" \
" 1\n"  \
"+1bis\n" \
"+2\n" \
" 3\n" \
" 4\n" \
"@@ -37,3 +38,4 @@ hello world\n" \
" hello world\n" \
" hello world\n" \
" hello world\n" \
"+hello world"
parser = GitDiffParser(raw_patch)
print(parser.calculate_updated_line_range(1, 6))


try:
        g = Github("etufwf")
        g.get_rate_limit()
except BadCredentialsException as e:
        print("error printed")

# GITHUB_APP_IDENTIFIER = 33713
# INSTALLATION_ID = 1191487

with open('ressources/github-private-key.pem', 'rb') as file:
    private_key = file.read()

# g2 = GitHub()
# g2.login_as_app_installation(private_key, GITHUB_APP_IDENTIFIER, INSTALLATION_ID)
#
# # print(dir(g2.repository("saturnin13", "tech-company-documentation").file_contents("")))
# print(g2.repository("saturnin13", "tech-company-documentation").directory_contents(""))
# print(dir(g2.repository("saturnin13", "tech-company-documentation").file_contents("Makefile")))
# print(base64.b64decode(g2.repository("saturnin13", "tech-company-documentation").file_contents("Makefile").content))
# print(g2.all_repositories())
# # for repo in g2.all_repositories():
# #         print(dir(repo))

integration = GithubIntegration(str(GITHUB_APP_IDENTIFIER), private_key)
print(integration.create_jwt())
print(datetime.datetime.now())
print("access token: " + str(integration.get_access_token(INSTALLATION_ID).token))
print("access token expire time: " + str(integration.get_access_token(INSTALLATION_ID).expires_at))

access_token = integration.get_access_token(INSTALLATION_ID).token
access_token = "v1.3de1f74b2ac2a858a7da17cb17f6bdddc457de94"

g2 = GithubInterface(access_token=access_token, is_user_access_token=False)
# root_directory = g2.get_repo("saturnin13/tech-company-documentation").root_directory
# root_directory.load_subfiles()
# print(root_directory.subfiles["backend"])
# root_directory.subfiles["backend"].load_subfiles()
# print(root_directory.subfiles["backend"].subfiles["web_server.py"].content)
print("laaaaaaaaaaaaaaaaaaaaaa")
for repo in g2.get_repos():
        print(repo.full_name)
print(g2.get_installation(INSTALLATION_ID))
print()



start = time.time()

# repo_name = "saturnin13/tech-company-documentation"
repo_name = "louisblin/LondonHousingForecast-Backend"
# repo_name = "paulvidal/1-week-1-tool"

g = GithubInterface(access_token="v1.3de1f74b2ac2a858a7da17cb17f6bdddc457de94", is_user_access_token=True)
repo = g.get_repo(repo_name)
repo_root = repo.root_directory

print("laaaaa")
print(repo.get_commits())

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
        print(commit_file.has_path_changed)
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

# GITHUB_WEBHOOK_SECRET = SatPaulDocumentation
# GITHUB_APP_IDENTIFIER = 33713