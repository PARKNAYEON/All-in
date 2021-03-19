  
import csv
import os
import datetime
from collections import Counter

import pandas as pd
import rhinoMorph

os.chdir("/Users/parkn/Desktop/삼성전자2/")

'''
DateTagging.py
날짜에 따라 형태소 & 빈도수 분석 -> 상승장 하락장에서 많이 나오는 단어들을 알기 위한 알고리즘

def write_data(data, filename, encoding='UTF8') : 쓰기 함수
def read_data(filename, encoding='UTF8') : 읽기 함수
def concating(startdate,enddate, key_result,value_result) : 데이터 프레임을 사용해 csv 파일로 저장하는 함수

def dateTagging(filename, s_file) : 날짜별 형태소 분석 및 빈도수 파악 (메인함수)


'''


def write_data(data, filename, encoding='UTF8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)

def read_data(filename, encoding='UTF8'):
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]  # txt 파일의 헤더는 제외
    return data

def concating(startdate,enddate, key_result,value_result):
    concat_data={'형태소': key_result,
                 '빈도수': value_result}
    tagging_df=pd.DataFrame(concat_data)
    tagging_df.to_csv('./삼성전자단어하락장(3.16-19).csv',mode='w',encoding='utf-8-sig',header=True,index=True)



def dateTagging(filename, s_file, start_date, end_date):

    csv_count = 1
    count = 1
    
    morphed_data = ''
    stop_words_list = []
    rn = rhinoMorph.startRhino()

    s_file_name = open(s_file+'.txt', 'r', encoding='utf-8')
    for line in s_file_name.readlines():
        stop_words_list.append(line.rstrip())

    s_file_name.close()
    # debugging
    print(stop_words_list)

    # 분석할 파일 열기
    with open(filename+'.csv','r',encoding='UTF8') as f:
        reader = csv.reader(f)

        for a in reader:
            text_analyzed = rhinoMorph.onlyMorph_list(rn, a[1], pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR','MM','NV','NF'], eomi=True)
            for w in text_analyzed:
                if w not in stop_words_list:  # 내용이 있는 경우만 저장
                    morphed_data += a[2] + "\t" + w + "\n"

            count += 1

    # 형태소 별로 나눈 morphed_data를 쓰고 다시 읽기(이 과정 불필요 할 수도 나중에 수정)
    write_data(morphed_data, 'rating_삼성전자.txt', encoding='UTF8')
    data = read_data('rating_삼성전자.txt', encoding='UTF8')

    # 날짜 내에 들어가는 단어 리스트에 저장
    data_text = []

    # 날짜가 들어와있는 형식에 따라 변경 필요
    date_start = datetime.datetime.strptime(start_date, "['%Y.%m.%d %H:%M']") # 시작 날짜
    date_end = datetime.datetime.strptime(end_date, "['%Y.%m.%d %H:%M']") # 끝 날짜

    # 비교 시간 가져오기
    for line in data:
        date = datetime.datetime.strptime(line[0], "['%Y.%m.%d %H:%M']") # 비교될 시간
        if date_start < date and date_end > date: # 날짜 안에 들어와있을 경우
            text = line[1] # 텍스트 추가
            data_text.append(text)

    mergedText = ' '.join(data_text)
    mergeTextList = mergedText.split(' ')
    wordInfo = Counter(mergeTextList) # 빈도수 체크

    sorted_keys = sorted(wordInfo, key=wordInfo.get, reverse=True) # 단어는 key
    sorted_values = sorted(wordInfo.values(), reverse=True) # 빈도수는 value

    concating(date_start, date_end, sorted_keys, sorted_values)


# 시작 지점
if __name__ == '__main__':
    dateTagging('삼성전자', '중립_감성사전',"['2020.03.16 00:00']" , "['2020.03.19 23:59']")