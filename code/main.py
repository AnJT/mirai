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

from captcha import getCaptcha
from choice import Choice
from dailyenglish import DailyEnglish
from electricity import DianFei
from fanyi import FanYi
from jitang import JiTang
from setu import SeTu, SeTuDB
from startup import app, bcc, inc, loop, scheduler
from xiaolan import XiaoLan

app.launch_blocking()
loop.run_forever()
