from fastapi import File
import base64


def base64_encode(file_bytes: bytearray = File()) -> str:
    return base64.b64encode(file_bytes)
