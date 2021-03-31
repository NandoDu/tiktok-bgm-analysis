import csv
import os
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
all=[]
rootdir = 'BGM1'
list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
print(list)
with open('3.csv', 'a') as csvfile:
    header=['No', 'title', 'tempo']
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    csvfile.close()

errors=0
for i in range(0, len(list)):
    path = os.path.join(rootdir, list[i])
    print(path)
    try:
        yy, sr = librosa.load(path)
        onset_env = librosa.onset.onset_strength(yy, sr=sr, hop_length=512, aggregate=np.median)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        want=[i+1,list[i],tempo]
        all.append(want)
        print(want)
    except:
        errors+=1
print(all)
with open('3.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    for i in all:
        try:
            writer.writerow(i)
        except:
            errors+=1


print(errors)