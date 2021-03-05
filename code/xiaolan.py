import asyncio
import json

import requests

url='http://openapi.tuling123.com/openapi/api/v2'

async def checkxiaolan(content,index):
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

async def chat(content):
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
