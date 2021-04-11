import os
import random
import urllib.request as request

import cv2
import numpy as np
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RequireParam)
from PIL import Image as IMG

from startup import bcc

# print(os.getcwd())
img_url = 'http://q1.qlogo.cn/g?b=qq&nk=##&s=100'


# URL到图片
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = request.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

# 图像处理，获取图片最大内接圆，其他区域置为透明
def img_deal(img):
    # cv2.IMREAD_COLOR，读取BGR通道数值，即彩色通道，该参数为函数默认值
    # cv2.IMREAD_UNCHANGED，读取透明（alpha）通道数值
    # cv2.IMREAD_ANYDEPTH，读取灰色图，返回矩阵是两维的
    rows, cols, channel = img.shape

    # 创建一张4通道的新图片，包含透明通道，初始化是透明的
    img_new = np.zeros((rows,cols,4),np.uint8)

    img_new[:,:,0:3] = img[:,:,0:3]
    # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
    img_circle = np.zeros((rows,cols,1),np.uint8)
    img_circle[:,:,:] = 0  # 设置为全透明

    img_circle = cv2.circle(img_circle,(cols//2,rows//2),min(rows, cols)//2,(255),-1) # 设置最大内接圆为不透明

    # 图片融合
    img_new[:,:,3] = img_circle[:,:,0]
    # 显示图片，调用opencv展示
    # cv2.imshow("img_new", img_new)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return img_new

def get_bytes(qq):
    pa_url = '/root/mirai/code/img/pa'
    pa_url += str(random.randint(1, 9)) + '.png'
    pa_img = cv2.imread(pa_url, cv2.IMREAD_UNCHANGED)
    qq_img = url_to_image(img_url.replace('##',qq))
    if pa_img.shape[2]==4:
        qq_img = img_deal(qq_img)
    for i in range(100):
        for j in range(100):
            if (50-i)**2+(50-j)**2 > 50**2:
                continue
            pa_img[i+400][j]=qq_img[i][j]
    img_b = cv2.imencode('.png', pa_img)[1].tobytes()
    return img_b

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([FullMatch("爬"), RequireParam(name="saying")])
])
async def pa(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    try:
        at = saying.get(At)
        for i in at:
            qq = i.target
            bs = get_bytes(str(qq))
            # print(type(bs))
            await app.sendGroupMessage(group, MessageChain.create([
                Image.fromUnsafeBytes(bs)
            ]))
    except:
        pass

