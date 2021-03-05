import asyncio
import hashlib
import random

import aiohttp

url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
appid='20210304000715313'
secret_key='yuGzsednir4nSt1BlCmO'
fromLang='auto'
toLang='zh'
salt=random.randint(32768,65536)


async def getFanyi(content):
    sign=appid+content+str(salt)+secret_key
    sign=hashlib.md5(sign.encode()).hexdigest()
    params = {
    'q':content,
    'from':fromLang,
    'to':toLang,
    'appid':appid,
    'salt':salt,
    'sign':sign
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as resp:
            data = await resp.json()
            try:
                return data['trans_result'][0]['src']+':'+data['trans_result'][0]['dst']
            except Exception as e:
                raise e
            # print(data)
            # return data["data"][0]["url"]
