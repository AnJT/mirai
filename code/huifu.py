import os
import random

from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain

from startup import bcc


@bcc.receiver("GroupMessage")
async def huifu(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    print(message.asDisplay())
    if message.asDisplay() == '@246987206':
        file_num = 52
        file_name = "img/at/" + str(random.randint(0, file_num)) +'.png'
        print(file_name)
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile(file_name)
        ]))
