#coding=utf-8

import asyncio
import json
import random
import sqlite3
import uuid
from datetime import datetime

import aiohttp
import requests
from bs4 import BeautifulSoup
from graia.application import GraiaMiraiApplication
from graia.application.event.messages import SourceElementDispatcher
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)
from graia.scheduler.timers import (crontabify, every_custom_hours,
                                    every_custom_minutes, every_custom_seconds)

from startup import app, bcc, scheduler


def GetChengyuFromUrl():
    all_url = 'http://chengyu.t086.com/'

    #http请求头
    Hostreferer = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Referer':'http://chengyu.t086.com/'
    }

    word=['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T','W','X','Y','Z']
    sum = 0
    f=open('chengyu.json')
    data=json.load(f)
    f.close()
    for w in word:
        for n in range(1,100):
            url=all_url+'list/'+w+'_'+str(n)+'.html'
        
            start_html = requests.get(url,headers = Hostreferer)
            if(start_html.status_code==404):
                break
            start_html.encoding='gbk'
            soup = BeautifulSoup(start_html.text,"html.parser")

            listw = soup.find('div',class_='listw')
            
            lista = listw.find_all('a')
            for p in lista:
                sum += 1
                data[str(sum)] = p.text
    with open('chengyu.json', 'w+', encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

def GetChengyuFromJson(cy):
    f=open('chengyu.json',encoding='utf-8')
    data=json.load(f)
    f.close()
    result = []
    for value in data.values():
        if value.startswith(cy):
            result.append(value)
    return result

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("接龙"), RequireParam(name="saying")])
])
async def Chengyu(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    word = saying.asDisplay()[-1]
    if not is_all_chinese(word):
        return 
    result = GetChengyuFromJson(word)
    if len(result) == 0:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain("xs，根本找不到")
        ]))
        return
    sresult = random.sample(result, min(5, len(result)))
    reply = '\n'
    for value in sresult:
        reply += value+'\n'
    print(reply)
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(reply)
    ]))

@bcc.receiver("FriendMessage", dispatchers=[
    Kanata([FullMatch("接龙"), RequireParam(name="saying")])
])
async def Chengyu_friend(
    app: GraiaMiraiApplication, friend: Friend,
    saying: MessageChain
):
    word = saying.asDisplay()[-1]
    if not is_all_chinese(word):
        return 
    result = GetChengyuFromJson(word)
    if len(result) == 0:
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain("xs，根本找不到")
        ]))
        return
    sresult = random.sample(result, min(5, len(result)))
    reply = ''
    for value in sresult:
        reply += value+'\n'
    print(reply)
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain(reply)
    ]))
