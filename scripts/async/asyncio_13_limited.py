# https://dev.classmethod.jp/articles/python-asyncio/

import asyncio
import functools
import time


async def sleeping(sec: int):
    loop = asyncio.get_event_loop()
    func = functools.partial(time.sleep, sec)
    print(f'start: wait for {sec}s')
    await loop.run_in_executor(None, func)
    print(f'finish: wait for {sec}s')


async def limited_parallel_call(sec_list: [int], limit: int):
    sem = asyncio.Semaphore(limit)

    async def call(sec: int):
        # with await sem:
        async with sem:
            return await sleeping(sec)

    return await asyncio.gather(*[call(x) for x in sec_list])


def main():
    loop = asyncio.get_event_loop()
    options = [5, 1, 8, 3, 4]

    print('=== Execute without limit ===')
    loop.run_until_complete(asyncio.gather(*[sleeping(x) for x in options]))

    print('\n=== Execute with limit:2 ===')
    loop.run_until_complete(limited_parallel_call(options, 2))

    print('\n===finish===')


if __name__ == "__main__":
    main()
