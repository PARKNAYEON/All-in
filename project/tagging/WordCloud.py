import csv
import os
from tkinter import Image

import collections
import matplotlib
import rhinoMorph
from matplotlib import font_manager

import numpy as np

#wordcloud 라이브러리
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

'''
WordCloud.py
단어 빈도수 파악해서 원하는 모양에 워드클라우드 생성(기간도 정할 수 있음)

def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs) : 긍정적 워드클라우드 색 지정 함수
def blue_color_func(word, font_size, position, orientation, random_state=None, **kwargs) : 부정적 워드클라우드 색 지정 함수
def wordcloud(filename, stop_dic, positive_dic, negative_dic) : 단어 태깅하고 워드클라우드 그리는 함수

'''

try:
    os.chdir("/Users/parkn/Desktop/삼성전자2/")
    print("Directory changed")
except OSError:
    print("Can't change the Current Working Directory")


font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'

font_name = font_manager.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_name)

def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 67%%, %d%%)" % np.random.randint(60,100))


def blue_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(208, 63%%, %d%%)" % np.random.randint(60,100))


def wordcloud(filename, stop_dic, positive_dic, negative_dic):

    csv_count = 1
    count = 1

    rn = rhinoMorph.startRhino()
    
    stop_words_list = []
    positive_words_list=[]
    negative_words_list=[]
    s_file_name = open(stop_dic+'.txt', 'r', encoding='utf-8')
    positive_file = open(positive_dic+'.txt', 'r', encoding='utf=8')
    negative_file = open(negative_dic+'.txt', 'r', encoding='utf=8')

    # 긍정 부정 중립 사전을 각각의 리스트에 넣음
    for line in s_file_name.readlines(): 
        stop_words_list.append(line.rstrip())

    for line in positive_file.readlines():
        positive_words_list.append(line.rstrip())

    for line in negative_file.readlines():
        negative_words_list.append(line.rstrip())

    s_file_name.close()
    positive_file.close()
    negative_file.close()


    result_positive_words = [] # 조건에 통가한 긍정적인 단어
    result_negative_words = [] # 조건에 통가한 부정적인 단어

    with open(filename + '.csv', 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            for a in reader:

                if a[3] == 'date': # 불필요한 거 continue
                    continue
                present_date = datetime.datetime.strptime(a[3], '%Y.%m.%d %H:%M') # 비교할 시간 가져오기
                
                # 기간을 정해서 분기별로 가져오거나 달별로 가져오거나  1년 단위로 가져오거나 함 ****
                start_date = datetime.datetime(2020, 1, 1, 00, 00)
                end_date = datetime.datetime(2020, 3, 31, 23, 59) 

                if start_date <= present_date <= end_date:
                    text_analyzed = rhinoMorph.onlyMorph_list(rn, a[2], pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR','MM','NV','NF'], eomi=True)
                    for w in text_analyzed:
                        if w not in stop_words_list:  # 내용이 있는 경우만 저장
                            if w in positive_words_list: # 긍정일 때
                                result_positive_words.append(w)
                            elif w in negative_words_list: # 부정일 때
                                result_negative_words.append(w)

            # 긍정적인 단어 워드클라우드
            posi_counts = collections.Counter(result_positive_words) # 딕셔너리 형식으로 단어 빈도수 
            posi_icon = Image.open('./저금통.png') # 이미지 가져오기
            posi_mask = Image.new("RGB", posi_icon.size, (255,255,255))
            posi_mask.paste(posi_icon, posi_icon)
            posi_mask =np.array(posi_mask)
            posi_wc = WordCloud(font_path, background_color='#333333', width=800, height=600, max_words=200, mask=posi_mask)
            posi_cloud = posi_wc.generate_from_frequencies(posi_counts)
            plt.figure(figsize=(10,10))
            plt.axis('off')
            plt.imshow(posi_cloud.recolor(color_func=red_color_func), interpolation="bilinear")
            plt.show()
            
            # 부정적인 단어 워드클라우드
            nega_counts = collections.Counter(result_negative_words) # 딕셔너리 형식으로 단어 빈도수 
            nega_icon = Image.open('./쪼개진저금통.png') # 이미지 가져오기
            nega_mask = Image.new("RGB", nega_icon.size, (255,255,255))
            nega_mask.paste(nega_icon, nega_icon)
            nega_mask =np.array(nega_mask)
            nega_wc = WordCloud(font_path, background_color='#333333', width=800, height=600, max_words=200, mask=nega_mask)
            nega_cloud = nega_wc.generate_from_frequencies(nega_counts)
            plt.figure(figsize=(10,10))
            plt.axis('off')
            plt.imshow(nega_cloud.recolor(color_func=blue_color_func), interpolation="bilinear")
            plt.show()
            

if __name__ == "__main__":
    wordcloud('merge_000660')