import sys

from chat import xiaolan
from chengyu import chengyu
from choice import choice
from compile import compile
from courses import courses_db, courses_search, courses
# from electricity import search_elec, search_elec2, update_scheduled
from dailyenglish import daily_english
from baozhi import daily_briefing
from diu import diu
from fanyi import fanyi
from fuli import fuli
from guess import guess
from help import help, help_fun
from huifu import huifu
from image_search import image_search
from nokia import nokia
from pa import pa
from setu import setu, setu_db
from startup import app, loop
from weather import weather

app.launch_blocking()
loop.run_forever()
