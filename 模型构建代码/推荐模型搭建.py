# -*- coding:utf-8 -*-
import csv
import os
import csv
import json
import math
import time
import string
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter
import numpy as np
import re
from matplotlib.font_manager import FontProperties
import json
from pyecharts import Pie
allobject=[]
#对四个维度的打分
def salesjudge(sales):
    salesgroup=[1,10,1000,5000,10000,20000,50000,100000,1000000,10000000]
    judge=41
    for i in range(len(salesgroup)-1,0,-1):
        if sales<=salesgroup[i]:
            judge-=1
    return judge
def likesjudge(sales):
    likesgroup = [1, 10, 100, 500, 1000, 5000, 10000, 100000, 1000000, 10000000]
    judg=11
    for i in range(len(likesgroup)-1,0,-1):
        if sales<=likesgroup[i]:
            judg-=1
    return judg
def commentsjudge(sales):
    commentsgroup = [1, 10, 100, 200, 500, 1000, 3000, 5000, 10000, 100000]
    jud=11
    for i in range(len(commentsgroup)-1,0,-1):
        if sales<=commentsgroup[i]:
            jud-=1
    return jud
def forwardsjudge(sales):
    forwardsgroup=[1,10,100,200,500,1000,3000,5000,10000,100000]
    ju=11
    for i in range(len(forwardsgroup)-1,0,-1):
        if sales<=forwardsgroup[i]:
            ju-=1
    return ju
#对打分求均值排名的六个函数
def languageclassify(list):
    music=0
    english=0
    janp=0
    korea=0
    chinese=0
    others=0
    for i in list:
        if i[10]=='纯音乐':
            music+=i[4]
        elif i[10]=='英语':
            english+=i[4]
        elif i[10]=='国语':
            chinese+=i[4]
        elif i[10]=='日语':
            janp+=i[4]
        elif i[10]=='韩语':
            korea+=i[4]
        else:
            others+=i[4]
    types=['music','english','chinese','japanese','korean','others']
    score=[music/len(list),english/len(list),chinese/len(list),janp/len(list),korea/len(list),others/len(list)]
    dic=dict(zip(types,score))
    dic=sorted(dic.items(), key=lambda item:item[1],reverse=True)
    return dic
def feelingsclassify(list):
    happy=0
    peaceful=0
    sad=0
    mad=0
    for i in list:
        if i[13]=='peaceful':
            peaceful+=i[4]
        elif i[13]=='happy':
            happy+=i[4]
        elif i[13]=='sad':
            sad+=i[4]
        elif i[13]=='mad':
            mad+=i[4]
    types=['happy', 'peaceful', 'sad', 'mad']
    score=[happy/len(list),peaceful/len(list),sad/len(list),mad/len(list)]
    dic=dict(zip(types,score))
    dic=sorted(dic.items(), key=lambda item:item[1],reverse=True)
    return dic
def timeclassify(list):
    c1900=0
    c2000=0
    c2010=0
    error=0
    for i in list:
        try:
            year=eval(i[11][0:4])
            if year<2000:
                c1900+=i[4]
            elif year<=2010:
                c2000+=i[4]
            else:
                c2010+=i[4]
        except:
            error+=1
    types=['20c', '21c00s', '21c10s']
    score=[c1900/(len(list)-error),c2000/(len(list)-error),c2010/(len(list)-error)]
    dic=dict(zip(types,score))
    dic=sorted(dic.items(), key=lambda item:item[1],reverse=True)
    return dic
def bpmclassify(list):
    slow=0
    medium=0
    quick=0
    error=0
    for i in list:
        bpm=int(i[8])
        if bpm<110:
            slow+=i[4]
        elif bpm<=130:
            medium+=i[4]
        else:
            quick+=i[4]
    types=['slow', 'medium', 'quick']
    score=[slow/(len(list)-error),medium/(len(list)-error),quick/(len(list)-error)]
    dic=dict(zip(types,score))
    dic=sorted(dic.items(), key=lambda item:item[1],reverse=True)
    return dic
