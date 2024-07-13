from pathlib import Path


def get_files_from_directory(path: Path, recursive=False):
    assert path.is_dir()
    iterator = path.glob("**/*") if recursive else path.iterdir()
    return list(filter(lambda path: path.is_file(), iterator))
