import csv
import os
import datetime
from collections import Counter

import matplotlib
import pandas as pd

from matplotlib import font_manager

os.chdir("/Users/parkn/Desktop/삼성전자2/")

stock_date = []
date_data = []

def read_stock_data(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)

        for a in reader:
            if a[0] == 'Date':
                continue

            date_data.append(a[0])
            start = int(a[3])
            end = int(a[4])
            compare = end - start  # 빼서 비교할 수도 있고
            # 장이 시작될 때의 가격을 기준으로 할 수도 있다
            # print(compare)
            stock_date.append(compare)
            com_data = {'date': date_data,
                        '떨어진 정도': stock_date,
                       }
            compare_df = pd.DataFrame(com_data)
            compare_df.to_csv('./2020 주가 변동 폭.csv', mode='w', encoding='utf-8-sig', header=True, index=True)

def compare_ratio(stockfilename, posnegfilename):
    match_rate = 0
    not_match_rate = 0
    with open(stockfilename, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        for a in reader:
            if a[1] == 'date':
                continue
            stock = datetime.date.fromisoformat(a[1])
            #print(stock)
            with open(posnegfilename, 'r', encoding='UTF8') as f:
                reader = csv.reader(f)
                for b in reader:
                    if b[2] == 'end date':
                        continue
                    st = b[2].replace(" 15:30:00", "")
                    #print(st)
                    posneg = datetime.date.fromisoformat(st)
                    if stock == posneg:
                        if int(a[2]) <= 0:
                            if float(b[5]) <= 0:
                                print(posneg)
                                print(a[2])
                                print(b[5])
                                match_rate = match_rate + 1
                        if int(a[2]) > 0:
                            if float(b[5]) > 0:
                                print(posneg)
                                print(a[2])
                                print(b[5])
                                match_rate = match_rate + 1
                        if int(a[2]) > 0:
                            if float(b[5]) < 0:
                                not_match_rate = not_match_rate + 1
                        if int(a[2]) < 0:
                            if float(b[5]) > 0:
                                not_match_rate = not_match_rate + 1

    print(match_rate)
    print(not_match_rate)
    result_rate = match_rate / (match_rate + not_match_rate)
    print(result_rate)

def posneg_matching(filename):
    year_ = 2020
    month_ = 1
    day_ = 1

    start_data = []
    end_data = []
    compare_data = []
    posi_data = []
    nega_data = []
    for i in range(365):
        start_date = datetime.datetime(year_, month_, day_, 18, 00)
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
        count = 0

        with open(filename, 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            for a in reader:
                if a[2] == 'date':
                    continue
                present_date = datetime.datetime.strptime(a[2], '%Y.%m.%d %H:%M')
                # print(start_date)
                # print(end_date)
                count = count + 1
                # print(count)
                if start_date < present_date < end_date:
                    # 여기서의 긍부정 표시하기!! -> 이걸 액셀 파일로 올려서 두 개의 파일을 비교하기 그래서 어느정도의 정확도를 가지고 있는지(우리는 등락의 폭을 계산하는 건 무리)
                    if int(a[7]) > 0:  # 긍정 글이면 1, 2 상관없이 +1로 체크하려고 하는데 이부분 의논 필요
                        positive_emo = positive_emo + 1
                    if int(a[7]) < 0:
                        negative_emo = negative_emo + 1

        # print(str(year_) + str(month_) + str(day_) + str(positive_emo - negative_emo))
        start_data.append(start_date)
        end_data.append(end_date)
        posi_data.append(positive_emo)
        nega_data.append(negative_emo)
        compare_data.append(positive_emo*1.93 - negative_emo)

    print(compare_data)
    com_data = {'start date':start_data,
                'end date' : end_data,
                'posi' : posi_data,
                'nega' : nega_data,
                'posneg':compare_data}
    compare_df = pd.DataFrame(com_data)
    compare_df.to_csv('./2020 매칭율 긍부정 나누기 (시간오후6시부터).csv',mode='w',encoding='utf-8-sig',header=True,index=True)

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


#read_stock_data('삼성_주가.csv')
#print(stock_date)
#posneg_matching('삼성전자 긍부정추가된 데이터 셋2.csv')
compare_ratio('2020 주가 변동 폭.csv', '2020 매칭율 긍부정 나누기(장중).csv')