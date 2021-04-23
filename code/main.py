import sys

from chat import xiaolan
from chengyu import chengyu
from choice import choice
from compile import compile
from courses import courses_db, courses_search, get_courses
from dailyenglish import daily_english
from daxuexi import daxuexi, daxuexi_remind, get_reply
from diu import diu
# from electricity import dianfei
from fanyi import fanyi
from fuli import fuli
from guess import guess
from help import help, help_fun
from huifu import huifu
from jinyan import jinyan
from jitang import jitang
from lc import daily_lc, daily_lc_scheduled
from nokia import nokia
from pa import pa
from pronhub import (pronhub, pronhub_group, pronhub_search,
                     pronhub_search_group)
from setu import setu, setu_db
from startup import app, loop
from weather import weather

app.launch_blocking()
loop.run_forever()
