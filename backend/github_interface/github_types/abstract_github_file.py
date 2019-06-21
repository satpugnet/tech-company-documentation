from utils.json.jsonable import Jsonable


class AbstractGithubFile(Jsonable):

    DIRECTORY = "dir"

    def __init__(self, content_file):
        self._path = content_file.path if content_file else ""
        self._type = content_file.type if content_file else self.DIRECTORY
        self._name = content_file.name if content_file else ""

    @property
    def path(self):
        return self._path

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    def to_json(self):
        return {
            "path": self.path,
            "type": self.type,
            "name": self.name
        }

