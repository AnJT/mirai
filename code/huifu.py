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
    if message.asDisplay() == '?' or message.asDisplay() == '？':
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile('/root/mirai/code/img/wenhao.jpg')
        ]))
