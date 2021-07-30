# https://dev.classmethod.jp/articles/python-asyncio/

import asyncio
import time
import functools


def delayed_print(message: str, sec: int):
    time.sleep(sec)
    print(message)


async def call_1(message: str, sec: int):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, delayed_print, message, sec)


async def call_2(message: str, sec: int):
    loop = asyncio.get_event_loop()
    func = functools.partial(delayed_print, message, sec)
    await loop.run_in_executor(None, func)


async def call_3(mes: str, seconds: int):
    loop = asyncio.get_event_loop()
    func = functools.partial(delayed_print, message=mes, sec=seconds)
    await loop.run_in_executor(None, func)


def main():
    loop = asyncio.get_event_loop()
    gather = asyncio.gather(
        call_1('333', 3),
        call_2('222', 2),
        call_3('111', 1)
    )
    loop.run_until_complete(gather)


if __name__ == "__main__":
    main()
