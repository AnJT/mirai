import random
import ssl
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

from startup import bcc

ssl._create_default_https_context = ssl._create_unverified_context


url = ['https://api.nmb.show/xiaojiejie1.php','http://api.nmb.show/xiaojiejie2.php ']


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
    # cv2.imwrite('/root/mirai/code/img/1.png',image, [int( cv2.IMWRITE_JPEG_QUALITY), 95])
    return image

def get_bytes():
    fuli_url = random.choice(url)
    fuli_img = url_to_image(fuli_url)
    img_b = cv2.imencode('.png', fuli_img)[1].tobytes()
    return img_b

@bcc.receiver("GroupMessage")
async def fuli(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    content=message.asDisplay()
    if content =='福利' or content =='来点福利':
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Image.fromUnsafeBytes(get_bytes())
        ]))
