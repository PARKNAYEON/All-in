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
            compare = end - start
            #print(compare)
            temp_data.append(compare)
            stock_date.append(temp_data)

year_ = 2020
month_ = 1
day_ = 1


def posneg_matching(filename):
    global year_
    global month_
    global day_
    with open(filename, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)

        for a in reader:
            start_date = datetime.datetime(year_, month_, day_, 9, 0)
            end_date = datetime.datetime(year_, month_, day_, 15, 30)
            print(start_date)
            print(end_date)
            if a[0] == 'date':
                continue
            # for c in stock_date:
            #     if c == datetime.datetime(a[0]):
            #         print(datetime.datetime(a[0]))

                #if a[0] > start_date & a[0] < end_date:
            day_ = day_ + 1
            print(day_)
            print(month_%2)
            if month_ == 2:
                if day_ == 30:
                    day_ = 1
                    month_ = 3
            if day_ == 31:
                if month_ % 2 == 0:
                    day_ = 1
                    month_ = month_ + 1
            if day_ == 32:
                if month_ % 2 == 1:
                    day_ = 1
                    month_ = month_ + 1




read_stock_data('삼성_주가.csv')
posneg_matching('삼성전자 긍부정추가된 데이터 셋.csv')


