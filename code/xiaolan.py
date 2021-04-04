import asyncio
import json

import requests
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)

from startup import bcc

url='http://openapi.tuling123.com/openapi/api/v2'

async def CheckXiaoLan(content,index):
    if content.startswith("来点"):
        return False
    if content.startswith("选择"):
        return False
    if content.startswith("ddl"):
        return False
    if content.startswith("电费"):
        return False
    if content.startswith("开启青少年模式"):
        return False
    if content.startswith("开启lsp模式"):
        return False
    if content.startswith("心灵鸡汤"):
        return 
    if ''.join(content.lower().strip().split()).startswith("dailyenglish"):
        return
    f=open('mydata.json')
    data=json.load(f)
    data.setdefault("started_xiaolan",{})
    try:
        if data['started_fanyi'][index] == True:
            return False
    except:
        return False
    return True

async def Chat(content):
    data={
        "reqType":0,
        "perception": {
            "inputText": {
                "text": content
            },
            "inputImage": {
            "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "上海市",
                    "province": "上海市",
                    "street": "曹安公路"
                }
            }
        },
        "userInfo": {
            "apiKey": "644619ad0e5442b58785b2beb32e1fb4",
            "userId": "ajtbot"
        }
    }
    data=json.dumps(data)
    # 图灵接口接收的是json格式，而上面创建的data是字典，所以需要格式转化
    res=requests.post(url,data=data)
    result=res.json()
    for reply in result['results']:
        return reply['values']['text']

@bcc.receiver("GroupMessage")
async def XiaoLan(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    content=message.asDisplay()
    index=str(group.id)+str(member.id)

    check = await CheckXiaoLan(content,index)
    if check == False:
        return

    f=open('mydata.json')
    data=json.load(f)
    data.setdefault("started_xiaolan",{})
    
    if index in data["started_xiaolan"] and data["started_xiaolan"][index]==True:
        await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(await Chat(content))
    ]))
    else:
        if message.asDisplay().startswith("小兰小兰"):
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("我在！")
            ]))
            data["started_xiaolan"][index]=True

    if content.startswith("再见小兰") or content.startswith("小兰再见"):
        data["started_xiaolan"][index]=False

    with open('mydata.json','w') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
