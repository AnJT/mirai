import json

import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)

from startup import bcc

api_key = "32801024603dc3189af642"
url = "https://api.lolicon.app/setu/"
params = {
    "apikey":api_key,
    "r18":1,
    "num":1
    }

async def get_setu(r18:int, keyword='')->str:
    params["r18"] = r18
    params["keyword"] = ''.join(keyword.lower().strip().split())
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            try:
                result = data["data"][0]["url"]
            except:
                result = 'xs,没找到'
            return result


@bcc.receiver("GroupMessage")
async def setu_db(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    data = dict()
    with open('mydata.json') as f:
        data=json.load(f)
        data['group'][str(group.id)]=group.id
        data['friend'][str(member.id)]=member.id
    
    index = str(group.id)+str(member.id)
    if ''.join(message.asDisplay().lower().strip().split()) == "r18down":
        data['r18'][index]=0
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("懂了")
        ]))
    if ''.join(message.asDisplay().lower().strip().split()) == "r18on":
        data['r18'][index]=1
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("懂了")
        ]))
    with open('mydata.json','w+') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("搜色图"), RequireParam(name="saying")])
])
async def sou_setu(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    index = str(group.id) + str(member.id)
    r18=0
    try:
        with open('mydata.json') as f:
            data=json.load(f)
            r18=int(data['r18'][index])
    except:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("已默为r18 down模式，若想开启r18模式，请随时输入“r18 on”")
        ]))
        f=open('mydata.json')
        data=json.load(f)
        data['r18'][index]=0
        with open('mydata.json','w+') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
    result = await get_setu(r18, saying.asDisplay().strip())
    if result == 'xs,没找到':
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(result)
        ]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromNetworkAddress(url=result)
        ]))

@bcc.receiver("GroupMessage")
async def setu(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    content=message.asDisplay()
    index = str(group.id )+ str(member.id)
    if content=="美女" or content=="色图" or content=="涩图" or content=="来点美女" or content=="来点色图" or content=="来点涩图":
        r18=0
        try:
            with open('mydata.json') as f:
                data=json.load(f)
                r18=int(data['r18'][index])
        except:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("已默为r18 down模式，若想开启r18模式，请随时输入“r18 on”")
            ]))
            f=open('mydata.json')
            data=json.load(f)
            data['r18'][index]=0
            with open('mydata.json','w+') as f:
                json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

        result = await get_setu(r18)
  
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromNetworkAddress(url=result)
        ]))
