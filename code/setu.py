import asyncio

import aiohttp

api_key = "32801024603dc3189af642"
url = "https://api.lolicon.app/setu/"
params = {"apikey":api_key,"r18":1,"num":1}

async def getSetu(r18:int)->str:
    params["r18"]=r18
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as resp:
            data = await resp.json()
            # print(data["data"])
            return data["data"][0]["url"]
