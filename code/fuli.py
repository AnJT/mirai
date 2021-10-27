import random
import ssl
import urllib.request as request

import aiohttp
import cv2
import numpy as np
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)

from startup import bcc

ssl._create_default_https_context = ssl._create_unverified_context


_url = ['https://api.nmb.show/xiaojiejie1.php','http://api.nmb.show/xiaojiejie2.php ']


# URL到图片
async def url_to_image():
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    url = _url[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            txt = await resp.read()
            return txt

# async def get_bytes():
#     fuli_url = random.choice(url)
#     fuli_img = await url_to_image(fuli_url)
#     img_b = cv2.imencode('.png', fuli_img)[1].tobytes()
#     return img_b

@bcc.receiver("GroupMessage")
async def fuli(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    content=message.asDisplay()
    if content =='福利' or content =='来点福利':
        try:
            await app.sendGroupMessage(group, MessageChain.create([
                # At(member.id),Image.fromUnsafeBytes(await url_to_image())
                At(member.id),Image.fromNetworkAddress(_url[0])
            ]))
        except aiohttp.client_exceptions.ClientResponseError:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("冲慢点！就1Mb带宽")
            ]))
