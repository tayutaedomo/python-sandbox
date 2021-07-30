# https://dev.classmethod.jp/articles/python-asyncio/

import asyncio
import time


async def sleeping(sec: int):
    # loop = asyncio.get_event_loop()
    print(f'start: wait for {sec}s')
    # await loop.run_in_executor(None, time.sleep, sec)
    await asyncio.sleep(sec)
    print(f'finish: wait for {sec}s')


def main():
    loop = asyncio.get_event_loop()

    print('=== Execute only 1 task ===')
    loop.run_until_complete(sleeping(2))

    print('\n=== Execute 5 tasks in parallel ===')
    gather = asyncio.gather(
        sleeping(5),
        sleeping(1),
        sleeping(8),
        sleeping(3),
        sleeping(4)
    )
    loop.run_until_complete(gather)


if __name__ == "__main__":
    main()
