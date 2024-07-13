import json
from pathlib import Path


class Task:
    def __init__(self, path: Path):
        self.path = path.absolute()
        self.content = json.load(path.open())

    def __getitem__(self, key):
        return self.content[key]

    def __contains__(self, key):
        return key in self.content

    def __repr__(self):
        return f"path: {self.path}\ncontent: {self.content}"

    @property
    def directory(self):
        return self.path.parent
