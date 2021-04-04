import asyncio
import base64
import hashlib
import json
import random

import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)
from PIL import Image

from startup import bcc, inc

url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
appid='20210304000715313'
secret_key='yuGzsednir4nSt1BlCmO'
fromLang='auto'
toLang='zh'
cuid='APICUID'
salt=random.randint(32768,65536)

async def GetFanyi(content):
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


@bcc.receiver("GroupMessage")
async def FanYi(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if message.asDisplay().startswith("翻译"):
        f=open('mydata.json')
        data=json.load(f)
        f.close()
        data.setdefault("started_fanyi",{})

        index=str(group.id)+str(member.id)
        data['started_fanyi'][index] = True

        with open('mydata.json','w') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("好的")
        ]))
        while True:
            content=await inc.wait(GroupMessageInterrupt(
                group, member,
                custom_judgement=lambda x: x.messageChain.asDisplay() is not None
            ))
            if content.messageChain.asDisplay().startswith("结束"):
                data['started_fanyi'][index] = False
                break
            # print(content)
            
            index=str(content.sender.group.id)+str(content.sender.id)
            if data['started_fanyi'][index] == False:
                continue

            reply = await GetFanyi(content.messageChain.asDisplay())  
            await app.sendGroupMessage(group,MessageChain.create([
                At(content.sender.id),Plain(reply)
            ]))

        with open('mydata.json','w') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
