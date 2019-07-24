from github_interface.github_types.github_commit_file import GithubCommitFile


class GithubCommit:
    def __init__(self, commit_object):
        self.__commit_object = commit_object
        self._files = self.__initialise_commit_files()
        self._sha = self.__commit_object.sha

    @property
    def files(self):
        return self._files

    @property
    def sha(self):
        return self._sha

    def __initialise_commit_files(self):
        files = []
        for file in self.__commit_object.files:
            if file.status == "removed":
                is_deleted = True
            else:
                is_deleted = False
            files.append(GithubCommitFile(file.filename, file.previous_filename, file.patch, is_deleted))
        return files
