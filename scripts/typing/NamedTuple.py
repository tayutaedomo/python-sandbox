from __future__ import annotations

from typing import NamedTuple


# Ref: https://docs.python.org/ja/3/library/typing.html#typing.NamedTuple
class Profile(NamedTuple):
    first_name: str
    last_name: str


john_doe = Profile("John", "Doe")
print(john_doe)
