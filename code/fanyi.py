import hashlib
import json
import random
import requests
import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from startup import bcc, inc

url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
appid = '20210304000715313'
secret_key = 'yuGzsednir4nSt1BlCmO'
fromLang = 'auto'
toLang = 'zh'
cuid = 'APICUID'
salt = random.randint(32768, 65536)

async def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Z2PGjO14zm8HlkjyDeV8lxAB&client_secret=OKWtWiEPYSrfaROdcZYs581lnrgGpFpD'
    response = requests.get(host)
    if response:
        return response.json()['access_token']

async def get_ocr(url):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

    params = {
        'url': '',
        'paragraph': True
    }
    params['url'] = url   
    access_token = await get_token()
    print(access_token)
    request_url = request_url + "?access_token=" + access_token
    print(request_url)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    result = ''
    if response:
        data = response.json()['words_result']
        for words in data:
            result += words['words']
    return result

async def get_fanyi(content):
    sign = appid + content + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()
    params = {
        'q': content,
        'from': fromLang,
        'to': toLang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            try:
                return data['trans_result'][0]['src'] + ':' + data['trans_result'][0]['dst']
            except Exception as e:
                raise e


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
    if content == "美女" or content == "色图" or content == "涩图" or content == "来点美女" or content == "来点色图" or content == "来点涩图":
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
async def fanyi(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group, member: Member,
):
    if message.asDisplay() == "翻译":
        f = open('mydata.json')
        data = json.load(f)
        f.close()
        data.setdefault("started_fanyi", {})

        index = str(group.id) + str(member.id)
        data['started_fanyi'][index] = True

        with open('mydata.json', 'w+') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ':'))
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("好的")
        ]))
        while True:
            content = await inc.wait(GroupMessageInterrupt(
                group, member,
                custom_judgement=lambda x: x.messageChain.asDisplay() is not None
            ))
            try:
                img_url = content.messageChain.get(Image)[0].url
                print(img_url)
                ocr = await get_ocr(img_url)
                reply = await get_fanyi(ocr)
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(reply)
                ]))
            except:
                if stop(content.messageChain.asDisplay()) == True:
                    data['started_fanyi'][index] = False
                    break
                if content.messageChain.asDisplay() == "翻译":
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(content.send.id), Plain("好的")
                    ]))
                    return
                if content.messageChain.asDisplay() == "结束" or content.messageChain.asDisplay() == "二狗":
                    data['started_fanyi'][index] = False
                    break
                # print(content)

                index = str(content.sender.group.id) + str(content.sender.id)
                if data['started_fanyi'][index] == False:
                    continue

                reply = await get_fanyi(content.messageChain.asDisplay())
                await app.sendGroupMessage(group, MessageChain.create([
                    At(content.sender.id), Plain(reply)
                ]))

        with open('mydata.json', 'w+') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ':'))
