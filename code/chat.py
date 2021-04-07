# -*- coding: utf8 -*-
import asyncio
import base64
import hashlib
import hmac
import json
import random
import sys
import time

import aiohttp
import requests
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

from startup import bcc

secret_id = "AKIDTigOt70mD0NUKvEOmqa5LK3B3f192H8P"
secret_key = "C8NLmwqUryeKjvEH5cs0h8J5JWpIVaQz"

def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str

def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)

def GetReply(content):
    endpoint = "nlp.tencentcloudapi.com"
    data = {
        'Action' : 'ChatBot',
        'Flag' : '0',
        'Language' : 'zh-CN',
        'Nonce' : 8148,
        'Query' : '你好',
        'Region' : 'ap-guangzhou',
        'SecretId' : 'AKIDTigOt70mD0NUKvEOmqa5LK3B3f192H8P',
        'Timestamp' : 1617714637,
        'Version' : '2019-04-08'
}
    data['Query'] = content
    data['Nonce'] = random.randint(1, sys.maxsize)
    data['Timestamp'] = int(time.time())
    s = get_string_to_sign("GET", endpoint, data)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)
    print(data['Signature'])
    resp = requests.get("https://" + endpoint, params=data)
    # print(resp.json()['Response']['Reply'])
    print(resp.json())
    return resp.json()['Response']['Reply']


@bcc.receiver("GroupMessage")
async def XiaoLan(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    content=message.asDisplay()
    index=str(group.id)+str(member.id)

    f=open('mydata.json')
    data=json.load(f)
    data.setdefault("started_xiaolan",{})
    
    if index in data["started_xiaolan"] and data["started_xiaolan"][index]==True:
        await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(GetReply(content))
    ]))
    else:
        if message.asDisplay().startswith("二狗"):
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("我在！")
            ]))
            data["started_xiaolan"][index]=True

    if content.startswith("再见") or content.startswith("拜拜"):
        data["started_xiaolan"][index]=False

    with open('mydata.json','w') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

