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

# api_key = "91579379616f6f226735f5"

# URL到图片
async def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    conn=aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url) as resp:
            txt = await resp.read()
            print(txt)
            return txt

async def get_setu(r18:int)->str:
    # print("get")
    url = "https://api.fantasyzone.cc/tu"
    params = {
    "class": "pixiv",
    "r18":1,
    "type": "json"
    }
    params["r18"] = r18
    conn=aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url=url,params=params) as resp:
            print(resp)
            data = await resp.json(content_type=None)
            # print(data)
            try:
                # data[0].urls.original
                result = data["url"]
            except:
                result = 'xs,没找到'
            return result

async def search_setu(key)->str:
    # print("get")
    url = "https://api.fantasyzone.cc/tu/search.php"
    params = {
    "search": key,
    "r18":2
    }
    conn=aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url=url,params=params) as resp:
            # print(resp)
            data = await resp.json(content_type=None)
            print(data)
            try:
                # data[0].urls.original
                result = data["url"]
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
    with open('./json/mydata.json') as f:
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
    with open('./json/mydata.json','w+') as f:
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
        with open('./json/mydata.json') as f:
            data=json.load(f)
            r18=int(data['r18'][index])
    except:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("已默为r18 down模式，若想开启r18模式，请随时输入“r18 on”")
        ]))
        f=open('./json/mydata.json')
        data=json.load(f)
        data['r18'][index]=0
        with open('./json/mydata.json','w+') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
    result = await search_setu(saying.asDisplay().strip())
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
            with open('./json/mydata.json') as f:
                data=json.load(f)
                r18=int(data['r18'][index])
        except:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("已默为r18 down模式，若想开启r18模式，请随时输入“r18 on”")
            ]))
            f=open('./json/mydata.json')
            data=json.load(f)
            data['r18'][index]=0
            with open('./json/mydata.json','w+') as f:
                json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
        result = await get_setu(r18)
        print(result)
        # await url_to_image(result)
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromNetworkAddress(url=result)
        ]))
