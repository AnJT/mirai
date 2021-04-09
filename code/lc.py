# coding=<encoding name> ： # coding=utf-8
import asyncio
import json
from datetime import datetime

import aiohttp
import requests
from bs4 import BeautifulSoup
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
from graia.scheduler.timers import (crontabify, every_custom_hours,
                                    every_custom_minutes, every_custom_seconds)

from startup import app, bcc, scheduler


def get_daily_question(lc='leetcode'):
    base_url = 'https://leetcode-cn.com'

    response = requests.post(base_url + "/graphql", json={
        "operationName": "questionOfToday",
        "variables": {},
        "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
    })
    leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')

    url = base_url + "/problems/" + leetcodeTitle
    response = requests.post(base_url + "/graphql",
                            json={"operationName": "questionData", "variables": {"titleSlug": leetcodeTitle},
                                "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
    jsonText = json.loads(response.text).get('data').get("question")

    no = jsonText.get('questionFrontendId')
    leetcodeTitle = jsonText.get('translatedTitle')
    level = jsonText.get('difficulty')
    context = jsonText.get('translatedContent')
    context = BeautifulSoup(context,'html.parser').get_text()
    if lc == 'lc':
        result = '狗都不做之lc每日一题:\n'+no+"."+leetcodeTitle+'.'+level+'\n'+\
        '本题链接:'+url
        return result
    result = '狗都不做之lc每日一题:\n'+no+"."+leetcodeTitle+'.'+level+'\n'+context+\
        '本题链接:'+url
    return result

@scheduler.schedule(crontabify("00 00 * * *"))
async def daily_lc_scheduled():
    f=open('mydata.json')
    data=json.load(f)
    await app.sendGroupMessage(data['group']["1020661362"], MessageChain.create([
        Plain(get_daily_question())
    ]))
    f.close()

@bcc.receiver("GroupMessage")
async def daily_lc(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):  
    if ''.join(message.asDisplay().lower().strip().split()) == "lc":
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(get_daily_question('lc'))
        ]))
    elif ''.join(message.asDisplay().lower().strip().split()) == "leetcode":
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain(get_daily_question())
        ]))
