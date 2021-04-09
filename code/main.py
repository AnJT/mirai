import asyncio
import json
import random

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
from chat import XiaoLan
from chengyu import Chengyu
from choice import Choice
from compile import Compile
from dailyenglish import DailyEnglish
from daxuexi import DaxuexiRemind
from electricity import DianFei
from fanyi import FanYi
from guess import Guess
from jinyan import Jinyan
from jitang import JiTang
from lc import GetDailyQuestion
from setu import SeTu, SeTuDB
from startup import app, bcc, inc, loop, scheduler
from weather import Weather

app.launch_blocking()
loop.run_forever()
