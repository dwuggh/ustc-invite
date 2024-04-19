from USTCLogin import login
import re
import base64
from datetime import datetime, timedelta

# departments' name and code
def getsysdeptlist(session):
    resp = session.get("https://bwcqyrx.ustc.edu.cn/rest/dept/getsysdeptlist")
    return resp.json()["data"]

def makeUsers(user_list):
    userinfo = []
    for name, phone, id in user_list:
        user = {
            "userName": name,
            "userPhone": phone,
            "applyArea":"",
            "areaId":"",
            "carType":"CardType1",
            "cardTypeName":"身份证",
            "cardNo": id,
            "isDanger":0,
            "akCode":"",
            "tripCode":"",
            "naCode":"",
            "hasCar":0,
            "carModelName":"",
            "passPlace":[],
            "passPlaceName":[]
        }
        userinfo.append(user)
    return userinfo

class Inviter(object):

    def __init__(self, uid, password, phone):
        resp, session = login(uid, password,  "https://bwcqyrx.ustc.edu.cn/weixin/validate")
        self.session = session
        self.openid = re.search(r'openId=(.*?)&', resp.url).group(1)
        self.name = re.search(r'concatName=(.*?)&', resp.url).group(1)
        self.wage = re.search(r'concatWage=(.*?)&', resp.url).group(1)
        self.gid = re.search(r'concatGid=(.*?)&', resp.url).group(1)
        self.phone = phone
        # gid = base64.b64decode(gid.encode('ascii')).decode('ascii')

    def send_invite(self, users, date):
        num = len(users)
        form = {
            # null for the 3 enties
            "checkUserName": "",
            "checkUserGid": "",
            "checkUserEmail": "",

            "inviteCode": "",
            "userInfo": users,
            "departName": "物理学院",
            "deptId": "1280316282751528961",
            "concatName": self.name,
            "concatPhone": self.phone,
            "campus": "西校区 中校区 南校区 北校区 高新校区",
            "campusId": "Campus4,Campus5,Campus1,Campus2,Campus7",
            "campusDoor": "",
            "enrolledReason": "访问",
            "concatGid": self.gid,
            "concatWage": self.wage,
            "hasCar": False,
            "openId": self.openid,
            "userNum": num,
            "carNum": 0,
            "enrolledDate": date,
            "endTime": date,
            "enrolledHour": 0,
            "endDate": date,
            "enrolledDateTime": 0,
            "enrolledTime": date,
            "source": "0"
        }
        # print(form)
        resp = self.session.post("https://bwcqyrx.ustc.edu.cn/zkd/qy/apply", json = form)
        print(resp.json())


def read_inviters(filename):
    inviters = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            uid, password, phone = line.strip().split()
            inviter = Inviter(uid, password, phone)
            inviters.append(inviter)

    return inviters


def read_users(filename):
    users = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            name, phone, id = line.strip().split()
            users.append((name, phone, id))

    print("reading users: ", users)
    return makeUsers(users)

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inviters", required=True)
    parser.add_argument("-u", "--users", required=True)
    parser.add_argument("-d", "--date", help="number of days after today or any date in YYYY-MM-DD", required=True)
    args = vars(parser.parse_args())
    inviters_filename = args['inviters']
    users_filename = args['users']
    date = args['date']
    try:
        advance_days = int(date)
    except:
        pass
    else:
        current_date = datetime.now().date()
        target_date = current_date + timedelta(days=advance_days)
        date = target_date.strftime("%Y-%m-%d")
        
    inviters = read_inviters(inviters_filename)
    users = read_users(users_filename)
    print("invite date: ", date)

    for i, inviter in enumerate(inviters):
        start = i * 5
        if start >= len(users):
            break
        end = i * 5 + 5
        end = len(users) if end > len(users) else end
        inviter.send_invite(users[start:end], date)
