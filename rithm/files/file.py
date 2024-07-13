from pathlib import Path


class File:
    def __init__(self, file):
        self.path = Path(file).absolute()
        assert self.path.is_file()

    @property
    def extension(self):
        return self.path.suffix

    @property
    def text(self):
        return self.path.open().read()

    @property
    def name(self):
        return self.path.name

    @property
    def name_without_extension(self):
        return self.path.stem

    @property
    def full_name(self):
        return str(self.path)

    @property
    def directory(self):
        return self.path.parent
