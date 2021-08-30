from typing import overload, Union


@overload
def double(arg: int) -> int:
    ...


@overload
def double(arg: str) -> str:
    ...


def double(arg: Union[int, str]):
    return arg * 2


# エラー出ない
var2: int = double(1)
var11: str = double("1")
print(type(var2), var2)
print(type(var11), var11)
