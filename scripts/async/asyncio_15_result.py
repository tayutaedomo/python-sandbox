# https://dev.classmethod.jp/articles/python-asyncio/

import asyncio
import time
import requests


def sleep(sec: int):
    time.sleep(sec)
    return sec


async def get_global_ip() -> str:
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, requests.get, 'http://inet-ip.info/ip')
    print('get_ip')
    return res.text


async def parallel_sleep(sec: int):
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, sleep, sec)
    print(f'sleep: {res}s')
    return res


def main():
    loop = asyncio.get_event_loop()
    gather = asyncio.gather(
        parallel_sleep(10),
        get_global_ip(),
        parallel_sleep(1)
    )
    ret = loop.run_until_complete(gather)
    print(ret)


if __name__ == "__main__":
    main()
