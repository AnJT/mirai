# -*- coding: utf8 -*-
import base64
import hashlib
import hmac
import json
import random
import sys
import time

import requests
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain

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

def get_reply(content):
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
    resp = requests.get("https://" + endpoint, params=data)
    return resp.json()['Response']['Reply']

def stop(content):
    if content.startswith('接龙'):
        return True
    if content.startswith('选择'):
        return True
    if content.startswith('lang'):
        return True
    if content.startswith('guess'):
        return True
    if content.startswith('丢'):
        return True
    if content.startswith('爬'):
        return True
    if ''.join(content.lower().strip().split()) == "dailyenglish":
        return True
    if content == '青年大学习' or content == '大学习':
        return True
    if content == '毒鸡汤':
        return True
    if content == 'lc' or content == 'leetcode':
        return True
    if ''.join(content.lower().strip().split()) == "r18down" or ''.join(content.lower().strip().split()) == "r18on":
        return True
    if content=="美女" or content=="色图" or content=="涩图" or content=="来点美女" or content=="来点色图" or content=="来点涩图":
        return True
    if content == '天气':
        return True
    if content == '天气预报':
        return True
    if content == '福利' or content == '来点福利':
        return True
    if content == 'help':
        return True
    return False
    


@bcc.receiver("GroupMessage")
async def xiaolan(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    content=message.asDisplay()
    index=str(group.id)+str(member.id)

    f=open('mydata.json')
    data=json.load(f)
    data.setdefault("started_xiaolan",{})
    f.close()

    if stop(content) == True:
        data["started_xiaolan"][index]=False
        with open('mydata.json','w+') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
        return

    if content == "翻译":
        data["started_xiaolan"][index]=False
        with open('mydata.json','w+') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
        return
    
    if index in data["started_xiaolan"] and data["started_xiaolan"][index]==True:
        await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(get_reply(content))
    ]))
    else:
        if message.asDisplay() == "二狗":
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("我在！")
            ]))
            data["started_xiaolan"][index]=True

    if content == "再见" or content == "拜拜" or content == "二狗再见" or content == "二狗拜拜":
        data["started_xiaolan"][index]=False

    with open('mydata.json','w+') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

