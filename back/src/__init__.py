import re

uuid_regex = re.compile(r"^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$")


def check_uuid(uuid: str) -> bool:
    return bool(uuid_regex.match(uuid))
