import csv
import os
import datetime
from collections import Counter

import matplotlib
import pandas as pd

from matplotlib import font_manager

os.chdir("/Users/parkn/Desktop/삼성전자2/")

'''
MatchingWord.py
매칭율을 비교하기 위한 데이터 수집

def read_stock_data(filename) 
: 주가 데이터 파일에 있는 날짜별 시가와 종가를 파악해서 하나의 파일로 만드는 함수
: ((종가 - 시가)/ 시가) * 100

def posneg_matching(filename) 
: 기간내에 긍정, 부정, 중립의 개수 파악할 수 있는 함수


'''

stock_date = []
date_data = []


def read_stock_data(filename):
    with open(filename + '.csv', 'r', encoding='UTF8') as f:
        reader = csv.reader(f)

        # 파일 읽어오기
        for a in reader:
            if a[0] == 'Date': # 불필요한 단어 continue
                continue
            
            date_data.append(a[0]) # 날짜 데이터 추가
            start = float(a[3]) # 시가
            end = float(a[4]) # 종가
            compare = (end - start)  # 종가 - 시가
            ratio = (compare/start) * 100 # 하락 상승률 파악을 위해서 ** 중요

            stock_date.append(ratio)

            com_data = {'date': date_data,
                        '등락폭': stock_date,
                        }
            compare_df = pd.DataFrame(com_data)
            compare_df.to_csv('./2020 ' + filename + '변동 폭.csv', mode='w', encoding='utf-8-sig', header=True,
                              index=True)


def posneg_matching(filename, start_hour, start_min, end_hour, end_min):
    # 2020년 기준
    year_ = 2020
    month_ = 1
    day_ = 1

    start_data = []
    end_data = []
    posi_data = []
    nega_data = []
    neu_data = []

    # 1년 동안의 날짜 비교
    for i in range(365):
        start_date = datetime.datetime(year_, month_, day_, start_hour, start_min)
        end_date = datetime.datetime(year_, month_, day_, end_hour, end_min)
        day_ = day_ + 1

        if month_ == 2:
            if day_ == 30:
                day_ = 1
                month_ = 3
        if month_ == 1 or month_ == 3 or month_ == 5 or month_ == 7 or month_ == 8 or month_ == 10 or month_ == 12:
            if day_ == 32:
                day_ = 1
                month_ = month_ + 1
        if month_ == 4 or month_ == 6 or month_ == 9 or month_ == 11:
            if day_ == 31:
                day_ = 1
                month_ = month_ + 1
        if month_ == 13:
            break


        positive_emo = 0 # 긍정 개수
        negative_emo = 0 # 부정 개수
        neu_emo = 0 # 중립 개수
        total_emo = 0 # 긍정 부정 중립 전체 개수

        count = 0

        with open(filename + '.csv', 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            for a in reader:

                if a[2] == 'date':
                    continue
                present_date = datetime.datetime.strptime(a[2], '%Y.%m.%d %H:%M') # 비교할 시간 가져오기
                count = count + 1
                if start_date < present_date < end_date: # 비교하는 날짜가 여기에 속할 경우
                    if int(a[7]) > 0: # 긍정
                        positive_emo = positive_emo + 1
                    if int(a[7]) < 0: # 부정
                        negative_emo = negative_emo + 1
                    if int(a[7]) == 0: # 중립
                        neu_emo = neu_emo + 1

        # check
        # print(str(year_) + str(month_) + str(day_) + str(positive_emo - negative_emo))
        
        total_emo = positive_emo + negative_emo + neu_emo

        start_data.append(start_date)
        end_data.append(end_date)
        posi_data.append(positive_emo/total_emo)
        nega_data.append(negative_emo/total_emo)
        neu_data.append(neu_emo/total_emo)

    print(compare_data)
    com_data = {'start date': start_data,
                'end date': end_data,
                'posi': posi_data,
                'nega': nega_data,
                'neu': neu_data}
    compare_df = pd.DataFrame(com_data)
    compare_df.to_csv('./2020 ' + filename + ' 장중 매칭율.csv', mode='w', encoding='utf-8-sig', header=True,
                      index=True)


# 시작 지점
if __name__ == '__main__':
    read_stock_data('005935.KS_주가')
    posneg_matching('068270_직접은어주가_긍부정포함데이터', 9, 00, 15, 30)