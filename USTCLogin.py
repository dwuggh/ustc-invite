import requests
from bs4 import BeautifulSoup
import re

def login(stuid, password, service, headers={}):
    session = requests.session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; Google Nexus 5X Build/NBD92Y; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 MMWEBID/2579 MicroMessenger/8.0.2.1860(0x28000236) Process/appbrand0 WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm32 miniProgram',
    })
    session.headers.update(headers)
    
    url = "https://passport.ustc.edu.cn/login"
    resp = session.get(url, params={
        "service": service
        })

    data = resp.text.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # soup = BeautifulSoup(data, 'html.parser')
    # CAS_LT = soup.find("input", id="CAS_LT")['value'] # type: ignore
    CAS_LT = re.search(r'\("#CAS_LT"\)\.val\("(.*?)"\)', data).group(1)
    # print(CAS_LT)
    
    session.cookies.set('lang', 'zh')

    showCode = re.search("showCode = '1'", data)
    if showCode is not None:
        import cv2
        import numpy as np
        import pytesseract

        validate_url = "https://passport.ustc.edu.cn/validatecode.jsp?type=login"
        resp = session.get(validate_url, stream=True);
        # print(resp.status_code)
        # print(type(resp.content))
        
        img = np.asarray(bytearray(resp.content), dtype='uint8')
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        custom_oem_psm_config = r'--psm 9'
        lt = pytesseract.image_to_string(img, config=custom_oem_psm_config).strip()
        # print("validate code is {}".format(lt))

    data = {
        'model': 'uplogin.jsp',
        'CAS_LT': CAS_LT,
        'service': service,
        'username': str(stuid),
        'password': str(password),
        'warn': '',
        'qrcode': '',
        'resultInput': '',
        'showCode': '' if showCode is None else '1',
        'LT': lt,
    }

    resp = session.post(url, data=data)
    # print(resp.status_code)
    # print(resp.url)

    return resp, session
