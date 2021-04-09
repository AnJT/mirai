import asyncio
import json

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
from graia.scheduler.timers import crontabify

from startup import app, bcc, scheduler

url = "http://api.tianapi.com/txapi/everyday/index"
key = "541a020960672cae3d0f9745fe840048"

async def GetDailyEnglish():
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

@scheduler.schedule(crontabify("00 07 * * *"))
async def DailyEnglishScheduled():
    f=open('mydata.json')
    data=json.load(f)
    await app.sendGroupMessage(data['group']["1020661362"], MessageChain.create([
        Plain(await GetDailyEnglish())
    ]))
    f.close()

@bcc.receiver("GroupMessage")
async def DailyEnglish(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not group.id==1020661362:
        return
    if ''.join(message.asDisplay().lower().strip().split()).startswith("dailyenglish"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(await GetDailyEnglish())
    ]))
