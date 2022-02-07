from typing import List


class Mbql:
    def compile(self):
        raise NotImplementedError()

    def __repr__(self):
        return str(self.compile())


class Field(Mbql):
    def __init__(self, id: int, option=None):
        self.id = id
        self.option = option

    def compile(self) -> List:
        return ["field", self.id, self.option]
