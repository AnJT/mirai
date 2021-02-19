import requests,json

url='http://openapi.tuling123.com/openapi/api/v2'
def chat(content):
    data={
        "reqType":0,
        "perception": {
            "inputText": {
                "text": content
            },
            "inputImage": {
            "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "石家庄市",
                    "province": "河北省",
                    "street": "慈峪镇"
                }
            }
        },
        "userInfo": {
            "apiKey": "644619ad0e5442b58785b2beb32e1fb4",
            "userId": "ajtbot"
        }
    }
    data=json.dumps(data)
    # 图灵接口接收的是json格式，而上面创建的data是字典，所以需要格式转化
    res=requests.post(url,data=data)
    result=res.json()
    for reply in result['results']:
        return reply['values']['text']