def gereclassify(list):
    Pop=0
    Soundtrack=0
    hiphop=0
    rock=0
    blues=0
    country=0
    others=0
    for i in list:
        ge=i[9]
        if i[9] == 'Pop':
            Pop += i[4]
        elif i[9] == 'Soundtrack':
            Soundtrack += i[4]
        elif i[9] == 'hiphop':
            hiphop += i[4]
        elif i[9] == 'rock':
            rock += i[4]
        elif i[9] == 'blues':
            blues += i[4]
        elif i[9] == 'country':
            country += i[4]
        else:
            others += i[4]
    types = ['Pop', 'Soundtrack', 'hiphop', 'rock','blues', 'country','others']
    score = [Pop / len(list), Soundtrack / len(list), hiphop / len(list), rock / len(list), blues / len(list),country/ len(list),
                 others / len(list)]
    dic = dict(zip(types, score))
    dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    return dic
def attitudeclassify(list):
    positive=0
    negative=0
    for i in list:
        ge=i[12]
        if i[12] == 'negative':
            negative += i[4]
        else:
            positive += i[4]
    types = ['positive', 'negative']
    score = [positive / len(list), negative/ len(list)]
    dic = dict(zip(types, score))
    dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    return dic
#打开文件 数据清洗
def openfile():
    error=0
    with open('完整的有效建模表.csv', 'r', encoding='utf-8')as f:
        f_csv = csv.reader(f)
        for k in f_csv:
            if (k[7] != '' and (str(k[7])[-1] == '万' or str(k[7])[-1] == 'w')):
                k[7] = eval(k[7][0:-1]) * 10000
            if (k[7] != '' and str(k[7])[0] == '\''):
                k[7] = eval(k[7][1:])
            if (k[8] != '' and (str(k[8])[-1] == '万' or str(k[8])[-1] == 'w')):
                k[8] = eval(k[8][0:-1]) * 10000
            if (k[8] != '' and str(k[8])[0] == '\''):
                k[8] = eval(k[8][1:])
            if (str(k[7]).count(',') != 0):
                k[7] = restoreNumber(k[7])
            if (str(k[8]).count(',') != 0):
                k[8] = restoreNumber(k[8])
            try:
                k[7] = eval(k[7])
                k[8]=eval(k[8])
            except:
                error += 1
            allobject.append(k)
            if types.count(k[1])==0:
                types.append(k[1])
def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf
#几个维度数据的映射函数
def function(list):
    saleslist=[]
    likeslist=[]
    commentslist=[]
    forwardslist=[]
    error=0
    for i in list:
        sales=i[2]
        likes=i[3]
        comments=i[4]
        forwards=i[5]
        if i[2]=='':
            i[2]=0
            sales=0
        if i[3]=='':
            i[3]=0
            likes=0
        if i[4]=='':
            i[4]=0
            comments=0
        if i[5]=='':
            i[5]=0
            forwards=0
        if(i[4]!=0):
            comments=eval(i[4])
        if(i[5]!=0):
            forwards=eval(i[5])
        try:
            sales=eval(i[2])
            likes=eval(i[3])
        except:
            error+=1
        saleslist.append(sales)
        likeslist.append(likes)
        commentslist.append(comments)
        forwardslist.append(forwards)
    newlike=[]
    newsale=[]
    newcom=[]
    newfor=[]
    for k in likeslist:
        newlike.append(int(k))
    for k in saleslist:
        newsale.append(int(k))
    for k in commentslist:
        newcom.append(int(k))
    for k in forwardslist:
        newfor.append(int(k))
    likeslist=newlike
    saleslist=newsale
    commentslist=newcom
    forwardslist=newfor
    salesdid=max(saleslist)-min(saleslist)
    likesdid=max(likeslist)-min(likeslist)
    commentsdid=max(commentslist)-min(commentslist)
    forwardsdid=max(forwardslist)-min(forwardslist)


    for i in list:
        sales=i[2]
        likes=i[3]
        comments=i[4]
        forwards=i[5]
        if i[2]=='':
            i[2]=0
            sales=0
        if i[3]=='':
            i[3]=0
            likes=0
        if i[4]=='':
            i[4]=0
            comments=0
        if i[5]=='':
            i[5]=0
            forwards=0
        if(i[4]!=0):
            comments=eval(i[4])
        if(i[5]!=0):
            forwards=eval(i[5])
        sales=i[2]
        likes=i[3]
        try:
            sales=eval(i[2])
            likes=eval(i[3])
        except:
            error+=1
        s=0
        sales=int(sales)
        likes=int(likes)
        comments=int(comments)
        forwards=int(forwards)
        a=salesjudge(sales)
        b=likesjudge(likes)
        c=commentsjudge(comments)
        d=forwardsjudge(forwards)
        final=[a,b,c,d]
        score=sum(final)
        i.insert(4,score)
