from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import pyperclip


def searchSongInfo(driver, song):
    infoList = []
    try:
        driver.find_element_by_class_name('search_input__input').send_keys(song)
        driver.find_element_by_class_name('sprite').click()
        sleep(2)
        driver.find_element_by_xpath('//*[@id="song_box"]/div[2]/ul[2]/li[1]/div/div[2]/span[1]/a/span').click()
        sleep(2)
        infoList.append(driver.find_element_by_class_name('js_lan').text)
        infoList.append(driver.find_element_by_class_name('js_genre').text)
        infoList.append(driver.find_element_by_class_name('js_public_time').text)
        driver.find_element_by_id('copy_link').click()
        lyrics = pyperclip.paste()
        f = open('H:\\NJU Documents\\tiktok\\音乐数据库歌词\\' + song + '.txt', mode='w', encoding='utf-8')
        f.write(lyrics)
        f.close()
        driver.find_element_by_class_name('search_input__input').clear()
    except NoSuchElementException as e:
        driver.find_element_by_class_name('search_input__input').clear()
        pass
    except ElementNotVisibleException:
        driver.find_element_by_class_name('search_input__input').clear()
        pass
    print(infoList)
    return infoList


bgmFrame = pd.read_csv(r'H:\NJU Documents\tiktok\数据分析\音乐数据库待完善数据.csv')
songList = []
cnt = 0
for i in range(cnt, len(bgmFrame)):
    song = bgmFrame.iloc[i]['bgm']
    song = song.replace('/','').replace('?','').replace('(','').replace(')','').replace('*','')
    songList.append(song)
driver = webdriver.Chrome(r'L:\Chrome6103163100x86\GoogleChrome_61.0.3163.100_x86\ChromePortable\App\Google Chrome\chromedriver.exe')
driver.maximize_window()
driver.get("https://y.qq.com/")
sleep(10)
driver.find_element_by_class_name('popup__icon_close').click()
for song in songList:
    infoList = searchSongInfo(driver, song)
    if len(infoList) == 3:
        language = infoList[0]
        genre = infoList[1]
        public_time = infoList[2]
        index1 = language.find('：')
        index2 = genre.find('：')
        index3 = public_time.find('：')
        language = language[index1 + 1:].replace(' ', '')
        genre = genre[index2 + 1:].replace(' ', '')
        public_time = public_time[index3 + 1:].replace(' ', '')
        bgmFrame.loc[cnt, 'language'] = language
        bgmFrame.loc[cnt, 'genre'] = genre
        bgmFrame.loc[cnt, 'public_time'] = public_time
    cnt = cnt + 1
    print('完成' + str(cnt) + '首歌曲的搜索')
    bgmFrame.to_csv(r'H:\NJU Documents\tiktok\数据分析\音乐数据库待完善数据.csv')
