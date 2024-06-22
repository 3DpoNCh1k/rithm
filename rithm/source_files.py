from os.path import splitext
import re


class SourceFile:
    def __init__(self, path):
        self.path = path

    @property
    def extension(self):
        with_dot = splitext(self.path)[1]
        assert with_dot.startswith(".")
        return with_dot[1:]

    @property
    def text(self):
        return self.path.open().read()

    @property
    def name(self):
        return self.path.name

    @property
    def absolute_name(self):
        return str(self.path.absolute())


class CppFile(SourceFile):
    extensions = ("cpp", "hpp", "h")

    def __init__(self, path):
        super().__init__(path)
        assert self.extension in CppFile.extensions
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
