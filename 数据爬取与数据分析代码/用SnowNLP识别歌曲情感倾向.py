from snownlp import SnowNLP
import paddlehub as hub
import os
import csv

rootdir = r'H:\NJU Documents\tiktok\音乐数据库歌词'
list = os.listdir(rootdir)
all=[]
senta = hub.Module(name="senta_lstm")

for i in range(0, len(list)):
    path = os.path.join(rootdir, list[i])
    sent=""
    posi=0
    nega=0
    with open(path, encoding='utf-8') as f:
        print(path)
        test = f.readline().replace(' ', '')
        try:
            if(len(test)>20 and '\u4e00' <= test[0] <= '\u9fff'):
                test_text = [test]
                # 情感分类
                results = senta.sentiment_classify(data={"text": test_text})
                # 得到结果
                for result in results:
                    # 整体情感偏向
                    print("该歌词的情感倾向为" + result['sentiment_key'])
                    # 积极比
                    print("该歌词的积极情感倾向为")
                    print(result['positive_probs'])
                    # 消极比
                    print("该歌词的消极情感倾向为")
                    print(result['negative_probs'])
                sent=result['sentiment_key']
                posi=result['positive_probs']
                nega=result['negative_probs']
                # 词性分类并统计
                s = SnowNLP(test)
                tags = [x for x in s.tags]
                vcount = 0
                ncount = 0
                acount = 0
                for tag in tags:
                    if tag[1] == 'v':
                        vcount += 1
                    elif tag[1] == 'n':
                        ncount += 1
                    elif tag[1] == 'a':
                        acount += 1
                words = {'动词': vcount, '名词': ncount, '形容词': acount}
                max = 0
                maxword = ""
                for x in s.keywords(limit=10):
                    if s.words.count(x) > max:
                        max = s.words.count(x)
                        maxword = x
            else:
                s = SnowNLP(test)

                if s.sentiments>0.5:
                    sent="positive"

                else:
                    sent="negative"
                posi=s.sentiments
                nega=1-posi
                tags = [x for x in s.tags]
                vcount = 0
                ncount = 0
                acount = 0
                for tag in tags:
                    if tag[1] == 'v':
                        vcount += 1
                    elif tag[1] == 'n':
                        ncount += 1
                    elif tag[1] == 'a':
                        acount += 1
                words = {'动词': vcount, '名词': ncount, '形容词': acount}
                max = 0
                maxword = ""
                for x in s.keywords(limit=10):
                    if s.words.count(x) > max:
                        max = s.words.count(x)
                        maxword = x
            #want 每首歌词分析结果
            want=[path[3:],sent,str(posi)[0:6],str(nega)[0:6],words,s.keywords(limit=10)]
            #all 全部分析结果
            all.append(want)
        except:
            pass
