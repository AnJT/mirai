import asyncio
import hashlib
import random

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

url = "http://api.tianapi.com/txapi/dujitang/index"
key = "541a020960672cae3d0f9745fe840048"

async def GetJiTang():
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

@bcc.receiver("GroupMessage")
async def JiTang(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not group.id==1020661362:
        return
    if message.asDisplay().startswith('毒鸡汤'):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(await GetJiTang())
    ]))
