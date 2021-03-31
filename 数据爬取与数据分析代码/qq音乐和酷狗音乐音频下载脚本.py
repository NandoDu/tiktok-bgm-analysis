import pyautogui
import time
import os
import pyperclip
import csv
import pandas as pd


def qqMusicSoundHound(path_list):
    lastText = ''
    text = ''
    pyperclip.copy('')
    for i in range(len(path_list)):
        lastText = text
        wavPath = 'S:\\抖音音频\\抖音原音频\\' + path_list[i]
        os.startfile(wavPath)
        time.sleep(1)
        Path = r'H:\Download\QQMusic\QQMusic.exe'
        os.startfile(Path)
        time.sleep(1)
        pyautogui.moveTo(1038, 190)
        time.sleep(1)
        pyautogui.click(clicks=1)
        time.sleep(10)
        pyautogui.moveTo(968, 456)
        time.sleep(1)
        pyautogui.click(clicks=1)
        text = pyperclip.paste()
        if lastText == text:
            print('未正确识别')
            with open("music.csv", 'a+', encoding='utf-8') as f:
                csv_write = csv.writer(f)
                csv_write.writerow([path_list[i], '0'])
        else:
            endIndex = int(str(text).find('，'))
            print(text[4:endIndex])
            pyautogui.moveTo(977, 610)
            time.sleep(1)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(1068, 645)
            time.sleep(1)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(878, 616)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(1156, 814)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(801, 808)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(1257, 285)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(904, 377)
            time.sleep(2)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(1257, 285)
            time.sleep(1)
            pyautogui.click(clicks=1)
            pyautogui.moveTo(792, 448)
            pyautogui.dragRel(210, 240, duration=1)
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            detail = pyperclip.paste()
            print(detail)
            with open("music.csv", 'a+', encoding='utf-8') as f:
                csv_write = csv.writer(f)
                csv_write.writerow([path_list[i], detail])
            pyperclip.copy(text)
        time.sleep(1)


def kugouMusicSoundHound(path_list):
    lastText = ''
    text = ''
    pyperclip.copy('')
    for i in range(len(path_list)):
        lastText = text
        wavPath = 'S:\\抖音音频\\抖音原音频\\' + path_list[i]
        os.startfile(wavPath)
        time.sleep(1)
        Path = r'H:\Download\KGMusic\KuGou.exe'
        os.startfile(Path)
        time.sleep(1)
        pyautogui.moveTo(1068, 680)
        pyautogui.click()
        time.sleep(15)
        pyautogui.moveTo(1235, 333)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(582, 443)
        pyautogui.rightClick()
        pyautogui.moveTo(666, 625)
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(809, 444)
        pyautogui.dragRel(300, 0, duration=0.5)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        detail = pyperclip.paste()
        print(detail)


def KuGouDownload():
    Path = r'H:\Download\KGMusic\KuGou.exe'
    os.startfile(Path)
    dataFrame = pd.read_csv('data3.csv')
    bgmFrame = dataFrame.drop_duplicates('bgm', keep='first')
    for i in range(683, len(bgmFrame)):
        if type(bgmFrame.iloc[i]['bgm']) == str:
            bgmName = bgmFrame.iloc[i]['bgm']
            index = bgmName.find('-')
            searchName = bgmName[0:index]
            time.sleep(2)
            pyautogui.moveTo(795, 153)
            pyautogui.click(clicks=2)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            pyautogui.hotkey('backspace')
            time.sleep(1)
            pyperclip.copy(searchName)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.hotkey('enter')
            time.sleep(3)
            pyautogui.moveTo(511, 444)
            pyautogui.click(clicks=2)
            time.sleep(1)
            pyautogui.rightClick()
            pyautogui.moveTo(561, 553)
            pyautogui.click()
            time.sleep(2)
            pyautogui.moveTo(888, 559)
            pyautogui.click()
            pyautogui.moveTo(957, 583)
            pyautogui.click()
            pyautogui.moveTo(957, 624)
            pyautogui.click()
            time.sleep(2)

def QQMusicDownload():
    Path = r'H:\Download\QQMusic\QQMusic.exe'
    os.startfile(Path)
    dataFrame = pd.read_csv(r'H:\NJU Documents\抖音数据分析ppt\数据分析\完整新数据.csv')
    cnt = 570
    for i in range(cnt, len(dataFrame)):
        bgm = dataFrame.iloc[i]['bgm']
        if len(bgm) > 0:
            searchName = bgm
            pyautogui.moveTo(883, 250)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            pyautogui.hotkey('backspace')
            time.sleep(1)
            pyperclip.copy(searchName)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.hotkey('enter')
            time.sleep(3)
            print('已下载第' + str(i + 1) + '首歌')

def mousePosition():
    while True:
        current_X, current_y = pyautogui.position()
        print('(' + str(current_X) + ',' + ' ' + str(current_y) + ')')


# KuGouDownload()
# mousePosition()
QQMusicDownload()
