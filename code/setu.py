import asyncio
import json
from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY, NULL

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

api_key = "32801024603dc3189af642"
url = "https://api.lolicon.app/setu/"
params = {
    "apikey":api_key,
    "r18":1,
    "num":1
    }

async def GetSeTu(r18:int)->str:
    params["r18"]=r18
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as resp:
            data = await resp.json()
            # print(data["data"])
            return data["data"][0]["url"]

@bcc.receiver("GroupMessage")
async def SeTuDB(
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
    if message.asDisplay().startswith("开启青少年模式"):
        data['r18'][index]=0
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("懂了")
        ]))
    if message.asDisplay().startswith("开启lsp模式"):
        data['r18'][index]=1
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("懂了")
        ]))
    with open('mydata.json','w') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorator 混起来
    Kanata([FullMatch("来点"), RequireParam(name="saying")])
])
async def SeTu(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    img_path='img\\'
    content=saying.asDisplay()
    num_list=[0,1,2]
    index = str(group.id)+str(member.id)
    if "美女" in content or "色图" in content or "涩图" in content:
        r18=0
        try:
            with open('mydata.json') as f:
                data=json.load(f)
                r18=int(data['r18'][index])
        except:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("已默认为您开启青少年模式，若想开启lsp模式，请随时输入“开启lsp模式”")
            ]))
            f=open('mydata.json')
            data=json.load(f)
            data['r18'][index]=0
            with open('mydata.json','w') as f:
                json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

        img_url = await GetSeTu(r18)

        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromNetworkAddress(url=img_url)
        ]))