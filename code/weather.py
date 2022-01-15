import asyncio
import json

import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain

from startup import bcc

api_key = "7892f7070c9545fbfd285a97fe717f37"
url = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
params = {
    "key": api_key,
    "city": 310114,
    "extensions": "base",
    "output": "JSON"
    }

async def get_now_weather(city_adcode=310114)->str:
    params["extensions"] = "base"
    params["city"] = city_adcode
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            # print(data)
            data = data["lives"][0]
            if data == []:
                return ''
            try:
                if data['province'] in data['city']:
                    result = '\n' + data['city'] + ':' + "天气：{} 温度：{}°C 风向：{} 风力：{}级 湿度：{}% \n数据更新于{}".format(
                        data["weather"], data["temperature"], data["winddirection"], data["windpower"], data["humidity"], data["reporttime"]
                    )
                else:
                    result = '\n' + data['province']  + data['city'] + ':' + "天气：{} 温度：{}°C 风向：{} 风力：{}级 湿度：{}% \n数据更新于{}".format(
                        data["weather"], data["temperature"], data["winddirection"], data["windpower"], data["humidity"], data["reporttime"]
                    )
            except:
                return ''
            return result

async def get_forecast_weather(city_adcode=310114)->str:
    params["extensions"] = "all"
    params["city"] = city_adcode
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            data = data["forecasts"][0]
            # print(data)
            if data['casts'] == []:
                return ''
            try:
                date = "数据更新于{} \n".format(data["reporttime"])
                if data['province'] in data['city']:
                    result = '\n' + data['city'] + ':'
                else:
                    result = '\n' + data['province']  + data['city'] + ':'
                data = data["casts"]
                for i in range(3):
                    ndata = data[i]
                    result += '\n' + "{} 白天天气：{} 温度：{}°C 风力：{} 夜晚天气：{} 温度：{}°C 风力：{}级".format(
                        ndata["date"],ndata["dayweather"],ndata["daytemp"],ndata["daypower"],ndata["nightweather"],ndata["nighttemp"],ndata["nightpower"]
                    )
                result += date
            except:
                return ''
            return result


@bcc.receiver("GroupMessage")
async def weather(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    try:
        li =['区', '县', '省', '市', '自治区', '特别行政区', '自治县', '自治州', '市辖区']
        if message.asDisplay() == "天气":
            await app.sendGroupMessage(group,MessageChain.create([
                At(member.id),Plain(await get_now_weather())
            ]))
        elif message.asDisplay() == "天气预报":
            await app.sendGroupMessage(group,MessageChain.create([
                At(member.id),Plain(await get_forecast_weather())
            ]))
        elif message.asDisplay().startswith("天气预报"):
            f=open('./json/city.json',encoding='utf-8')
            data=json.load(f)
            f.close()
            city = ''.join(message.asDisplay()[4:].lower().strip().split())
            if len(city) <= 1:
                return
            for i in li:
                if city in i:
                    await app.sendGroupMessage(group,MessageChain.create([
                        At(member.id),Plain('你肯定是有什么大病')
                    ]))
                    return
            reply = ''
            for k, v in data.items():
                if city in k:
                    reply += await get_forecast_weather(int(v))
            if reply == '':
                reply = '要么这不是个城市，要么你肯定有什么大病'
            await app.sendGroupMessage(group,MessageChain.create([
                At(member.id),Plain(reply)
            ]))
        elif message.asDisplay().startswith("天气"):
            f=open('./json/city.json',encoding='utf-8')
            data=json.load(f)
            f.close()
            city = ''.join(message.asDisplay()[2:].lower().strip().split())
            if len(city) <= 1:
                return
            for i in li:
                if city in i:
                    await app.sendGroupMessage(group,MessageChain.create([
                        At(member.id),Plain('你肯定是有什么大病')
                    ]))
                    return
            reply = ''
            for k, v in data.items():
                if city in k:
                    reply += await get_now_weather(int(v))
            if reply == '':
                reply = '要么这不是个城市，要么你肯定有什么大病'
            await app.sendGroupMessage(group,MessageChain.create([
                At(member.id),Plain(reply)
            ]))
    except Exception as e:
        print(e)
