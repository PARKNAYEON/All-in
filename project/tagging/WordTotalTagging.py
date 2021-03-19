import csv
import os
import datetime
from collections import Counter

import matplotlib
import pandas as pd
import rhinoMorph

'''
WordTatalTagging.py

rhinoMorph를 사용해서 형태소를 분석한 후 사전에 만들어둔 감성사전(txt 파일)에 있는 단어들과 비교 및 분석

s_file_name : 중립 감성사전 및 불용어 사전
positive_file : 긍정 사전
negative_file : 부정 사전

positive_cnt : 긍정 개수를 count하기 위한 변수
negative_cnt : 부정 개수를 count하기 위한 변수

'''

# 각자의 환경변수에 맞게 수정 필요
os.chdir("C:/Users/**/Desktop/감성사전")

def totalTagging(filenanme, stop_dic, positive_dic, negative_dic):
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
  
    
    positive_cnt = 0
    negative_cnt = 0

    
    code_result = []
    title_result = []
    date_result = []
    view_result = []
    like_result = []
    dislike_result = []
    cnt_result = [] # 긍부정 최종 결과 넣기

    # 분석할 파일 불러오기
    with open(filenanme+'.csv','r',encoding='UTF8') as f:
        reader = csv.reader(f)

        # title 한 줄씩 읽어옴
        for a in reader:
            text_analyzed = rhinoMorph.onlyMorph_list(rn, a[2], pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR','MM','NV','NF'], eomi=True)
            
            #debugging
            #print("\n", count, ". 형태소 분석 결과:", text_analyzed)
            #joined_data_each = ' '.join(text_analyzed)  # 문자열을 하나로 연결


            for w in text_analyzed:
                if w not in stop_words_list:  # 내용이 있는 경우만 저장
                    if w in positive_words_list: # 긍정일 때
                        positive_cnt += 1
                    elif w in negative_words_list: # 부정일 때
                        negative_cnt -= 1

            # 각 결과 리스트에 추가            
            cnt_result.append(positive_cnt + negative_cnt)
            code_result.append(a[1])
            date_result.append(a[3])
            title_result.append(a[2])
            view_result.append(a[4])
            like_result.append(a[5])
            dislike_result.append(a[6])
            positive_cnt = 0
            negative_cnt = 0
            count += 1
           

    # 딕셔너리로 변환
    concat_data={'code':code_result,
                'date':date_result,
                'title':title_result,
                'views':view_result,
                'like':like_result,
                'dislike':dislike_result,
                'pos/neg':cnt_result}
    # 데이터프레임에 넣기
    analyzed_df=pd.DataFrame(concat_data)
    analyzed_df.to_csv('./전체_직접은어_긍부정포함데이터.csv', mode='w',encoding='utf-8-sig',header=True,index=True)


# 시작 지점
if __name__ == '__main__':
    # 넣어야 하는 분석기준, 중립, 긍정, 부정 파일
    totalTagging('a_total_file', '중립_감성사전', '긍정_전체형태소_감성사전', '부정_전체형태소_감성사전')