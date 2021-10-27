import json

import requests
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)

from startup import bcc


def get_guess(text):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    data = {
        'text' : text
    }
    response = requests.post(url, data=data, headers=headers)
    response = json.loads(response.content)
    result = text + ' maybe:\n'
    try:
        results = response[0]['trans']
    except KeyError:
        results = response[0]['inputting']
    if len(results) == 0:
        result += '啥也不是'
    else:
        for i in results:
            result += i + '\n'
        result = result[:-1]
    return result

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("guess"), RequireParam(name="saying")])
])
async def guess(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    words = ''.join(saying.asDisplay().lower().strip().split())
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(get_guess(words))
    ]))
