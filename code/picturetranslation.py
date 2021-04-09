import base64
import json

import requests
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import models, tmt_client


def get_as_base64(url):
    res =  base64.b64encode(requests.get(url).content)
    return str(res, 'utf8')

def GetReply(url):
    try: 
        cred = credential.Credential("AKIDTigOt70mD0NUKvEOmqa5LK3B3f192H8P", "C8NLmwqUryeKjvEH5cs0h8J5JWpIVaQz") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile) 

        req = models.ImageTranslateRequest()
        params = {
            "SessionUuid": "qwer",
            "Scene": "doc",
            "Data": "",
            "Source": "auto",
            "Target": "zh",
            "ProjectId": 0
        }
        bs = get_as_base64(url)
        params['Data'] = bs
        req.from_json_string(json.dumps(params))

        resp = client.ImageTranslate(req) 
        resp = resp.to_json_string()
        resp = json.loads(resp)['ImageRecord']['Value'][0]
        reply = resp['SourceText'] + '\n' + resp['TargetText']
        return reply

    except TencentCloudSDKException as err: 
        print(err)
