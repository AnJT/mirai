from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Face, Plain

from startup import bcc


@bcc.receiver("GroupMessage")
async def help(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if ''.join(message.asDisplay().lower().strip().split()) == "help":
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain('\n'),Face(faceId=298),Plain('成语接龙\n'),
            Face(faceId=298),Plain('选择\n'),
            Face(faceId=298),Plain('compile\n'),
            Face(faceId=298),Plain('guess\n'),
            Face(faceId=298),Plain('智能聊天\n'),
            Face(faceId=298),Plain('daily english\n'),
            Face(faceId=298),Plain('青年大学习\n'),
            Face(faceId=298),Plain('毒鸡汤\n'),
            Face(faceId=298),Plain('leetcode\n'),
            Face(faceId=298),Plain('色图\n'),
            Face(faceId=298),Plain('天气\n'),
            Face(faceId=298),Plain('翻译\n'),
            Face(faceId=298),Plain("具体请help 功能")
        ]))
