import asyncio
import json
import numpy as np
import aiohttp
import re
from graia.application.friend import Friend
from fake_useragent.settings import HTTP_RETRIES
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)
import random
import time
import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
import httpx
from lxml import etree
from startup import bcc

async def testVpn(key):
    url = f'https://cn.pornhub.com/video/search?search={key}'
    headers = {
        "User-Agent": UserAgent().random,
        'content-type': 'text/html; charset=UTF-8'
    }
    proxys = {"http": 'socks5://127.0.0.1:10808', "https": 'socks5://127.0.0.1:10808'}
    resp = requests.get(url=url, headers=headers, proxies=proxys) 
    resp.encoding = 'UTF-8'
    demo = etree.HTML(resp.text)
    nodes = demo.xpath('//ul[@id="videoSearchResult"]//li[@class="pcVideoListItem js-pop videoblock videoBox"]')
    hrefs = []
    img_src = []    
    try:
        for i in nodes:
            text = etree.tostring(i, encoding="utf-8", pretty_print=True).decode("utf-8")
            href = re.search('<a href="(.*?)"', text, re.S).group(1)
            href = 'https://cn.pornhub.com' + href
            hrefs.append(href)

            src = re.search('data-thumb_url="(.*?)"', text, re.S).group(1)
            img_src.append(src)

    except Exception as e:
        print(e)
    if len(href) == 0:
        return 'xs, 没找到', None
    idx = random.choice(np.arange(len(hrefs)))
    return hrefs[idx], img_src[idx]


@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorator 混起来
    Kanata([FullMatch("pornhub"), RequireParam(name="saying")])
])
async def searchPornhub(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    content=saying.asDisplay().strip()
    reply, _ = await testVpn(content)
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(reply)
    ]))

@bcc.receiver("FriendMessage", dispatchers=[
    Kanata([FullMatch("pornhub"), RequireParam(name="saying")])
])
async def searchPornhubFriend(
    app: GraiaMiraiApplication, friend: Friend,
    saying: MessageChain
):
    content=saying.asDisplay().strip()
    reply, img_src = await testVpn(content)
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain(reply), Image.fromNetworkAddress(url=img_src)
    ]))
