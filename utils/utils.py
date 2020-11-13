import json

ENCODING = 'utf-8'


def dict_to_bytes(message_dict):
    """
    Convert dict to bytes
    :param message_dict: dict
    :return: bytes
    """
    if not isinstance(message_dict, dict):
        raise TypeError

    jmessage = json.dumps(message_dict)

    bmessage = jmessage.encode(ENCODING)
    return bmessage


def byte_to_dict(message_byte):
    """
    Convert bytes to dict
    :param message_byte: bytes
    :return: dict
    """
    if not isinstance(message_byte, bytes):
        raise TypeError

    jmessage = message_byte.decode(ENCODING)

    message_dict = json.loads(jmessage)
    return message_dict
