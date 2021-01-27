import csv
import os

from konlpy.tag import Hannanum
import rhinoMorph
import pandas as pd
from rhinoMorphExtension import calWordsFreq
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from matplotlib import font_manager, rc

font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'

font_name = font_manager.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_name)

os.chdir("/Users/parkn/Desktop/삼성전자2/")
rn = rhinoMorph.startRhino()
csv_count = 1
count = 1
morphed_data = ''
stop="때,오늘,삼전,게시물,답글,주식,이,하,되,주,ㅋ,ㅡ,다,오,내일,왜,말,지금,사,알,이제,ㅇ,푸"
stop_list=stop.split(',')

def write_data(data, filename, encoding='UTF8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)

def read_data(filename, encoding='UTF8'):
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]  # txt 파일의 헤더는 제외
    return data

def concating(key_result,value_result):
    concat_data={'형태소': key_result,
                 '빈도수': value_result}
    tagging_df=pd.DataFrame(concat_data)
    tagging_df.to_csv('./삼성전자단어빈도수.csv',mode='w',encoding='utf-8-sig',header=True,index=True)



# with open('삼성전자.csv','r',encoding='UTF8') as f:
#     reader = csv.reader(f)
#
#     for a in reader:
#         text_analyzed = rhinoMorph.onlyMorph_list(rn, a[1], pos=['NNG', 'VCP', 'VCN', 'IC', 'MAG', 'VA', 'VV', 'XR'])
#         #print("\n", count, ". 형태소 분석 결과:", text_analyzed)
#         #joined_data_each = ' '.join(text_analyzed)  # 문자열을 하나로 연결
#         for w in text_analyzed:
#             if w not in stop_list:  # 내용이 있는 경우만 저장
#                 morphed_data += a[2] + "\t" + w + "\n"
#
#         count += 1

#print(morphed_data)
#write_data(morphed_data, 'rating_삼성전자.txt', encoding='UTF8')
data = read_data('rating_삼성전자.txt', encoding='UTF8')
data_day = [line[0] for line in data]
data_text = [line[1] for line in data]
mergedText = ' '.join(data_text)
print(mergedText)
mergeTextList = mergedText.split(' ')
wordInfo = Counter(mergeTextList)

sorted_keys = sorted(wordInfo, key=wordInfo.get, reverse=True)
sorted_values = sorted(wordInfo.values(), reverse=True)

concating(sorted_keys, sorted_values)

#그래프
# plt.bar(range(50),sorted_values[:50])
# plt.xticks(range(50),sorted_keys[:50])
# plt.show()
#
# cloud = WordCloud(font_path=font_path, width=800, height=600).generate(" ".join(data_text))
# plt.imshow(cloud, interpolation='bilinear') # 글자를 부드럽게
# plt.axis('off')
# plt.show()
