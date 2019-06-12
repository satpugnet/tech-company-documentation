class GitDiffCodeLine:
    def __init__(self, code_line, state):
        self.code_line = code_line
        self.state = state

    def get_state(self):
        return self.state

    def get_code_line(self):
        return self.code_line

