import asyncio
import json

import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.event.messages import SourceElementDispatcher
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)

from startup import bcc

api_key = "7892f7070c9545fbfd285a97fe717f37"
url = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
params = {
    "key": api_key,
    "city": 310114,
    "extensions": "base",
    "output": "JSON"
    }

async def GetNowWeather()->str:
    params["extensions"] = "base"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            # print(data)
            data = data["lives"][0]
            result = "天气：{} 温度：{}摄氏度 风向：{} 风力：{}级 湿度：{}% \n数据发布于{}".format(
                data["weather"],data["temperature"],data["winddirection"],data["windpower"],data["humidity"],data["reporttime"]
            )
            return (result)

async def GetForecastWeather()->str:
    params["extensions"] = "all"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            data = data["forecasts"][0]
            date = "数据更新于{} \n".format(data["reporttime"])
            data = data["casts"]
            result = "\n"
            print(data)
            for i in range(4):
                ndata = data[i]
                result += "{} 白天天气：{} 温度：{}摄氏度 风力：{} 夜晚天气：{} 温度：{}摄氏度 风力：{}级\n".format(
                    ndata["date"],ndata["dayweather"],ndata["daytemp"],ndata["daypower"],ndata["nightweather"],ndata["nighttemp"],ndata["nightpower"]
                )
            result += date
            return result



@bcc.receiver("GroupMessage")
async def Weather(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not message.asDisplay().startswith("天气"):
        return
    if message.asDisplay().count("预报") or message.asDisplay().count("预测"):
        reply = await GetForecastWeather()
    else:
        reply = await GetNowWeather()
    await app.sendGroupMessage(group,MessageChain.create([
        At(member.id),Plain(reply)
    ]))
