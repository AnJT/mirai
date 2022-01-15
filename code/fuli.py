import random
import ssl
import urllib.request as request
import json
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
from yaml import full_load

from startup import bcc

ssl._create_default_https_context = ssl._create_unverified_context


_url = ['https://api.nmb.show/xiaojiejie1.php','http://api.nmb.show/xiaojiejie2.php ']
url_phone = 'https://api.vvhan.com/api/mobil.girl'

@bcc.receiver("GroupMessage")
async def fuli(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    content=message.asDisplay()
    if content =='福利':
        try:
            try:
                with open('./json/mydata.json') as f:
                    data=json.load(f)
                    fuli_type = data['fuli'][str(member.id)]
            except:
                fuli_type = 'pc'
            print(fuli_type)
            if fuli_type == 'pc':
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id),Image.fromNetworkAddress(_url[0])
                ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id),Image.fromNetworkAddress(url_phone)
                ]))
        except aiohttp.client_exceptions.ClientResponseError:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("冲慢点！就1Mb带宽")
            ]))

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("福利"), RequireParam(name="saying")])
])
async def fuli_n(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    if message.asDisplay().startswith('福利 --change'):
        return
    num = ''.join(saying.asDisplay().lower().strip().split())
    print(num)
    if not num.isdigit():
        await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain('\n' + 'keyerror')
            ]))
        return
    if int(num) <=0 or int(num) > 5:
        await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain(f'\n num <= 0 or num > 5')
            ]))
        return
    try:
        try:
            with open('./json/mydata.json') as f:
                data=json.load(f)
                fuli_type = data['fuli'][str(member.id)]
        except:
            fuli_type = 'pc'
        for i in range(int(num)):
            if fuli_type == 'pc':
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id),Image.fromNetworkAddress(_url[0])
                ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id),Image.fromNetworkAddress(url_phone)
                ]))
    except aiohttp.client_exceptions.ClientResponseError:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain("冲慢点！就1Mb带宽")
        ]))


@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("福利 --change"), RequireParam(name="saying")])
])
async def fuli_change(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    fuli_type = ''.join(saying.asDisplay().lower().strip().split())
    print(fuli_type)
    if fuli_type != 'pc' and fuli_type != 'phone':
        await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain('\n' + 'keyerror')
            ]))
        return
    with open('./json/mydata.json') as f:
        data=json.load(f)
        data['fuli'][member.id] = fuli_type
    with open('./json/mydata.json','w+') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
    print("ye")