#对类别的分类函数
def classify(list):
    makeups = []
    clothes = []
    toys = []
    digits = []
    foods = []
    boots = []
    others = []
    daily = []
    medecines = []
    allkinds = [makeups, clothes, digits, toys, foods, boots, others, medecines, daily]
    for i in allobject:
        if (i[1] == '美妆类'):
            allkinds[0].append(i)
        elif (i[1] == '服装类'):
            allkinds[1].append(i)
        elif (i[1] == '电器数码类'):
            allkinds[2].append(i)
        elif (i[1] == '文具玩具图书类'):
            allkinds[3].append(i)
        elif (i[1] == '食品类'):
            allkinds[4].append(i)
        elif (i[1] == '鞋靴箱包饰品类'):
            allkinds[5].append(i)
        elif (i[1] == '其他'):
            allkinds[6].append(i)
        elif (i[1] == '医药保健类'):
            allkinds[7].append(i)
        elif (i[1] == '家装日用类'):
            allkinds[8].append(i)
    print(allkinds)
    return allkinds
def restoreNumber(numStr):
    pattern=re.compile('\D')
    numList=pattern.split(numStr)
    numStr=''.join(numList)
    return int(numStr)
def draw_pic():
    data=[]
    for i in after_classify:
        data.append(len(i))
    print(data)
    from pyecharts import Bar
    columns = ['美妆类', '服装类', '电器数码类', '文具玩具图书类', '食品类', '鞋靴箱包饰品类', '其他', '医药保健类', '家装日用类']
    pie = Pie("饼状图", "带货商品种类", title_pos='center', width=900)
    pie.add("商品种类", columns, data, center=[50, 50],is_label_show=True,is_legend_show=False)
    pie.render()

def ui():
    print('********音乐推荐系统********')
    time.sleep(2)
    print('请选择商品类目：')
    print('1. 家装日用类')
    print('2. 美妆类')
    print('3. 文具玩具图书类')
    print('4. 食品类')
    print('5. 医药保健类')
    print('6. 鞋靴箱包饰品类')
    print('7. 服装类')
    print('8. 电器数码类')
    print('9. 其他')

    goods = int(input())
    time.sleep(1)
    print('****正在努力为您匹配合适的BGM****')
    time.sleep(3)
    print('**以下是系统推荐的BGM：**')
    print('   音乐    ---    推荐指数')
    print('')
    print('1. 音乐1   ---      9.0')
    print('2. 音乐2   ---      8.8')
    print('3. 音乐3   ---      8.7')
    print('4. 音乐4   ---      8.5')
    print('5. 音乐5   ---      8.4')
    print('')
    time.sleep(2)
    while True:
        print('请选择您要进行的操作：')
        print('1. 显示更多')
        print('2. 选择音乐')
        judge = int(input())
        if judge == 1:
            print('   音乐    ---    推荐指数')
            print('')
            print('6. 音乐6   ---      8.2')
            print('7. 音乐7   ---      7.8')
            print('8. 音乐8   ---      7.7')
            print('9. 音乐9   ---      7.5')
            print('10.音乐10  ---      7.4')
        else:
            print('您要选择的音乐序号是：')
            order = int(input())
            time.sleep(2)
            while True:
                print('您可以进行如下操作：')
                print('1. 试听音乐')
                print('2. 采纳音乐')
                print('3. 点赞')
                print('4. 点踩')
                choose = int(input())
                if choose == 1:
                    time.sleep(2)
                    print('*音乐播放中*')
                    time.sleep(5)
                    print('*试听结束*')
                    time.sleep(2)
                    print('')
                elif choose == 2:
                    time.sleep(2)
                    print('*小提示*该音乐配合xx类带货视频往往能起到xx效果，但我们更推荐你选用快节奏的音乐')
                    exit(1)
                elif choose == 3:
                    time.sleep(2)
                    print('*您的反馈已收到，在今后相关类目的推荐中，我们将考虑优先推荐该背景音乐*')
                    time.sleep(2)
                    print('')
                else:
                    time.sleep(2)
                    print('*您的反馈已收到，在今后相关类目的推荐中，我们将尽量少推荐该背景音乐*')
                    time.sleep(2)
                    print('')
