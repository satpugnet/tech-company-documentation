class AbstractGithubFile:
    def __init__(self, path, type):
        self.__path = path
        self.__type = type

    def get_path(self):
        return self.__path

    def get_type(self):
        return self.__type

