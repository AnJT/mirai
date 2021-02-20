import asyncio
from graia.application.event.messages import SourceElementDispatcher
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import At, Plain,Image
from graia.application.session import Session
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, OptionalParam, RequireParam
import random
from graia.application.interrupts import GroupMessageInterrupt
from startup import bcc,inc,app,scheduler,loop
from xiaolan import chat
from electricity import getElectricity
from graia.scheduler.timers import crontabify
import json


@bcc.receiver("GroupMessage")
async def group_message_database_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    f=open('mydata.json')
    data=json.load(f)
    data['group'][str(group.id)]=group.id
    data['friend'][str(member.id)]=member.id
    print(data)
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

@scheduler.schedule(crontabify("23 11 * * *"))
async def ddl_scheduled():
    print("11:01")
    f=open('mydata.json')
    data=json.load(f)
    await app.sendGroupMessage(data['group']["1020661362"], MessageChain.create([
        At(342472121),Plain("时间到了！")
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
    content=saying.asDisplay()
    img_path="img\\"
    if "美女" in content or "色图" in content or "涩图" in content:
        img_path+="s"+str(random.randint(1,5))+'.jpg'
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromLocalFile(img_path)
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
    content=message.asDisplay()
    index=str(group.id)+str(member.id)
    if content.startswith("来点") or content.startswith("选择") or content.startswith("ddl") or content.startswith("电费"):
        return

    f=open('mydata.json')
    data=json.load(f)
    data.setdefault("started_xiaolan",{})

    if index in data["started_xiaolan"] and data["started_xiaolan"][index]==True:
        await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(chat(content))
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