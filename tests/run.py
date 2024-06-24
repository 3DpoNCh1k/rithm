from pathlib import Path

from rithm.source_files import *
from rithm.graph import *


def main():
    print("Hello!")
    paths = list(Path(".").iterdir())
    print(paths)
    # for p in paths:
    #     if p.is_file():
    #         print(os.path.splitext(p))
    #         # print(SourceFile(p).extension)
    #         # print(SourceFile(p).text)
    #         CppFile(p)
    p = Path("./tests/run.cpp")
    cpp_file = CppFile(p)
    print(hash(cpp_file))
    print(hash(Node(cpp_file)))

    g = create_graph(p)
    res, cycle = has_cycle(g)
    print(g)

    g = {1: [2], 2: [1]}
    res, cycle = has_cycle(g)
    print(res)
    print(cycle)


if __name__ == "__main__":
    main()
