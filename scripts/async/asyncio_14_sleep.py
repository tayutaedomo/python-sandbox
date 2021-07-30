# https://dev.classmethod.jp/articles/python-asyncio/

import asyncio


async def sleeping(sec: int):
    print(f'start: wait for {sec}s')
    await asyncio.sleep(sec)
    print(f'finish: wait for {sec}s')


async def limited_parallel_call(sec_list: [int], limit: int):
    sem = asyncio.Semaphore(limit)

    async def call(sec: int):
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
