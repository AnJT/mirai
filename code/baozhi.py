import asyncio
import json

import aiohttp
import re
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.scheduler.timers import (crontabify, every_custom_hours,
                                   every_custom_minutes, every_custom_seconds)
import random
import time
import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
from aiohttp import TCPConnector

from startup import app, bcc, scheduler, loop

ua = UserAgent().random

def get_proxy():
   return requests.get("http://127.0.0.1:5010/get/").json()

def get_new_headers():
   headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
             "Accept-Encoding": "gzip, deflate, br",
             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
             "User-Agent": ua}
   return headers

def get_new_cookies(proxies):
   url = 'https://v.sogou.com/v?ie=utf8&query=&p=40030600'
   # proxies = {"http": "http://" + '127.0.0.1:10808'}
   headers = {'User-Agent': ua}
   rst = requests.get(url=url,
                      headers=headers,
                      proxies=proxies,
                      allow_redirects=False)
   cookies = rst.cookies.get_dict()
   return cookies
   
async def news_result(html):
   month = str(datetime.datetime.now().month)
   day = str(datetime.datetime.now().day)
   soup = BS(html, 'html.parser')
   ul = soup.find(class_="news-list")
   for li in ul.find_all('li'):
       try:
           url = li.a['href']
           div = li.find_all('div')[1]

           # print(div.h3.a)
           res =  re.search(".*?今日简报.*?(\d+).*?(\d+).*", str(div.h3.a), re.S)
           # print(res.group(1))
           # print(res.group(2))
           # print(type(res.group(1)))
           if div.div.a.text == '易即今日' and res.group(1) == month and res.group(2) == day:
               return url
           # print(div.div.a.text)
       except Exception as e:
           print(e)

async def url_decode(r): 
   url = 'https://weixin.sogou.com' + r
   b = random.randint(0, 99)
   a = url.index('url=')
   a = url[a + 30 + b:a + 31 + b:]
   url += '&k=' + str(b) + '&h=' + a
   return url

async def getBriefing():
   proxy = get_proxy().get("proxy")
   proxy_url = "http://{}".format(proxy)
   proxies={"http": "http://{}".format(proxy)}
   timeout = aiohttp.ClientTimeout(total=60)
   connector = aiohttp.TCPConnector(limit=50, ssl=False)
   async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
       month = datetime.datetime.now().month
       day = datetime.datetime.now().day
       query = f'今日简报({month}月{day}日)易即今日'
       # print(query)
       url = 'https://weixin.sogou.com/weixin'
       params = {
           'type': 2,
           's_from': 'input',
           'ie': 'uft8',
           '_sug_': 'n',
           '_sug_type_': '',
           'query': query
       }
       headers = get_new_headers()
       cookies = get_new_cookies(proxies)
       async with session.get(url=url, params=params, proxy=proxy_url, headers=headers, cookies=cookies, ssl=False) as resp:
           html = await resp.text()  
           # print(html)
           url = await news_result(html)
           url = await url_decode(url)
           # print(url)
       params = {
           'wx_fmt': 'jpeg'
       }  
       # print(cookies)
       async with session.get(url=url, params=params, proxy=proxy_url, ssl=False, cookies=cookies, headers=headers) as resp:
           text = await resp.text()
           # print(text)
           pattern = r"url \+= '(.*?)';"
           url_list = re.finditer(pattern, text, re.S)
           # print(url_list)
           url = ''
           for u in url_list:
               url += u.group(1)
           url = url.replace('http', 'https')
           # print(url)
       async with session.get(url=url, params=params, proxy=proxy_url, ssl=False, cookies=cookies, headers=headers) as resp:
           text = await resp.text()
           bs = BS(text, "html.parser")
           url = bs.find('div', id='img_list').img.get('src')
           # print(url)
       async with session.get(url=url,  ssl=False, cookies=cookies, proxy=proxy_url, headers=headers) as resp:
           with open('./img/picture.png', 'wb') as file:
               bs = await toBtyes(resp)
               file.write(bs)
   return 'img/picture.jpg'


async def toBtyes(resp):
   empty_bytes = b''
   result = empty_bytes
   while True:
       chunk = await resp.content.read(8)
       if chunk == empty_bytes:
           break
       result += chunk
   return result


@scheduler.schedule(every_custom_minutes(30))
async def daily_briefing_scheduled():
   # f=open('./json/mydata.json')
   # data=json.load(f)
   for _ in range(20):
       try:
           img_path = await getBriefing()
           break
       except Exception as e:
           pass
   # await app.sendGroupMessage(data['group']["1020661362"], MessageChain.create([
   #     Image.fromLocalFile(img_path)
   # ]))
   # f.close()

#loop.run_until_complete(getBriefing())

@bcc.receiver("GroupMessage")
async def daily_briefing(
   message: MessageChain,
   app: GraiaMiraiApplication,
   group: Group, member: Member,
):  
   if ''.join(message.asDisplay().lower().strip().split()) == "今日简报":
       url = './img/picture.png'
       # print(url)
       await app.sendGroupMessage(group, MessageChain.create([
           Image.fromLocalFile(url)
       ]))
