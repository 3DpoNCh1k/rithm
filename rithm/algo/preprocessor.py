import sys

from rithm.utils.cpp import *
from rithm.utils.graph import get_topological_order, has_cycle

from .cpp_file import AlgoCppFile


class Preprocessor:
    def __init__(self, algo_path):
        self.algo_path = algo_path

    def expand_includes(self, file: AlgoCppFile):
        dependency_graph = self._create_graph(file)
        dependency_order = get_topological_order(dependency_graph)

        header = "// TODO: add header"
        std_includes_text = self._get_std_includes_text(dependency_order)
        algo_text = self._get_algo_text(dependency_order)

        return "\n".join([header, std_includes_text, algo_text])

    def check_dependency_cycle(self, file: AlgoCppFile):
        dependency_graph = self._create_graph(file)
        result, cycle = has_cycle(dependency_graph)
        if result:
            print(f"Found cycle: {cycle}")
            sys.exit(1)

    def _get_std_includes_text(self, dependency_order):
        std_dependencies = set()
        for file_node in dependency_order:
            std_dependencies.update(file_node.file.other_dependencies)

        return generate_includes(std_dependencies)

    def _get_algo_text(self, dependency_order):
        algo_text_list = []
        for file_node in dependency_order:
            file_text = file_node.file.text
            file_text = remove_pragma_once(file_text)
            file_text = remove_includes(file_text)
            algo_text_list.append(file_text)

        return "\n".join(algo_text_list)

    def _create_graph(self, file: AlgoCppFile):

        class Node:
            def __init__(self, file: AlgoCppFile):
                self.file = file

        nodes = {}
        graph = {}

        def get_or_create_node(file):
            if file not in nodes:
                nodes[file] = Node(file)
            return nodes[file]

        def traverse(current_node: Node):
            if current_node in graph:
                return

            graph[current_node] = []
            for dependency_name in current_node.file.algo_dependencies:
                dependency_file = AlgoCppFile(self.algo_path / dependency_name)
                dependency_node = get_or_create_node(dependency_file)
                graph[current_node].append(dependency_node)
                traverse(dependency_node)

        traverse(get_or_create_node(file))
        return graph
