class GitDiffCodeLine:
    def __init__(self, code_line, state):
        self.__code_line = code_line
        self.__state = state

    @property
    def code_line(self):
        return self.__code_line

    @property
    def state(self):
        return self.__state


