import csv
import os
import datetime
from collections import Counter

import matplotlib
import pandas as pd

from matplotlib import font_manager

os.chdir("/Users/parkn/Desktop/삼성전자2/")

stock_date = []


def read_stock_data(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)

        for a in reader:
            if a[0] == 'Date':
                continue
            temp_data = []
            temp_data.append(a[0])
            start = int(a[3])
            end = int(a[4])
            compare = end - start  # 빼서 비교할 수도 있고
            # 장이 시작될 때의 가격을 기준으로 할 수도 있다
            # print(compare)
            temp_data.append(compare)
            stock_date.append(temp_data)


def posneg_matching(filename):
    year_ = 2020
    month_ = 1
    day_ = 1

    compare_data = []
    with open(filename, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)

        for i in range(365):
            start_date = datetime.datetime(year_, month_, day_, 15, 30)
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
            end_date = datetime.datetime(year_, month_, day_, 9, 00)

            positive_emo = 0
            negative_emo = 0

            for a in reader:
                if a[1] == 'date':
                    continue
                present_date = datetime.datetime.strptime(a[1], '%Y.%m.%d %H:%M')
                if start_date < present_date < end_date:
                    # 여기서의 긍부정 표시하기!! -> 이걸 액셀 파일로 올려서 두 개의 파일을 비교하기 그래서 어느정도의 정확도를 가지고 있는지(우리는 등락의 폭을 계산하는 건 무리)
                    if int(a[6]) > 0:  # 긍정 글이면 1, 2 상관없이 +1로 체크하려고 하는데 이부분 의논 필요
                        positive_emo = positive_emo + 1
                    if int(a[6]) < 0:
                        negative_emo = negative_emo + 1

            print(str(year_)+str(month_)+str(day_)+str(positive_emo+negative_emo))
            compare_data.append(positive_emo+negative_emo)

        print(compare_data)

        # for s in stock_date:
        #     stock = datetime.datetime.strptime(s[0], '%Y-%m-%d')
        #     start_date = datetime.datetime(year_, month_, day_, 15, 30)
        #     day_ = day_ + 1
        #     # print(day_)
        #     # print(month_%2)
        #     if month_ == 2:
        #         if day_ == 30:
        #             day_ = 1
        #             month_ = 3
        #     if month_ == 1 or month_ == 3 or month_ == 5 or month_ == 7 or month_ == 8 or month_ == 10 or month_ == 12:
        #         if day_ == 32:
        #             day_ = 1
        #             month_ = month_ + 1
        #     if month_ == 4 or month_ == 6 or month_ == 9 or month_ == 11:
        #         if day_ == 31:
        #             day_ = 1
        #             month_ = month_ + 1
        #     if month_ == 13:
        #         break
        #     end_date = datetime.datetime(year_, month_, day_, 9, 00)
        #     for a in reader:
        #         if a[1] == 'date':
        #             continue
        #         #여기서의 긍부정 표시하기!! -> 이걸 액셀 파일로 올려서 두 개의 파일을 비교하기 그래서 어느정도의 정확도를 가지고 있는지(우리는 등락의 폭을 계산하는 건 무리)
        #         present_date = datetime.datetime.strptime(a[1], '%Y.%m.%d %H:%M')
        #         if start_date < present_date < end_date:
        #
        #
        #         # for c in stock_date:
        #         #     if c == datetime.datetime(a[0]):
        #         #         print(datetime.datetime(a[0]))
        #
        #             #if a[0] > start_date & a[0] < end_date:
        #
        #


read_stock_data('삼성_주가.csv')
print(stock_date)
posneg_matching('삼성전자 긍부정추가된 데이터 셋.csv')
