# Refer: https://qiita.com/maueki/items/8f1e190681682ea11c98

import asyncio
import time


async def task_one() -> int:
    print('task_one: before sleep')
    await asyncio.sleep(0.1)
    print('task_one: after sleep')
    return 1


async def time_sleep():
    time.sleep(5)
    print('time_sleep')


async def task_two() -> int:
    print('task_two: before sleep')
    await time_sleep()
    print('task_two: after sleep')
    return 2


async def test(loop):
    t1 = loop.create_task(task_one())
    t2 = loop.create_task(task_two())

    print(repr(await t1))
    print(repr(await t2))


def main():
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(test(loop))
    finally:
        loop.close()


main()
