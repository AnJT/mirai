import json
import time

from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain

from startup import bcc


@bcc.receiver("GroupMessage")
async def jinyan(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    f=open('mydata.json')
    data=json.load(f)
    f.close()

    data.setdefault("jinyan",{})
    idx = str(group.id) + str(member.id)
    data['jinyan'].setdefault(idx, [])

    ntime = time.time()
    times= []
    for i in data['jinyan'][idx]:
        if ntime-i<3.0:
            times.append(i)
    times.append(ntime)
    data['jinyan'][idx] = times
    if len(times) > 5:
        try:
            if idx in data['jinyaned']:
                try:
                    # 已经设置禁言，无需再禁
                    if time.time()-data['jinyaned'][idx]<60.0:
                        return
                except:
                    pass
            # 设置禁言
            await app.mute(group, member, 60)
            data['jinyaned'][idx] = time.time()
        # 无权限
        except:
            pass

    with open('mydata.json','w+') as f:
        json.dump(data,f,ensure_ascii=False, indent=4, separators=(',', ':'))
