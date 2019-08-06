from github_interface.abstract_github_interface import AbstractGithubInterface


class AuthentificatedGithubInterface(AbstractGithubInterface):

    @staticmethod
    def get_repo(user_login, installation_account_login, repo_name):
        repo = super().get_repo(installation_account_login, repo_name)
        print("The enrichment from AnotherSubclass")

    @staticmethod
    def get_repo_without_user_authentification(installation_account_login, repo_name):
        repo = super().get_repo(installation_account_login, repo_name)
        print("The enrichment from AnotherSubclass")

    @staticmethod
    def get_repos(user_login, installation_account_login):
        repos = super().get_repos(user_login, installation_account_login)

    @staticmethod
    def get_user_installations(user_login):
        installations = super().get_user_installations(user_login)
        return FilteredGithubInterface.__filter_user_installations(installations)

    @staticmethod
    def __filter_repo(installations):
        pass

    @staticmethod
    def __filter_repos(installations):
        pass

    @staticmethod
    def __filter_user_installations(installations):
        pass

