import time

import requests
from bs4 import BeautifulSoup
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from startup import bcc

url='http://202.120.163.129:88/Default.aspx'
headers={
    'Cookie':'ASP.NET_SessionId=3qqehnbxppz1x3qtjebzobwg',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}

def GetElectricity():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless=True
    #这样设置请求头
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"')
    driver = webdriver.Chrome(options=chrome_options)
    # 可恶，这个库不是这样设置请求头
    # driver.get(url,headers=headers)
    driver.get(url)
    
    WAIT=WebDriverWait(driver,10)

    campus_value='9'
    building_value='20'
    floor_value='2005'
    room_value='200508'
    
    campus=WAIT.until(EC.presence_of_element_located((By.NAME,'drlouming')))
    Select(campus).select_by_value(campus_value)
    building=WAIT.until(EC.presence_of_element_located((By.NAME,'drceng')))
    Select(building).select_by_value(building_value)
    floor=WAIT.until(EC.presence_of_element_located((By.NAME,'dr_ceng')))
    Select(floor).select_by_value(floor_value)
    room=WAIT.until(EC.presence_of_element_located((By.NAME,'drfangjian')))
    Select(room).select_by_value(room_value)

    electricity_record=WAIT.until(EC.element_to_be_clickable((By.ID,'usedR')))
    electricity_record.click()
    login=WAIT.until(EC.element_to_be_clickable((By.ID,'ImageButton1')))
    login.click()
    
    # html=driver.page_source
    # soup=BeautifulSoup(html,'lxml')
    # print(soup)
    remaining_battery=WAIT.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[3]/div[2]/div[1]/h6/span[1]')))
    return remaining_battery.text+'度'


@bcc.receiver("GroupMessage")
async def DianFei(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if not group.id==1020661362:
        return
    if message.asDisplay().startswith('电费'):
        elec=GetElectricity()
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain(elec)
        ]))
