#coding=utf-8

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
from graia.scheduler.timers import (crontabify, every_custom_hours,
                                    every_custom_minutes, every_custom_seconds)

from startup import app, bcc

url = 'https://baike.baidu.com/item/'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75'
}

async def GetSummary(word):
    word_url = url + word
    async with aiohttp.ClientSession() as session:
        async with session.get(url=word_url) as resp:
            result = resp.text
            print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(GetSummary('oracle'))
