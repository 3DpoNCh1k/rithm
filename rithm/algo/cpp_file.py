from rithm.files.cpp import CppFile


class AlgoCppFile(CppFile):
    def __init__(self, file):
        super().__init__(file)

    @property
    def algo_dependencies(self):
        return tuple(
            filter(lambda dependency: dependency.startswith("algo/"), self.dependencies)
        )

    @property
    def other_dependencies(self):
        algo_dependencies = self.algo_dependencies
        return tuple(
            filter(
                lambda dependency: dependency not in algo_dependencies,
                self.dependencies,
            )
        )
