import pytesseract
import requests
from PIL import Image, ImageEnhance


def convert_img(url):
    img = Image.open(requests.get(url, stream=True).raw)
    img=img.convert('RGB')
    enhancer = ImageEnhance.Color(img)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    img = enhancer.enhance(20)
    return img
#识别图片验证码
def getCaptcha(url):
    result=convert_img(url)
    # result.show()
    result=pytesseract.image_to_string(result)
    print(result)
    return result

# getCaptcha(url)
