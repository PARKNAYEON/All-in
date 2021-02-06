# import csv
# import os
# import datetime
# from collections import Counter
#
# import matplotlib
# import pandas as pd
# import rhinoMorph
# from matplotlib import font_manager
#
# font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'
#
# font_name = font_manager.FontProperties(fname=font_path).get_name()
#
# matplotlib.rc('font', family=font_name)
#
# os.chdir("/Users/parkn/Desktop/삼성전자2/")
# rn = rhinoMorph.startRhino()
# csv_count = 1
# count = 1
# morphed_data = ''
# stop_words_list = []
# s_file_name = open('중립_감성사전.txt', 'r', encoding='utf-8')
# for line in s_file_name.readlines():
#     stop_words_list.append(line.rstrip())
#
# s_file_name.close()
# print(stop_words_list)
#
# def write_data(data, filename, encoding='UTF8'):
#     with open(filename, 'w', encoding=encoding) as f:
#         f.write(data)
#
# def read_data(filename, encoding='UTF8'):
#     with open(filename, 'r', encoding=encoding) as f:
#         data = [line.split('\t') for line in f.read().splitlines()]
#         data = data[1:]  # txt 파일의 헤더는 제외
#     return data
#
# def concating(startdate,enddate, key_result,value_result):
#     concat_data={'형태소': key_result,
#                  '빈도수': value_result}
#     tagging_df=pd.DataFrame(concat_data)
#     tagging_df.to_csv('./삼성전자단어하락장(3.16-19).csv',mode='w',encoding='utf-8-sig',header=True,index=True)
#
#
#
# with open('삼성전자.csv','r',encoding='UTF8') as f:
#     reader = csv.reader(f)
#
#     for a in reader:
#         text_analyzed = rhinoMorph.onlyMorph_list(rn, a[1], pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR','MM','NV','NF'], eomi=True)
#         #print("\n", count, ". 형태소 분석 결과:", text_analyzed)
#         #joined_data_each = ' '.join(text_analyzed)  # 문자열을 하나로 연결
#         for w in text_analyzed:
#             if w not in stop_words_list:  # 내용이 있는 경우만 저장
#                 morphed_data += a[2] + "\t" + w + "\n"
#
#         count += 1
#
# print(morphed_data)
# write_data(morphed_data, 'rating_삼성전자.txt', encoding='UTF8')
# data = read_data('rating_삼성전자.txt', encoding='UTF8')
#
# # date_day = [line[0] for line in data]
# data_text = []
# # date = datetime.datetime.strptime(date_day[0], "['%Y.%m.%d %H:%M']")
# date_start = datetime.datetime.strptime("['2020.03.16 00:00']", "['%Y.%m.%d %H:%M']")
# date_end = datetime.datetime.strptime("['2020.03.19 23:59']", "['%Y.%m.%d %H:%M']")
# for line in data:
#     date = datetime.datetime.strptime(line[0], "['%Y.%m.%d %H:%M']")
#     if date_start < date and date_end > date:
#         print(date)
#         text = line[1]
#         data_text.append(text)
#         #print(data_text)
#
# mergedText = ' '.join(data_text)
# print(mergedText)
# mergeTextList = mergedText.split(' ')
# wordInfo = Counter(mergeTextList)
#
# sorted_keys = sorted(wordInfo, key=wordInfo.get, reverse=True)
# sorted_values = sorted(wordInfo.values(), reverse=True)
#
# concating(date_start, date_end, sorted_keys, sorted_values)
#
# #그래프
# # plt.bar(range(50),sorted_values[:50])
# # plt.xticks(range(50),sorted_keys[:50])
# # plt.show()
# #
# # cloud = WordCloud(font_path=font_path, width=800, height=600).generate(" ".join(data_text))
# # plt.imshow(cloud, interpolation='bilinear') # 글자를 부드럽게
# # plt.axis('off')
# # plt.show()
#
# #긍정, 부정, 중립 사전 분류
# # font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'
# #
# # font_name = font_manager.FontProperties(fname=font_path).get_name()
# #
# # matplotlib.rc('font', family=font_name)
# #
# # os.chdir("/Users/parkn/Desktop/삼성전자2/")
# # rn = rhinoMorph.startRhino()
# #
# # positive_data=''
# # negative_data=''
# # neu_data=''
# # count = 1
# #
# # def write_data(data, filename, encoding='UTF8'):
# #     with open(filename, 'w', encoding=encoding) as f:
# #         f.write(data)
# #
# # with open('전체형태소_삼성전자.csv','r',encoding='UTF8') as f:
# #     reader = csv.reader(f)
# #
# #     for a in reader:
# #         if a[2] == '-1':
# #             negative_data += a[0] + "\n"
# #         elif a[2] == '1':
# #             positive_data += a[0] + "\n"
# #         else:
# #             neu_data += a[0] + "\n"
# #
# #         count += 1
# #
# # write_data(positive_data,'긍정_전체형태소_감성사전.txt', encoding='UTF8')
# # write_data(negative_data, '부정_전체형태소_감성사전.txt', encoding='UTF8')
# # write_data(neu_data,'중립_감성사전.txt', encoding='UTF8')


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
                    positive_cnt+=1
                elif w in negative_words_list:
                    negative_cnt-=1
        cnt_result.append(positive_cnt+negative_cnt)
        date_result.append(a[2])
        title_result.append(a[1])


        positive_cnt = 0
        negative_cnt = 0
        count += 1

concat_data={'date':date_result,
             'title':title_result,
             'pos/neg':cnt_result}
analyzed_df=pd.DataFrame(concat_data)
analyzed_df.to_csv('./긍부정추가된 데이터 셋.csv', mode='w',encoding='utf-8-sig',header=True,index=True)