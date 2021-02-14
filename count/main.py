import csv
import os
import datetime
from collections import Counter

import pandas as pd


os.chdir("/Users/parkn/Desktop/삼성전자2/")

positive_lists=[]
negative_lists=[]
stock_posi_lists=[]
stock_nega_lists=[]

def write_data(data, filename, encoding='UTF8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)

def read_data(filename, encoding='UTF8'):
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]  # txt 파일의 헤더는 제외
    return data

def append_list(listname, filename):
    for line in filename.readlines():
        listname.append(line.rstrip())


positive_file = open('긍정_전체형태소_감성사전.txt', 'r', encoding='utf=8')
negative_file = open('부정_전체형태소_감성사전.txt', 'r', encoding='utf=8')
stock_positive_file = open('주가에 따른 단어 분류_상승.txt', 'r', encoding='utf=8')
stock_negative_file = open('주가에 따른 단어 분류_하락.txt', 'r', encoding='utf=8')

append_list(positive_lists,positive_file)
append_list(negative_lists,negative_file)
append_list(stock_posi_lists,stock_positive_file)
append_list(stock_nega_lists,stock_negative_file)

rate_positive = 0
for i in positive_lists:
    for j in stock_posi_lists:
        if(i == j):
            rate_positive+=1

print("주가에 따른 긍정 매칭율", rate_positive / len(stock_posi_lists))

rate_negative = 0
for i in negative_lists:
    for j in stock_nega_lists:
        if(i == j):
            rate_negative+=1

print("주가에 따른 부정 매칭율", rate_negative / len(stock_nega_lists))