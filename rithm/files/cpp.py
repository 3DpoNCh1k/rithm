import re

from .file import File


class CppFile(File):
    valid_extensions = (".cpp", ".hpp", ".h")

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
