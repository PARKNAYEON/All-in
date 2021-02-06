import csv
import os
import datetime
from collections import Counter

import matplotlib
import pandas as pd
import rhinoMorph
from matplotlib import font_manager

#긍정, 부정, 중립 사전 분류
font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'

font_name = font_manager.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_name)

os.chdir("/Users/parkn/Desktop/삼성전자2/")
rn = rhinoMorph.startRhino()

positive_data=''
negative_data=''
neu_data=''
count = 1

def write_data(data, filename, encoding='UTF8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)

with open('전체형태소_삼성전자.csv','r',encoding='UTF8') as f:
    reader = csv.reader(f)

    for a in reader:
        if a[2] == '-1':
            negative_data += a[0] + "\n"
        elif a[2] == '1':
            positive_data += a[0] + "\n"
        else:
            neu_data += a[0] + "\n"

        count += 1

write_data(positive_data,'긍정_전체형태소_감성사전.txt', encoding='UTF8')
write_data(negative_data, '부정_전체형태소_감성사전.txt', encoding='UTF8')
write_data(neu_data,'중립_감성사전.txt', encoding='UTF8')