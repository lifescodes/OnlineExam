from uuid import uuid4


def uuid_8_chars():
    return str(uuid4())[:8]
