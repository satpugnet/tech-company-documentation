class AbstractGithubFile:
    def __init__(self, content_file):
        self.__path = content_file.path if content_file else ""
        self.__type = content_file.type if content_file else None
        self.__name = content_file.name if content_file else ""

    def get_path(self):
        return self.__path

    def get_type(self):
        return self.__type

    def get_name(self):
        return self.__name

