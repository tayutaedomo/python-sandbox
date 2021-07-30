# Refer: https://qiita.com/maueki/items/8f1e190681682ea11c98

import asyncio
import time


async def hello_world(n: int):
    time.sleep(1)
    print('{}: Hello World!'.format(n))


async def call_hello_world_1():
    print('call_hello_world_1()')
    await hello_world(1)


async def call_hello_world_2():
    print('call_hello_world_2()')
    await hello_world(2)


loop = asyncio.get_event_loop()
loop.create_task(call_hello_world_1())
loop.run_until_complete(call_hello_world_2())
