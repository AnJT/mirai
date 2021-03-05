import asyncio
import hashlib
import random

import aiohttp

url = "http://api.tianapi.com/txapi/everyday/index"
key = "541a020960672cae3d0f9745fe840048"

async def getDailyenglish():
    params = {
        'key':key,
        'rand':1
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as resp:
            data = await resp.json()
            try:
                return '\n'+data['newslist'][0]['content']+'\n'+data['newslist'][0]['note']
            except Exception as e:
                raise e
