# Refer: https://qiita.com/maueki/items/8f1e190681682ea11c98

import asyncio


async def hello_world():
    print('Hello World!')


# hello_world()

loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
