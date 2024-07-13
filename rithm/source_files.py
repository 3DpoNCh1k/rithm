import re
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


class CppFile(File):
    valid_extensions = ("cpp", "hpp", "h")

    def __init__(self, file):
        super().__init__(file)
        assert (
            self.extension in self.valid_extensions
        ), f"File {file} should have any of these {self.valid_extensions} extensions"

        self.dependencies = self._find_dependencies()

    def _find_dependencies(self):
        angle_brackets_deps = tuple(
            map(
                lambda match: match.group("path"),
                re.finditer(r"#include <(?P<path>.*)>", self.text),
            )
        )
        quotes_deps = tuple(
            map(
                lambda match: match.group("path"),
                re.finditer(r'#include "(?P<path>.*)"', self.text),
            )
        )
        return angle_brackets_deps + quotes_deps

    @property
    def algo_dependencies(self):
        return tuple(filter(lambda dep: dep.startswith("algo/"), self.dependencies))

    @property
    def std_dependencies(self):
        return tuple(filter(lambda dep: not dep.startswith("algo/"), self.dependencies))
