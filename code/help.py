from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Face, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)

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
            Face(faceId=298),Plain('色图\n'),
            Face(faceId=298),Plain('福利\n'),
            Face(faceId=298),Plain('天气\n'),
            Face(faceId=298),Plain('翻译\n'),
            Face(faceId=298),Plain('丢\n'),
            Face(faceId=298),Plain('爬\n'),
            Face(faceId=298),Plain('nokia\n'),
            Face(faceId=298),Plain('课表\n'),
            Face(faceId=298),Plain('搜图\n'),
            Face(faceId=298),Plain("具体请help 功能")
        ]))

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("help"), RequireParam(name="saying")])
])
async def help_fun(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    content = ''.join(saying.asDisplay().lower().strip().split())
    if content == '成语接龙':
        reply = '成语接龙，指令为：接龙 [成语] 例如：接龙 一个顶俩 或者 接龙 俩'
    elif content == '选择':
        reply = '选择，指令为：选择[被选项] 例如：选择 1 2 3'
    elif content == 'compile':
        reply = '代码编译器，指令为：lang [语言]; [code] 例如 lang python; print("好耶")\n\
目前支持的语言有R,VB.NET,TypeScript,Kotlin,Pascal,Lua,Node.js,Go,Swift,Rust,Bash,Perl,Erlang,\
Scala,C#,Ruby,C++,C,Java,Python3,Python,PHP'
    elif content == 'guess':
        reply = '拼音首字母缩写释义，指令为：guess [首字母] 例如：guess yysy'
    elif content == '智能聊天':
        reply = '智能聊天,输入指令 二狗 即可开始聊天，输入指令 拜拜 or 再见 结束聊天，同时其他功能指令也会结束聊天，\
以便其他功能的使用'
    elif content == 'dailyenglish':
        reply = '每日英语，输入指令 daily english 即可获取一句每日英语，不准睡，快学！'
    elif content == '色图':
        reply = '色图，输入指令 色图 or 涩图 or 美女 or 来点色图 or 来点涩图 or 来点美女 即可获取一张色图\n\
输入指令 搜色图 [keyword] 例如 搜色图 黑丝 即可搜索色图\n \
输入指令 r18 on 即可开启r18模式，输入指令 r18 down 即可关闭'
    elif content == '福利':
        reply = '福利，输入指令 福利 or 来点福利 即可获取一张福利图'
    elif content == '天气':
        reply = '天气，输入指令 天气 获取当天天气状况，输入指令 天气预报 获取近四天天气状况'
    elif content == '翻译':
        reply = '翻译,输入指令 翻译 即可开启翻译，翻译支持图片翻译和文字翻译，输入指令 结束 来结束翻译，同时其他功能指令也会结束翻译，\
以便其他功能的使用'
    elif content == '丢':
        reply = '丢，输入指令 丢 @[一个人]，那就可以丢他了'
    elif content == '爬':
        reply = '爬，输入指令 爬 @[一个人]，那就可以让他爬了'
    elif content == 'nokia':
        reply = 'nokia，输入指令 nokia[句子]，即可得到一张nokia短信图片'
    elif content == '课表':
        reply = '课表，输入指令 课表，即可获取当天课表，输入指令 课表[1-7] 例如 课表 1 即可获取本周星期1的课表，输入指令 课表[1-7] [1-17]\
例如 课表 6 9 即可获取第9周星期六的课表\n输入修改学号 [学号]，即可修改学号'
    elif content == 'help':
        reply = '你指定是有什么大病'
    elif content == '搜图':
        reply = '搜图，输入指令 搜图，再发一张图片，即可搜索相似图片的详细信息'
    else:
        reply = '好小子，这个功能就交给你了'
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain('\n'),Face(faceId=298),Plain(reply)
    ]))
