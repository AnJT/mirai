from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import requests

url='http://202.120.163.129:88/Default.aspx'

def getElectricity():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless=True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    campus_value='9'
    building_value='20'
    floor_value='2005'
    room_value='200508'

    Select(driver.find_element_by_name('drlouming')).select_by_value(campus_value)
    Select(driver.find_element_by_name('drceng')).select_by_value(building_value)
    Select(driver.find_element_by_name('dr_ceng')).select_by_value(floor_value)
    Select(driver.find_element_by_name('drfangjian')).select_by_value(room_value)

    electricity_record=driver.find_element_by_id('usedR')
    electricity_record.click()
    login=driver.find_element_by_id('ImageButton1')
    login.click()

    remaining_battery=driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[1]/h6/span[1]').text
    return remaining_battery