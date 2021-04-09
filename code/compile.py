#coding=utf-8

import asyncio
import json
import random
import sqlite3
import uuid
from datetime import datetime

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
from graia.scheduler.timers import (crontabify, every_custom_hours,
                                    every_custom_minutes, every_custom_seconds)

from startup import app, bcc

url = 'https://tool.runoob.com/compile2.php'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}
data = {
    'code':'''fn main() {
    println!("Hello World!");
}''',
    'token':'4381fe197827ec87cbac9552f14ec62a',
    'fileext':'rs'
}
async def GetOutput(lang, code):
    f=open('compile.json',encoding='utf-8')
    js=json.load(f)
    if lang not in js:
        return 'yysy，这个语言还是你懂得多！'
    data['fileext'] = js.get(lang)
    data['code'] = code.lstrip()
    print(code.lstrip())
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data, headers=headers) as resp:
            result = await resp.json()
            print(result)
            if result['errors'] =='\n\n':
                reply = 'output: ' + result['output']
            else:
                replt = reply = 'output: ' + result['output'] + '\nerrors: ' + result['errors']
            return reply


@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("lang"), RequireParam(name="saying")])
])
async def Compile(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    try:
        saying = saying.asDisplay()
        idx = saying.index(';')
        lang = saying[:idx]
        lang = ''.join(lang.lower().strip().split())
        code = saying[idx+1:]
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(await GetOutput(lang, code))
        ]))
    except Exception as e:
        print(e)
