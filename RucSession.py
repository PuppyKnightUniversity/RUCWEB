import requests
import ddddocr
import re
import base64
import os,sys
# 获取session
# userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
codeurl = 'https://v.ruc.edu.cn/auth/captcha' # 请求验证码的url
loginurl = "https://v.ruc.edu.cn/auth/login"
class Session(object):
    # RUC系列的session
    def __init__(self,userAgent, stuid, pwd, name):
        print('Session init processing')
        self.session = requests.session()
        self.userAgent = userAgent
        self.headers = {'User-Agent': self.userAgent}
        self.islogin = False
        while(not self.islogin):
            if(self.login(loginurl, stuid, pwd, name)):
                self.islogin = True
        print('Login: SUCESS')
        self.cookies = self.session.cookies
        #print(self.cookies)
        #print(self.session.cookies)


    def OCR_code(self, codeurl):
        """
        识别验证码
        :return: 验证码string
        """
        valcode = self.session.get(url=codeurl, headers=self.headers)
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*?)\"", valcode.text, re.DOTALL)
        codeid = re.search("id\":\"(?P<id>.*?)\"", valcode.text, re.DOTALL).groupdict().get("id")
        # print(codeid)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")
            img = base64.urlsafe_b64decode(data)
            filename = "{}.{}".format('test', ext)
            with open(filename, "wb") as f:
                f.write(img)
            print("Captcha Obtain: SUCCESS")
            # 验证码识别
            sys.stdout = open(os.devnull, 'w')
            ocr = ddddocr.DdddOcr()
            with open('test.png', 'rb') as f:
                img_bytes = f.read()
            res = ocr.classification(img_bytes)
            sys.stdout = sys.__stdout__
            # print(res)
            return res,codeid

    def login(self, posturl, stuid, pwd, name):
        """
        登录验证
        :param self:
        :return:
        """
        print("RUC logining.....")
        code,codeid = self.OCR_code(codeurl)
        rucusr = 'ruc:'+stuid
        postData = {
            "username": rucusr,
            "password": pwd,
            "code": code,
            "remember_me": "true",
            "redirect_uri": "http://appointment.ruc.edu.cn/",
            "twofactor_password": "",
            "twofactor_recovery": "",
            # "token": "ovpzugqi8v",
            "captcha_id": codeid}
        #print(postData)
        responseRes = self.session.post(posturl, json=postData, headers=self.headers)
        #print(responseRes.status_code)
        #print(responseRes.text)
        if responseRes.status_code == 200:
            # 继续跳转
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,mn;q=0.8,zh-TW;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Origin': 'http://appointment.ruc.edu.cn',
                'Referer': 'http://appointment.ruc.edu.cn/index/ruclogin/backurl?code=ywd346VJR_G4tLqvzSUGCA&state=soogee',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            }
            # 学号姓名选择
            data = {
                'stno': stuid,
                'name': name,
            }

            response = self.session.post('http://appointment.ruc.edu.cn/index/ruclogin/morelist', headers=headers,
                                         data=data,
                                         verify=False)
            return True
        else:
            return False

    def appointment(self, NAME, TEL, IDCARD, SEX, TIME):
        cookies = self.cookies
        #cookies = self.cookies
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,mn;q=0.8,zh-TW;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'PHPSESSID=r1rcqd7tn05jrr86vdl4rlp1km; access_token=e_ZCatb1QzuIIrroy6Cg8Q; tp_yyts=0',
            'Origin': 'http://appointment.ruc.edu.cn',
            'Referer': 'http://appointment.ruc.edu.cn/index/apply/apply/RULEID/364',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        data = {
            'NAME': NAME,
            'TEL': TEL,
            'IDCARD': IDCARD,
            'CARDTYPE': '身份证',
            'SEX': SEX,
            'CARNUM': '',
            'AUTHONEPEO': '',
            'DOTOP': '0',
            'RULEID': '364',
            'OUTREACON': '2901',
            'RESON': '亲友来访',
            'QJT': '',
            'INFOTYPE': '5',
            'INTOGATE': '50',
            'DAYS': '',
            'COLOR': '',
            'RESONTYPE': '有临时入校需求的访客',
            'INFO': '确认,确认,确认',
            'BEIZHU': '',
            #'2023-03-13'
            'all_times_str': TIME,
            'all_INTODUAN_str': 'all',
            'all_times_str1': '',
            'all_INTODUAN_str1': '',
        }

        response = requests.post(
            'http://appointment.ruc.edu.cn/index/apply/apply',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,mn;q=0.8,zh-TW;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'PHPSESSID=r1rcqd7tn05jrr86vdl4rlp1km; access_token=e_ZCatb1QzuIIrroy6Cg8Q; tp_yyts=0',
            'Origin': 'http://appointment.ruc.edu.cn',
            'Referer': 'http://appointment.ruc.edu.cn/index/apply/apply/RULEID/364',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        data = {
            'NAME': NAME,
            'TEL': TEL,
            'IDCARD': IDCARD,
            'CARDTYPE': '身份证',
            'SEX': SEX,
            'CARNUM': '',
            'AUTHONEPEO': '20209615',
            'DOTOP': '0',
            'RULEID': '364',
            'OUTREACON': '2901',
            'RESON': '亲友来访',
            'QJT': '',
            'INFOTYPE': '5',
            'INTOGATE': '50',
            'DAYS': '',
            'COLOR': '',
            'RESONTYPE': '有临时入校需求的访客',
            'INFO': '确认,确认,确认',
            'BEIZHU': '',
            'all_times_str': TIME,
            'all_INTODUAN_str': 'all',
            'all_times_str1': '',
            'all_INTODUAN_str1': '',
        }

        response = requests.post(
            'http://appointment.ruc.edu.cn/index/apply/apply',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )

        return (response.text)
if __name__ == '__main__':
    session = Session()
    session.test()