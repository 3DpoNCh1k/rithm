from rithm.files.cpp import CppFile


class AlgoCppFile(CppFile):
    @property
    def algo_dependencies(self):
        return tuple(
            filter(lambda dependency: dependency.startswith("algo/"), self.dependencies)
        )

    @property
    def tests_dependencies(self):
        return tuple(
            filter(
                lambda dependency: dependency.startswith("tests/"), self.dependencies
            )
        )

    @property
    def other_dependencies(self):
        algo_dependencies = self.algo_dependencies
        tests_dependencies = self.tests_dependencies
        return tuple(
            filter(
                lambda dependency: dependency not in algo_dependencies
                and dependency not in tests_dependencies,
                self.dependencies,
            )
        )
