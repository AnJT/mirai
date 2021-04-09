import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup
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
from graia.scheduler.timers import (every_custom_hours, every_custom_minutes,
                                    every_custom_seconds)

from startup import app, bcc, scheduler

url = "http://news.cyol.com/node_67071.htm"
headers={
    'user-agend':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

async def GetNewestInfo():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            newest_url = soup.select(
                'body > div.mianbody > dl > dd > ul > li:nth-child(1) > a'
            )[0]['href']
            newest_title = soup.select(
                'body > div.mianbody > dl > dd > ul > li:nth-child(1) > h3 > a'
            )[0].string
            newest_time = soup.select(
                'body > div.mianbody > dl > dd > ul > li:nth-child(1) > div'
            )[0].text[1:]
            return (newest_title, newest_url, newest_time)

async def GetReply(data, call=False):
    reply = ''
    if not call:
        reply += '快学，大学习更新了\n'
    reply = data[0]+'\n'+data[1]+'\n更新于'+data[2]
    return reply

daxuexi_newest_title = ''

@scheduler.schedule(every_custom_minutes(10))
async def DaxuexiRemind():
    global daxuexi_newest_title
    newest_data = await GetNewestInfo()
    if newest_data[0] == daxuexi_newest_title:
        return
    if daxuexi_newest_title == '':
        daxuexi_newest_title = newest_data[0]
        return
    replay = await GetReply(newest_data)
    f=open('mydata.json')
    data=json.load(f)
    await app.sendGroupMessage(data['group']["1020661362"], MessageChain.create([
        At(342472121),Plain(replay)
    ]))
    f.close()

@bcc.receiver("GroupMessage")
async def Weather(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not message.asDisplay().startswith("青年大学习"):
        return
    newest_data = await GetNewestInfo()
    reply = await GetReply(newest_data, True)
    await app.sendGroupMessage(group,MessageChain.create([
        At(member.id),Plain(reply)
    ]))
