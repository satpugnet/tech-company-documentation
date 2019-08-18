class GithubCommit:
    def __init__(self, files, sha):
        self.__files = files
        self.__sha = sha

    @property
    def files(self):
        return self.__files

    @property
    def sha(self):
        return self.__sha
