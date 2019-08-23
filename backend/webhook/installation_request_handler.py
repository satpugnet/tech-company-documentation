from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from github_interface.interfaces.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.collection_clients.clients.db_github_file_client import DbGithubFileClient
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from tools.file_system_interface import FileSystemInterface


class InstallationRequestHandler:
    def __init__(self, github_account_login):
        self.__github_account_login = github_account_login

    # TODO: refactor so that the 2 distinct use of this enact (inserting token and then inserting file)
    #  are separated in different function/class
    # TODO: add a flag in documents reference stating when an installation has been deleted and therefore no access to the ref
    def enact_installation_deleted_event(self):
        DbGithubInstallationClient().remove(self.__github_account_login)
        DbRepoClient().remove(self.__github_account_login)
        DbGithubFileClient().remove(self.__github_account_login)

    # TODO: refactor so that the 2 distinct use of this enact (inserting token and then inserting file)
    #  are separated in different function/class
    def enact_installation_created_event(self, repos_name, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.request_installation_token(installation_id, FileSystemInterface.load_private_key())
        DbGithubInstallationClient().insert_one(self.__github_account_login, installation_id, installation_token, expires_at)

        for repo_name in repos_name:
            DbRepoClient().upsert_one(self.__github_account_login, repo_name)
            installation_repo = NonAuthenticatedGithubInterface(self.__github_account_login).request_repo(repo_name)
            flat_files = installation_repo.get_all_files_flat()

            for file in flat_files:
                DbGithubFileClient().insert_one(self.__github_account_login, repo_name, file.dir_path, file.name, file.type, file.content)

