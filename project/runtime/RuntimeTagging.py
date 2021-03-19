import csv
import os
import datetime
import time
import crawling
import pandas as pd
import rhinoMorph

# 실시간 연동을 위한 라이브러리
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from apscheduler.schedulers.background import BackgroundScheduler

'''
RuntimeTagging.py

구글 스프레드 api를 불러와서 sched.scheduled_job을 사용해 3시간마다 크롤링 된 원본 데이터 분석

spreadsheet_url : 구글 스프레드 시트가 있는 위치
doc : 문서 불러오기
worksheet : 문서의 이름

'''


scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

# 인터넷이 사용가능할 때 작동됨
key_file_name = 'all-in.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_name, scope)
gc = gspread.authorize(credentials)

# 각자에게 맞는 환경 설정
os.chdir("/Users/parkn/Desktop/삼성전자2/")


sched = BackgroundScheduler()
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1D7_U8eEJMbHSuM_IzKtSEtiAvSygQgjwckBE95XRkHk/edit#gid=0'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('시트1')

c = 1


# WordingTotalTagging.py 와 비슷한 알고리즘
@sched.scheduled_job('interval', hours=3, id='realtime_wordtagging')
def realtime_wordtagging():
    #debugging
    print({time.strftime("%H:%M:%S")})


    rn = rhinoMorph.startRhino()
    csv_count = 1
    count = 1

    stop_words_list = []
    positive_words_list = []
    negative_words_list = []
    s_file_name = open('중립_감성사전.txt', 'r', encoding='utf-8')
    positive_file = open('긍정_전체형태소_감성사전.txt', 'r', encoding='utf=8')
    negative_file = open('부정_전체형태소_감성사전.txt', 'r', encoding='utf=8')
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
    cnt_result = []
    title_result = []
    date_result = []
    view_result = []
    like_result = []
    dislike_result = []

    with open('merge_035420.csv', 'r', encoding='UTF8') as f:
        reader = csv.reader(f)

        for a in reader:
            text_analyzed = rhinoMorph.onlyMorph_list(rn, a[2],
                                                      pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR', 'MM', 'NV',
                                                           'NF'], eomi=True)
            # print("\n", count, ". 형태소 분석 결과:", text_analyzed)
            # joined_data_each = ' '.join(text_analyzed)  # 문자열을 하나로 연결
            if a[2] == 'title':
                continue
            for w in text_analyzed:
                if w not in stop_words_list:  # 내용이 있는 경우만 저장
                    if w in positive_words_list:
                        positive_cnt += 1
                    elif w in negative_words_list:
                        negative_cnt -= 1
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

    concat_data = {'code': code_result,
                   'date': date_result,
                   'title': title_result,
                   'views': view_result,
                   'like': like_result,
                   'dislike': dislike_result,
                   'pos/neg': cnt_result}

    analyzed_df = pd.DataFrame(concat_data)
    set_with_dataframe(worksheet, analyzed_df)


# 시작 설정
if __name__ == "__main__":
    print("start")
    sched.start()
    print('end')

    while True:
        time.sleep(1)