from appium import webdriver
from time import sleep
from seleniumCrawler.common.exceptions import NoSuchElementException, InvalidSessionIdException, WebDriverException
import csv
import codecs
import sounddevice as sd
from scipy.io import wavfile
import datetime as dt
import time as localTime


class Action:
    # 存储数据的列表
    infoList = []

    # 初始化函数
    def __init__(self):
        # 初始化设置
        print('初始化连接配置')
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "127.0.0.1:62001",
            "appPackage": "com.ss.android.ugc.aweme",
            "appActivity": ".main.MainActivity",
            "noReset": True,
            "unicodeKeyboard": True,
            "resetKeyboard": True,
        }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'
        # 新建一个Session
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        # 获取模拟器屏幕的尺寸
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        # 设置滑动初始坐标和滑动距离
        self.start_x = width * 0.5
        self.start_y = height * 0.75
        self.end_x = self.start_x
        self.end_y = height * 0.25
        self.waveIndex = 1
        self.judge = 0

    def comments(self):
        print('首页广告等待')
        sleep(15)
        self.driver.tap([(520, 360), (536, 373)], 500)
        sleep(5)

    def recordBGM(self, time):
        unit = time.split(':')
        time_record = int(unit[0]) * 60 + int(unit[1])
        if time_record >= 55:
            time_record = 55
        print('开始录制')
        fs = 44100  # Hz
        length = time_record  # s
        recording = sd.rec(frames=fs * length, samplerate=fs, blocking=True, channels=1)
        filename = dt.datetime.now().strftime('%F-%T')
        filename = filename.replace(':', '')
        wavfile.write('S:\\抖音音频\\抖音原音频\\%s.wav' % filename, fs, recording)
        print('成功保存')
    # 用浮浮雷达识别BGM
    def fufuSoundHound(self):
        sleep(2)
        music = ''
        self.driver.tap([(661, 976), (681, 989)], 500)
        sleep(2)
        try:
            self.driver.find_element_by_android_uiautomator("text(\"复制链接\")").click()
        except NoSuchElementException as e:
            return music
        try:
            sleep(15)
            music = self.driver.find_element_by_id('com.kugou.shiqutouch:id/url_extract_songDesc').text
        except NoSuchElementException as e:
            try:
                self.driver.find_element_by_id('com.kugou.shiqutouch:id/url_extract_close').click()
                return music
            except NoSuchElementException as e1:
                return music
        sleep(1)
        self.driver.find_element_by_id('com.kugou.shiqutouch:id/url_extract_close').click()
        print(music)
        return music

    # 抖音结合浮浮雷达的爬虫
    def fufuGoods(self):
        print('跳转到搜索页面')
        self.driver.tap([(667, 58), (690, 81)], 500)
        print('加载等待')
        sleep(10)
        print('跳转到好物榜')
        self.driver.find_element_by_xpath(
            '//android.view.View[@content-desc="更多"]/android.widget.TextView').click()
        print('加载等待')
        sleep(4)
        self.driver.find_element_by_android_uiautomator("text(\"好物榜\")").click()
        sleep(8)
        print('跳转到浏览更多带货视频')
        try:
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View')
        except NoSuchElementException as e:
            print('Warning: noSuchElementException!')
            return
        self.driver.swipe(350, 1260, 350, 270, 500)
        while True:
            try:
                text1_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text1_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text1_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text2_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text2_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text2_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text3_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text3_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text3_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text4_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text4_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text4_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text5_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text5_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text5_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text6_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text6_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text6_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text7_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text7_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text7_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            try:
                text8_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text8_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                music = self.fufuSoundHound()
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text8_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), music]
                print(item)
                with open("data3.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
                self.judge = 0
            except NoSuchElementException as e:
                self.judge = self.judge + 1
                print('Warning: noSuchElementException!')
                if self.judge >= 8:
                    break
                pass
            for i in range(5):
                self.driver.swipe(350, 1260, 350, 270, 500)
                sleep(3)
            try:
                self.driver.find_element_by_android_uiautomator("text(\"好物榜\")")
                break
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                print(self.judge)
                pass
            if self.judge >= 8:
                break

    # 好物榜视频浏览函数
    def goods(self):
        print('跳转到搜索页面')
        self.driver.tap([(667, 58), (690, 81)], 500)
        print('加载等待')
        sleep(10)
        print('跳转到好物榜')
        self.driver.find_element_by_xpath(
            '//android.view.View[@content-desc="更多"]/android.widget.TextView').click()
        print('加载等待')
        sleep(4)
        self.driver.find_element_by_android_uiautomator("text(\"好物榜\")").click()
        sleep(8)
        print('跳转到浏览更多带货视频')
        try:
            self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View')
        except NoSuchElementException as e:
            print('Warning: noSuchElementException!')
            return
        self.driver.swipe(350, 1260, 350, 270, 500)
        while True:
            try:
                text1_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text1_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text1_title, time_record, num[3:num.find('件')], localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text2_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text2_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text2_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text3_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text3_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text3_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text4_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text4_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text4_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text5_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text5_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text5_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text6_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text6_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text6_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text7_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').text
                print(text7_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[1]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text7_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            try:
                text8_title = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[2]/android.widget.TextView[1]').text
                print(text8_title)
                duration = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.TextView').text
                print(duration)
                num = self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[2]/android.widget.TextView[4]').text
                print(num)
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View[1]/android.support.v4.view.ViewPager/android.view.View/android.widget.ScrollView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[2]').click()
                sleep(2)
                filename = dt.datetime.now().strftime('%F-%T')
                filename = filename.replace(':', '')
                self.recordBGM(duration)
                unit = duration.split(':')
                time_record = int(unit[0]) * 60 + int(unit[1])
                item = [text8_title, time_record, num[3:num.find('件')],
                        localTime.strftime("%Y-%m-%d %H:%M:%S", localTime.localtime()), filename + '.wav']
                print(item)
                with open("data.csv", 'a+', encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(item)
                self.driver.tap([(29, 68), (39, 68)])
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass
            self.driver.swipe(350, 1260, 350, 540, 500)
            try:
                self.driver.find_element_by_android_uiautomator("text(\"好物榜\")")
                break
            except NoSuchElementException as e:
                print('Warning: noSuchElementException!')
                pass

    def main(self):
        self.comments()
        self.fufuGoods()


if __name__ == '__main__':
    sd.default.device[0] = 18
    while True:
        action = Action()
        try:
            action.main()
        except InvalidSessionIdException as e:
            print('Warning: invalidSessionIdException!')
            continue
        except WebDriverException as e:
            print('Warning: webDriverException!')
            continue
