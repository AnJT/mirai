import asyncio
import json

import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from requests.models import parse_header_links

from startup import bcc, inc


async def get_reply(img_url, id) -> MessageChain:
    url = "https://saucenao.com/search.php"
    data = {
        "url": img_url,
        "numres": 1,
        "testmode": 1,
        "db": 999,
        "output_type": 2,
        "api_key": "e83a310fd21d2fd1ea50b1de66c6aadd88b0afe2"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            json_data = await resp.json()

            if json_data["header"]["status"] == -1:
                return MessageChain.create([
                    At(id), Plain(json_data['header']['message'])
                ])

            if not json_data["results"]:
                return MessageChain.create([
                    At(id), Plain("xs, 没找到")
                ])

            if json_data["header"]["status"] == 0:
                result = json_data["results"][0]
                searched_img_url = result["header"]["thumbnail"]
                similarity = result["header"]["similarity"]
                data = result["data"]
                reply = "\n相似度：{}".format(similarity)
                for key in data.keys():
                    if isinstance(data[key], list):
                        reply += "\n{}:{}".format(key, data[key][0])
                    else:
                        reply += "\n{}:{}".format(key, data[key])
                return MessageChain.create([
                    At(id), 
                    Plain("\n搜索到如下结果："),
                    Image.fromNetworkAddress(searched_img_url),
                    Plain(reply)
                ])
                        
            return MessageChain.create([
                At(id), Plain("不知道哪出错了，反正是出错了")
            ])

@bcc.receiver("GroupMessage")
async def image_search(
    message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group, member: Member,
):
    if message.asDisplay() != '搜图':
        return
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('请发送要搜索的图片')
    ]))
    res = await inc.wait(GroupMessageInterrupt(
        group, member,
        custom_judgement=lambda x: x.messageChain.has(Image)
    ))
    img_url = res.messageChain.get(Image)[0].url
    await app.sendGroupMessage(group, await get_reply(img_url, member.id))
