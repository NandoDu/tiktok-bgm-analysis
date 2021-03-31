from appium import webdriver
from time import sleep
import csv
import codecs
import datetime as dt
import time as localTime
import pandas as pd


class Action:
    # 存储数据的列表
    infoList = []

    # 初始化函数
    def __init__(self):
        # 初始化设置
        print('初始化连接配置')
        # self.desired_caps = {
        #     "platformName": "Android",
        #     "deviceName": "127.0.0.1:62001",
        #     "appPackage": "com.kugou.shiqutouch",
        #     "appActivity": "com.kugou.shiqutouch.activity.StartupActivity",
        #     "noReset": True,
        #     "unicodeKeyboard": True,
        #     "resetKeyboard": True,
        # }
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "127.0.0.1:62001"
        }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'
        # 新建一个Session
        # self.driver = webdriver.Remote(self.server, self.desired_caps)
        self.driver = webdriver.Remote(self.server, self.desired_caps)

    def recognise(self):
        dataFrame = pd.read_csv(r'H:\NJU Documents\抖音数据分析ppt\数据分析\新数据.csv')
        dataFrame['bgm'] = ''
        cnt = 0
        sleep(5)
        self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ImageView[1]').click()
        sleep(1)
        self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.TextView[1]').click()
        while True:
            url = dataFrame.iloc[cnt]['video_url']
            print('正在识别第' + str(cnt + 1) + '首歌曲')
            print(url)
            sleep(1)
            self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.EditText').send_keys(url)
            sleep(1)
            self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.Button').click()
            sleep(8)
            try:
                song = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[2]').text
                dataFrame.loc[cnt, 'bgm'] = song
                print(song)
            except:
                print('歌曲未识别')
                pass
            sleep(1)
            self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView').click()
            sleep(1)
            try:
                self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.ImageView').click()
            except:
                pass
            cnt = cnt + 1

    def miniRecognise(self):
        global cnt
        global index
        dataFrame = pd.read_csv(r'H:\NJU Documents\抖音数据分析ppt\数据分析\新数据(bgm).csv')
        for i in range(index, len(dataFrame)):
            cnt = i
            url = dataFrame.iloc[i]['video_url']
            print('正在识别第' + str(i + 1) + '首歌曲')
            print(url)
            self.driver.set_clipboard_text(url)
            sleep(5)
            try:
                bgm = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView[2]').text
                dataFrame.loc[i, 'bgm'] = bgm
                print(bgm)
            except:
                print('未识别到歌曲')
            dataFrame.to_csv(r'H:\NJU Documents\抖音数据分析ppt\数据分析\新数据(bgm).csv')
            self.driver.tap([(520, 360), (536, 373)], 500)

    def main(self):
        # self.recognise()
        self.miniRecognise()


if __name__ == '__main__':
    index = 1569
    cnt = index
    while True:
        action = Action()
        action.main()
