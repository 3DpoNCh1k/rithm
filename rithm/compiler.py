import subprocess

from .config import ALGO_PATH


def compile_solver(solution_path, solver_path):
    cmd = f"g++ --std=c++17 -I {ALGO_PATH} -Wall -Wextra -Wshadow -fsanitize=address -fsanitize=undefined -o {solver_path} {solution_path}"
    subprocess.check_call(cmd, shell=True)

class Compiler:
    pass