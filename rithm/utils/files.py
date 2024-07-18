from pathlib import Path


def get_files_from_directory(path: Path, recursive=False, extensions: list[str] = None):
    assert path.is_dir()
    iterator = path.glob("**/*") if recursive else path.iterdir()
    files_iterator = filter(lambda path: path.is_file(), iterator)
    if extensions is not None:
        files_iterator = filter(lambda file: file.suffix in extensions, files_iterator)
    return list(filter(lambda path: path.is_file(), iterator))
