import asyncio

import yaml
from graia import scheduler
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.interrupts import GroupMessageInterrupt
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.application.session import Session
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify

setting_yml_path='../config/net.mamoe.mirai-api-http/setting.yml'
with open(setting_yml_path) as f:
    setting=yaml.load(f,yaml.BaseLoader)

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop,debug_flag=False)

scheduler=GraiaScheduler(
    loop,bcc
)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=f"http://{setting['host']}:{setting['port']}",
        authKey=f"{setting['authKey']}",
        account=setting['qq'],
        websocket=setting['enableWebsocket']
    )
)
inc=InterruptControl(bcc)
