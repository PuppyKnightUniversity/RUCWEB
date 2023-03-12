import config
import RucSession
import time
from utils import send_wechat
import datetime
class RUC(object):
    def __init__(self):

        self.config = config.Config()
        # 微信推送
        self.enableWx = self.config.getboolean('messenger', 'enable')
        self.scKey = self.config.get('messenger', 'sckey')
        # 登录
        self.session = RucSession.Session( self.config.get('info','userAgent'),
                                self.config.get('info', 'stuid'),
                                self.config.get('info', 'pwd'),
                                self.config.get('info', 'name'), )

    def appointment(self):
        self.session.appointment(NAME = self.config.get('info','GuestName'),
                                 TEL = self.config.get('info','GuestTel'),
                                 IDCARD = self.config.get('info','GuestIdcard'),
                                 SEX = self.config.get('info','GuestSex'),
                                 TIME = self.config.get('info','GuestTime'))

    def EverydayAppoint(self):

        while True:
            time_now = time.strftime("%H%M", time.localtime())  # 刷新
            #print(time_now)
            year = time.strftime("%Y", time.localtime())
            day = time.strftime("%D", time.localtime()).split('/')
            time_str = year + '-' + day[0] + '-' + day[1]
            if time_now == "0001" or time_now == "1154" or time_now == "1155" :  # 设置要执行的时间
                text = self.session.appointment(NAME=self.config.get('info', 'GuestName'),
                                         TEL=self.config.get('info', 'GuestTel'),
                                         IDCARD=self.config.get('info', 'GuestIdcard'),
                                         SEX=self.config.get('info', 'GuestSex'),
                                         TIME=time_str)
                if self.enableWx:
                    send_wechat(
                        message='RUC每日自动化预约', desp= text, sckey=self.scKey)
                time.sleep(61)  # 停止执行61秒，防止反复运行程序。


if __name__ == "__main__":
    today = datetime.date.today()
    print(today)
    tomorrow = today + datetime.timedelta(days=1)
    print(tomorrow)
    TheDayAfterTomorrow = tomorrow + datetime.timedelta(days=1)
    print(TheDayAfterTomorrow)
    ruclogin = RUC().EverydayAppoint()
