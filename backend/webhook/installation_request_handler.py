import time

from github_interface.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.models.db_account_installation import DbAccountInstallation
from mongo.models.db_github_file import DbGithubFile
from mongo.models.db_repo import DbRepo


class InstallationRequestHandler:

    def __init__(self, org_user_account):
        self.__org_user_account = org_user_account

    # TODO: refactor so that the 2 distinct use of this enact (inserting token and then inserting file) are separated in different function/class
    def enact_installation_deleted_event(self):
        DbAccountInstallation.remove(self.__org_user_account)
        DbRepo.remove(self.__org_user_account)
        DbGithubFile.remove(self.__org_user_account)


    # TODO: refactor so that the 2 distinct use of this enact (inserting token and then inserting file) are separated in different function/class
    def enact_installation_created_event(self, repos_full_name, installation_id):
        DbAccountInstallation.insert_if_not_exist(self.__org_user_account, installation_id)

        for repo_full_name in repos_full_name:
            DbRepo.upsert(self.__org_user_account, repo_full_name)
            installation_repo = NonAuthenticatedGithubInterface.get_repo(self.__org_user_account, repo_full_name)
            flat_files = installation_repo.get_all_files_flat()
            for file in flat_files:
                DbGithubFile.upsert(self.__org_user_account, repo_full_name, file.dir_path, file.name, file.type, file.content)

