import asyncio
import json
import random
from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY, NULL

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
from graia.application.session import Session
from graia.broadcast import Broadcast
from graia.scheduler.timers import crontabify

from dailyenglish import getDailyenglish
from electricity import getElectricity
from fanyi import getFanyi
from jitang import getJitang
from setu import getSetu
from startup import app, bcc, inc, loop, scheduler
from xiaolan import chat, checkxiaolan


@bcc.receiver("GroupMessage")
async def group_message_database_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    data = dict()
    with open('mydata.json') as f:
        data=json.load(f)
        data['group'][str(group.id)]=group.id
        data['friend'][str(member.id)]=member.id
    # print(data)
    index = str(group.id)+str(member.id)
    if message.asDisplay().startswith("开启青少年模式"):
        data['r18'][index]=0
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("懂了")
        ]))
    if message.asDisplay().startswith("开启lsp模式"):
        data['r18'][index]=1
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("懂了")
        ]))
    with open('mydata.json','w') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))


@bcc.receiver("GroupMessage",dispatchers=[
    Kanata([FullMatch("ddl"),RequireParam(name="saying")])
])
async def group_message_ddl_hamdler(
    message:MessageChain,
    app:GraiaMiraiApplication,
    group:Group,member:Member,
    saying:MessageChain
):
    content=saying.asDisplay()

@scheduler.schedule(crontabify("00 07 * * *"))
async def daily_english_scheduled():
    f=open('mydata.json')
    data=json.load(f)
    await app.sendGroupMessage(data['group']["1020661362"], MessageChain.create([
        At(342472121),Plain(await getDailyenglish())
    ]))
    f.close()

@bcc.receiver("GroupMessage")
async def group_message_database_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not group.id==1020661362:
        return
    if ''.join(message.asDisplay().lower().strip().split()).startswith("dailyenglish"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(await getDailyenglish())
    ]))


@bcc.receiver("GroupMessage")
async def group_message_database_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not group.id==1020661362:
        return
    if message.asDisplay().startswith('毒鸡汤'):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(await getJitang())
    ]))

@bcc.receiver("GroupMessage")
async def group_message_database_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not group.id==1020661362:
        return
    if message.asDisplay().startswith('电费'):
        elec=getElectricity()
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain(elec)
        ]))


@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorator 混起来
    Kanata([FullMatch("来点"), RequireParam(name="saying")])
])
async def group_message_laidian_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    img_path='img\\'
    content=saying.asDisplay()
    num_list=[0,1,2]
    index = str(group.id)+str(member.id)
    if "美女" in content or "色图" in content or "涩图" in content:
        r18=0
        try:
            with open('mydata.json') as f:
                data=json.load(f)
                r18=int(data['r18'][index])
        except:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("已默认为您开启青少年模式，若想开启lsp模式，请随时输入“开启lsp模式”")
            ]))
            f=open('mydata.json')
            data=json.load(f)
            data['r18'][index]=0
            with open('mydata.json','w') as f:
                json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))

        img_url = await getSetu(r18)

        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromNetworkAddress(url=img_url)
        ]))
    elif "猫" in content:
        img_path+="m"+str(random.randint(1,5))+'.jpg'
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromLocalFile(img_path)
        ]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain("没实现呢！")
        ]))

@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorator 混起来
    Kanata([FullMatch("选择"), RequireParam(name="saying")])
])
async def group_message_choice_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    content_list=saying.asDisplay().strip().split()

    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(random.choice(content_list))
    ]))

@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if message.asDisplay().startswith("翻译"):
        f=open('mydata.json')
        data=json.load(f)
        f.close()
        data.setdefault("started_fanyi",{})

        index=str(group.id)+str(member.id)
        data['started_fanyi'][index] = True

        with open('mydata.json','w') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("请开始展示你的无知")
        ]))
        while True:
            content=await inc.wait(GroupMessageInterrupt(
                group, member,
                custom_judgement=lambda x: x.messageChain.asDisplay() is not None
            ))
            if content.messageChain.asDisplay().startswith("结束"):
                data['started_fanyi'][index] = False
                break
            # print(content)
            
            index=str(content.sender.group.id)+str(content.sender.id)
            if data['started_fanyi'][index] == False:
                continue

            reply = await getFanyi(content.messageChain.asDisplay())
            await app.sendGroupMessage(group,MessageChain.create([
                At(content.sender.id),Plain(reply)
            ]))
        # print(data)
        with open('mydata.json','w') as f:
            json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    content=message.asDisplay()
    index=str(group.id)+str(member.id)

    check = await checkxiaolan(content,index)
    if check == False:
        return

    f=open('mydata.json')
    data=json.load(f)
    data.setdefault("started_xiaolan",{})
    
    if index in data["started_xiaolan"] and data["started_xiaolan"][index]==True:
        await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(await chat(content))
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

app.launch_blocking()
loop.run_forever()