#对每首歌的rank打分
def judgeall(inlist):
    error=0
    makeups=[[('english', 11.751351351351351), ('others', 11.248648648648649), ('chinese', 10.935135135135136), ('music', 9.491891891891893), ('korean', 3.1243243243243244), ('japanese', 1.772972972972973)],[('happy', 23.21081081081081), ('mad', 9.21081081081081), ('peaceful', 8.81081081081081), ('sad', 7.091891891891892)],[('21c10s', 36.57615894039735), ('21c00s', 9.821192052980132), ('20c', 2.1059602649006623)],[('medium', 18.156756756756756), ('slow', 17.83783783783784), ('quick', 12.32972972972973)]]
    clothes = [[('chinese', 21.412228796844182), ('others', 10.684418145956608), ('music', 3.5226824457593686), ('english', 3.2958579881656807), ('korean', 0.8816568047337278), ('japanese', 0.15384615384615385)],[('happy', 22.16568047337278), ('sad', 8.22879684418146), ('peaceful', 4.867850098619329), ('mad', 4.68836291913215)],[('21c10s', 32.4317617866005), ('21c00s', 6.002481389578164), ('20c', 1.4764267990074442)],[('medium', 17.992110453648916), ('slow', 13.936883629191321), ('quick', 8.021696252465484)]]
    digits = [[('others', 14.908256880733944), ('chinese', 13.18348623853211), ('music', 7.5504587155963305), ('english', 5.862385321100917), ('japanese', 1.2935779816513762), ('korean', 0.45871559633027525)],[('happy', 19.63302752293578), ('sad', 10.715596330275229), ('mad', 8.0), ('peaceful', 4.908256880733945)],[('21c10s', 38.77333333333333), ('21c00s', 3.973333333333333), ('20c', 0.0)],[('medium', 22.422018348623855), ('slow', 11.20183486238532), ('quick', 9.63302752293578)]]
    toys = [[('chinese', 17.75796178343949), ('others', 10.528662420382165), ('music', 9.420382165605096), ('english', 3.694267515923567), ('korean', 1.21656050955414), ('japanese', 0.5859872611464968)],[('happy', 23.630573248407643), ('sad', 8.694267515923567), ('mad', 7.0), ('peaceful', 3.878980891719745)],[('21c10s', 35.968992248062015), ('21c00s', 5.728682170542636), ('20c', 1.4651162790697674)],[('slow', 18.598726114649683), ('medium', 16.515923566878982), ('quick', 8.089171974522293)]]
    foods = [[('chinese', 18.43452380952381), ('others', 15.81547619047619), ('music', 6.244047619047619), ('english', 2.8035714285714284), ('korean', 2.0654761904761907), ('japanese', 0.0)]
,[('happy', 21.785714285714285), ('mad', 11.31547619047619), ('sad', 8.19047619047619), ('peaceful', 4.071428571428571)]
,[('21c10s', 34.596774193548384), ('21c00s', 7.82258064516129), ('20c', 2.8306451612903225)]
,[('medium', 20.36904761904762), ('slow', 13.035714285714286), ('quick', 11.958333333333334)]]
    boots = [[('chinese', 22.859375), ('others', 7.6484375), ('music', 5.1640625), ('english', 3.8671875), ('japanese', 1.28125), ('korean', 0.0)]
,[('happy', 21.5546875), ('sad', 8.421875), ('mad', 7.65625), ('peaceful', 3.1875)]
,[('21c10s', 32.625), ('21c00s', 6.5576923076923075), ('20c', 2.019230769230769)]
,[('medium', 19.8203125), ('slow', 13.9296875), ('quick', 7.0703125)]]
    others = [[('chinese', 18.071428571428573), ('others', 10.964285714285714), ('music', 7.0), ('english', 2.7857142857142856), ('japanese', 0.0), ('korean', 0.0)]
,[('happy', 13.964285714285714), ('sad', 10.964285714285714), ('peaceful', 9.714285714285714), ('mad', 4.178571428571429)]
,[('21c10s', 32.17391304347826), ('21c00s', 5.043478260869565), ('20c', 1.7391304347826086)]
,[('medium', 20.821428571428573), ('quick', 11.071428571428571), ('slow', 6.928571428571429)]]
    medecines = [[('others', 17.25), ('music', 10.75), ('chinese', 5.0), ('english', 4.875), ('korean', 4.75), ('japanese', 0.0)]
,[('happy', 26.5), ('sad', 10.875), ('peaceful', 5.25), ('mad', 0.0)]
,[('21c10s', 40.6), ('20c', 0.0), ('21c00s', 0.0)]
,[('quick', 16.75), ('medium', 15.625), ('slow', 10.25)]]
    daily= [[('chinese', 20.691666666666666), ('others', 12.425), ('english', 5.133333333333334), ('music', 3.441666666666667), ('japanese', 1.35), ('korean', 0.95)]
,[('happy', 25.333333333333332), ('sad', 8.241666666666667), ('mad', 7.208333333333333), ('peaceful', 3.2083333333333335)]
,[('21c10s', 35.65217391304348), ('21c00s', 7.956521739130435), ('20c', 0.6739130434782609)]
,[('slow', 18.483333333333334), ('medium', 17.933333333333334), ('quick', 7.575)]]

    all = [makeups, clothes, digits, toys, foods, boots, others, medecines, daily]

    for i in inlist:
        rank=0

        lantype=i[13]
        feel=i[16]
        bpm = int(eval(i[18]))
        bpmtag=''
        yeartag=''
        lantag=''
        if bpm<110:
            bpmtag='slow'
        elif bpm<=130:
            bpmtag='medium'
        else:
            bpmtag='quick'

        try:
            year=eval(i[15][0:4])
            if year<2000:
                yeartag='20c'
            elif year<=2010:
                yeartag='21c00s'
            else:
                yeartag='21c10s'
        except:
            error+=1
        music = 0
        english = 0
        janp = 0
        korea = 0
        chinese = 0
        others = 0
        if i[13] == '纯音乐':
            lantag='music'
        elif i[13] == '英语':
            lantag='english'
        elif i[13] == '国语':
            lantag='chinese'
        elif i[13] == '日语':
            lantag= 'japanese'
        elif i[13] == '韩语':
            lantag='korean'
        else:
            lantag='others'
        this=[lantag,feel,yeartag,bpmtag]
        allrank=[]
        for j in all:
            rank=0
            for l in range(len(j)):
                new=dict(j[l])
                try:
                    rank+=list(new.keys()).index(this[l])
                except:
                    rank+=5
            allrank.append(rank)
        i.append(allrank)
    print(i)
    print("--------------------")
types=[]
musictype=[]
lantype=[]
feeltype=[]
allge=[]
#匹配拼接
openfile()
allobject.remove(allobject[0])
print(allobject)
after_classify=classify(allobject)
for k in after_classify:
    function(k)
    k.sort(reverse=True)
    print(k[0][1])
    print(languageclassify(k))
    print(feelingsclassify(k))
    print(bpmclassify(k))
    print(timeclassify(k))
    print(gereclassify(k))
    print(attitudeclassify(k))

    print("-----------------------------")
print(types)
print(after_classify)
draw_pic()