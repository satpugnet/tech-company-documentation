class GithubCommitFileModel:
    """
    Represent a github commit file.
    """

    def __init__(self, path, previous_path, patch, is_deleted):
        self.__path = path
        self.__has_path_changed = not (previous_path is None)
        self.__previous_path = self.__path if previous_path is None else previous_path
        self.__patch = patch
        self.__is_deleted = is_deleted

    @property
    def path(self):
        return self.__path

    @property
    def has_path_changed(self):
        return self.__has_path_changed

    @property
    def previous_path(self):
        return self.__previous_path

    @property
    def patch(self):
        return self.__patch

    @property
    def is_deleted(self):
        return self.__is_deleted

