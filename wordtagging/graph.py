import csv
import os
import datetime
from collections import Counter

import matplotlib
import pandas as pd
import rhinoMorph
from matplotlib import font_manager

font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'

font_name = font_manager.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_name)

os.chdir("/Users/parkn/Desktop/삼성전자2/")
rn = rhinoMorph.startRhino()
csv_count = 1
count = 1

stop_words_list = []
positive_words_list=[]
negative_words_list=[]
s_file_name = open('중립_감성사전.txt', 'r', encoding='utf-8')
positive_file = open('긍정_전체형태소_감성사전.txt', 'r', encoding='utf=8')
negative_file = open('부정_전체형태소_감성사전.txt', 'r', encoding='utf=8')
for line in s_file_name.readlines():
    stop_words_list.append(line.rstrip())

for line in positive_file.readlines():
    positive_words_list.append(line.rstrip())

for line in negative_file.readlines():
    negative_words_list.append(line.rstrip())

s_file_name.close()
positive_file.close()
negative_file.close()
print(stop_words_list)

positive_cnt = 0
negative_cnt = 0
cnt_result = []
title_result = []
date_result = []

with open('삼성전자.csv','r',encoding='UTF8') as f:
    reader = csv.reader(f)

    for a in reader:
        text_analyzed = rhinoMorph.onlyMorph_list(rn, a[1], pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR','MM','NV','NF'], eomi=True)
        #print("\n", count, ". 형태소 분석 결과:", text_analyzed)
        #joined_data_each = ' '.join(text_analyzed)  # 문자열을 하나로 연결

        for w in text_analyzed:
            if w not in stop_words_list:  # 내용이 있는 경우만 저장
                if w in positive_words_list:
                    positive_cnt += 1
                elif w in negative_words_list:
                    negative_cnt -= 1
        cnt_result.append(positive_cnt + negative_cnt)
        date_result.append(a[2])
        title_result.append(a[1])
        positive_cnt = 0
        negative_cnt = 0
        count += 1

concat_data={'date':date_result,
             'title':title_result,
             'pos/neg':cnt_result}
analyzed_df=pd.DataFrame(concat_data)
analyzed_df.to_csv('./sk하이닉스 긍부정추가된 데이터 셋.csv', mode='w',encoding='utf-8-sig',header=True,index=True)