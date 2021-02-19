import asyncio
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import At, Plain
from graia.application.session import Session
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member
from graia.broadcast.interrupt import InterruptControl
from graia.application.interrupts import GroupMessageInterrupt

from startup import bcc,inc,app

@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    if message.asDisplay().startswith("test"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("发送 yes 以继续运行")
        ]))
        await inc.wait(GroupMessageInterrupt(
            group, member,
            custom_judgement=lambda x: x.messageChain.asDisplay().startswith("yes")
        ))
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("执行完毕.")
        ]))

app.launch_blocking()