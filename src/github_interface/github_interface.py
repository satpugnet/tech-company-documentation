from github import Github, UnknownObjectException
import base64

class GithubInterface:

    def __init__(self, access_token):
        self.github_account = Github(access_token)

    def get_repo_file(self, repo_name, file_name):
        repo = self.github_account.get_repo(repo_name)

        try:
            encoded_contents = repo.get_contents(file_name)
        except UnknownObjectException:
            print("File " + file_name + " not found in " + repo_name)
            return

        contents = base64.b64decode(encoded_contents.content).decode("utf-8")
        return contents

    def get_repos(self):
        return self.github_account.get_user().get_repos()

