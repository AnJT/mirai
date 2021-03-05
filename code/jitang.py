import asyncio
import hashlib
import random

import aiohttp

url = "http://api.tianapi.com/txapi/dujitang/index"
key = "541a020960672cae3d0f9745fe840048"

async def getJitang():
    params = {
        'key':key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as resp:
            data = await resp.json()
            try:
                return data['newslist'][0]['content']
            except Exception as e:
                raise e
