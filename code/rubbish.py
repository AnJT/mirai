import json

import aiohttp
from aiohttp import client_exceptions
from graia.application import GraiaMiraiApplication, session
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from requests.models import parse_header_links

from startup import bcc, inc


@bcc.receiver("GroupMessage")
async def rubbish(
    message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group, member: Member,
):
    if message.asDisplay() != '垃圾分类':
        return
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('请发送要识别的垃圾')
    ]))
    res = await inc.wait(GroupMessageInterrupt(
        group, member,
        custom_judgement=lambda x: x.messageChain.has(Image)
    ))
    img_url = res.messageChain.get(Image)[0].url
    print(img_url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://106.12.131.236:8000/rubbish",
                json={"data_url": img_url}
            ) as resp:
                ans = await resp.json()
                print(ans["ans"])
                if ans["success"] == False:
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id), Plain("服务器炸了，慢点发！")
                    ]))
                    return
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(ans["ans"])
                ]))
    except:
        pass

