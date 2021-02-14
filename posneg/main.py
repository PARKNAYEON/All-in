import csv
import os
import datetime
from collections import Counter

import pandas as pd


os.chdir("/Users/parkn/Desktop/삼성전자2/")

positive_lists=[]
negative_lists=[]

def write_data(data, filename, encoding='UTF8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)

def read_data(filename, encoding='UTF8'):
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]  # txt 파일의 헤더는 제외
    return data



with open('삼성전자단어상승장.csv', 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    count = 0
    for a in reader:
        positive_lists.append(a[1])
        count+=1
        if count == 300:
            break

with open('삼성전자단어하락장.csv', 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    count = 0
    for a in reader:
        negative_lists.append(a[1])
        count += 1
        if count == 300:
            break

increase = ''
decrease = ''
posi_cnt = 0
nega_cnt = 0

for i in positive_lists:
    posi_cnt+=1
    nega_cnt = 0
    for j in negative_lists:
        nega_cnt+=1
        if i == j:
            if posi_cnt < nega_cnt:
                increase += i + "\n"
                continue

posi_cnt = 0
nega_cnt = 0

for i in negative_lists:
    nega_cnt+=1
    posi_cnt = 0
    for j in positive_lists:
        posi_cnt+=1
        if i == j:
            #print(i)
            #print(posi_cnt, ",", nega_cnt)
            if posi_cnt > nega_cnt:
                decrease += i + "\n"
                continue

write_data(increase, '주가에 따른 단어 분류_상승.txt', encoding='UTF8')
write_data(decrease, '주가에 따른 단어 분류_하락.txt', encoding='UTF8')