import magic


def file_type(filepath: str) -> str:
    type = magic.from_file(filepath, mime=True)
    return type
