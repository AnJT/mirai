import sys

from chat import xiaolan
from chengyu import chengyu
from choice import choice
from compile import compile
from courses import courses_db, courses_search, get_courses
from dailyenglish import daily_english
from daxuexi import daxuexi, daxuexi_remind, get_reply
from diu import diu
from fanyi import fanyi
from fuli import fuli
from guess import guess
from help import help, help_fun
from huifu import huifu
from image_search import image_search
from jinyan import jinyan
from lc import daily_lc, daily_lc_scheduled
from nokia import nokia
from pa import pa
from rubbish import rubbish
from setu import setu, setu_db
from startup import app, loop
from weather import weather

app.launch_blocking()
loop.run_forever()
