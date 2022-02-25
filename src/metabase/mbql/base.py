from typing import List


class Option:
    pass


class Mbql:
    def __init__(self, id: int, option: Option = None):
        self.id = id
        self.option = option

    def compile(self) -> List:
        return ["field", self.id, self.option]

    def __repr__(self):
        return str(self.compile())
