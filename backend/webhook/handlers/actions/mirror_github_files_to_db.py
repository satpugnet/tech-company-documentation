import glob
import os
import shutil

from git import Repo

from github_interface.wrappers.models.abstract_github_fs_node_model import AbstractGithubFSNode
from mongo.collection_clients.clients.db_github_fs_node_client import DbGithubFSNodeClient
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from tools import logger
from utils.path_manipulator import PathManipulator
from webhook.handlers.actions.abstract_webhook_action import AbstractWebhookAction


class MirrorGithubFilesToDb(AbstractWebhookAction):
    """
    Mirrors all of the github repos' files to the database for quicker access in the future.
    """

    def __init__(self, repos_name, github_account_login):
        self.__repos_name = repos_name
        self.__github_account_login = github_account_login

    def perform(self):
        logger.get_logger().info("Inserting and mirroring all the github files in repo %s in the database", self.__github_account_login)

        for repo_name in self.__repos_name:
            current_cloned_folder_name = "backend/temp_github_cloned_repos/{}".format(repo_name)
            installation_token = DbGithubInstallationClient().find_one(self.__github_account_login).token

            # Clone the repo from github
            Repo.clone_from("https://x-access-token:{}@github.com/{}/{}.git".format(installation_token, self.__github_account_login, repo_name), current_cloned_folder_name)

            # Walk through the repo and save the files and folders
            self.__walk_through_cloned_repo_and_insert_to_db(self.__github_account_login, repo_name, current_cloned_folder_name)

            # Remove the cloned folder
            shutil.rmtree(current_cloned_folder_name)

    def __walk_through_cloned_repo_and_insert_to_db(self, github_account_login, repo_name, cloned_repo_path):
        """
        This method walks through the directory at cloned_repo_path recursively and insert all of the files and
        directory to the database.
        """
        logger.get_logger().info("Walking and inserting to db for the repo %s/%s at path %s", github_account_login, repo_name, cloned_repo_path)

        for fs_node_path in glob.iglob(cloned_repo_path + '**/**', recursive=True):
            content = ""

            if os.path.isfile(fs_node_path):
                type = AbstractGithubFSNode.FILE_TYPE

                try:
                    with open(fs_node_path) as f:
                        content = f.read()

                except UnicodeDecodeError:
                    logger.get_logger().warning("UnicodeDecodeError: Could not read %s", fs_node_path)

            else:
                content = []
                for _, _, sub_fs_node_names in os.walk(fs_node_path):
                    for sub_fs_node_name in sub_fs_node_names:
                        content.append(sub_fs_node_name)
                    break  # prevent descending into subfolders
                type = AbstractGithubFSNode.DIRECTORY_TYPE

            split_path = PathManipulator().dissociate_dir_path_from_fs_node_name(fs_node_path)
            fs_node_name = split_path.fs_node_name
            dir_path = split_path.dir_path[len(cloned_repo_path) + 1:]

            DbGithubFSNodeClient().insert_one(
                github_account_login,
                repo_name,
                dir_path,
                fs_node_name,
                type,
                content
            )
