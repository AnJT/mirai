from io import BytesIO

import requests
from PIL import Image as IMG

img_url = 'http://q1.qlogo.cn/g?b=qq&nk=342472121&s=640'

response = requests.get(img_url)
image = IMG.open(BytesIO(response.content))
image.show()
