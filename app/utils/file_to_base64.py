from app.utils.base64_encode import base64_encode
import base64
import os


def file_to_base64(file_or_path: str | bytes, remove_file: bool = True) -> str:
    if type(file_or_path) == str:
        file = open(file_or_path, "rb")
        b64 = base64_encode(file.read())
        file.close()
        # removing file from storage
        if remove_file and os.path.exists(file_or_path):
            os.remove(file_or_path)
    elif type(file_or_path) == bytes:
        b64 = base64.b64encode(file_or_path)
    return b64
