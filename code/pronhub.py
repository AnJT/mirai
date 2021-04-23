import base64
import random
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from graia.application import GraiaMiraiApplication
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)
from lxml import etree
from PIL import Image as IMG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from startup import bcc

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

proxies = { "http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809", } 
proxy = '127.0.0.1:10809'
url = 'https://cn.pornhub.com/'
url_search = 'https://www.pornhub.com/video/search?search='

async def get_search(keyword):
    k_url = url_search + keyword
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless=True
    #chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"')
    driver = webdriver.Chrome(options=chrome_options)
    #driver.implicitly_wait(5)
    driver.get(k_url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    ul=driver.find_element_by_xpath('//ul[@class="videos search-video-thumbs"]')
    lis = ul.find_elements_by_xpath('li[@class="pcVideoListItem js-pop videoblock videoBox"]')
    lis = random.sample(lis, 2)
    result = []
    for li in lis:
        title = li.find_element_by_xpath('div/div[3]/span/a').text
        href = li.find_element_by_xpath('div/div[1]/a').get_attribute('href')
        img_src = li.find_element_by_xpath('div/div[1]/a/img').get_attribute('src')
        result.append((title, href, img_src))
    return result
    # 以下为requests方法，由于动态加载的原因，无法获取未加载的信息
    # html=requests.get(k_url,headers=headers,proxies=proxies)
    # html = etree.HTML(html.content)

    # ul = html.xpath('//ul[@class="videos search-video-thumbs"]')[0]
    # lis = ul.xpath('li[@class="pcVideoListItem js-pop videoblock videoBox"]')
    # for li in lis:
    #     title = li.xpath('div/div[3]/span/a/@title')[0]
    #     href = 'https://cn.pornhub.com'+ li.xpath('div/div[1]/a/@href')[0]
    #     img_src = li.xpath('div/div[1]/a/img/@src')[0]
    #     print(href, img_src)

async def get_popular():
    html=requests.get(url,headers=headers,proxies=proxies)
    html = etree.HTML(html.content)

    ul = html.xpath('//ul[@class="videos-morepad videos full-row-thumbs videos-being-watched logInHotContainer"]')[0]
    lis = ul.xpath('li[@class="pcVideoListItem js-pop videoblock videoBox"]')
    lis = random.sample(lis, 2)
    result = []
    for li in lis:
        title = li.xpath('div/div[3]/span/a/@title')[0]
        href = 'https://cn.pornhub.com' + li.xpath('div/div[1]/a/@href')[0]
        img_src = li.xpath('div/div[1]/a/img/@src')[0]
        result.append((title, href, img_src))
    return result

@bcc.receiver("FriendMessage")
async def pronhub(
    message: MessageChain,
    app: GraiaMiraiApplication,
    friend: Friend
):
    content=message.asDisplay()
    if content == 'pronhub':
        result = await get_popular()
        reply = []
        for i in result:
            reply.append(Plain("title:" + i[0] + '\n'))
            reply.append(Plain("url:" + i[1] + '\n'))
            # reply.append(Image.fromNetworkAddress(i[2]))
            reply.append(Plain("img_src:" + i[2]+'\n'))
        await app.sendFriendMessage(friend, MessageChain.create(
            reply
        ))

@bcc.receiver("FriendMessage", dispatchers=[
    Kanata([FullMatch("pronhub"), RequireParam(name="saying")])
])
async def pronhub_search(
    message: MessageChain,
    app: GraiaMiraiApplication,
    friend: Friend,
    saying: MessageChain
):
    content = saying.asDisplay().strip()
    print(content)
    result = await get_search(content)
    print(result)
    reply = []
    for i in result:
        reply.append(Plain("title:" + i[0] + '\n'))
        reply.append(Plain("url:" + i[1] + '\n'))
        # reply.append(Image.fromNetworkAddress(i[2]))
        reply.append(Plain("img_src:" + i[2]+'\n'))
    await app.sendFriendMessage(friend, MessageChain.create(
        reply
    ))

@bcc.receiver("GroupMessage")
async def pronhub_group(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member
):
    content=message.asDisplay()
    if content == 'pronhub':
        result = await get_popular()
        reply = []
        for i in result:
            reply.append(Plain("title:" + i[0] + '\n'))
            reply.append(Plain("url:" + i[1] + '\n'))
            # reply.append(Image.fromNetworkAddress(i[2]))
            reply.append(Plain("img_src:" + i[2]+'\n'))
        await app.sendGroupMessage(group, MessageChain.create(
            reply
        ))

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("pronhub"), RequireParam(name="saying")])
])
async def pronhub_search_group(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    content = saying.asDisplay().strip()
    print(content)
    result = await get_search(content)
    print(result)
    reply = []
    for i in result:
        reply.append(Plain("title:" + i[0] + '\n'))
        reply.append(Plain("url:" + i[1] + '\n'))
        # reply.append(Image.fromNetworkAddress(i[2]))
        reply.append(Plain("img_src:" + i[2]+'\n'))
    await app.sendGroupMessage(group, MessageChain.create(
        reply
    ))
