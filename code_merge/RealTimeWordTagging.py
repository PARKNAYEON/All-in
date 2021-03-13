import csv
import os
import datetime
import gspread
import time
import crawling

from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

import matplotlib
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import rhinoMorph
from matplotlib import font_manager

font_path = 'C:/Users/parkn/Desktop/맑은고딕/malgun.ttf'

font_name = font_manager.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_name)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

key_file_name = 'all-in.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_name, scope)
gc = gspread.authorize(credentials)

os.chdir("/Users/parkn/Desktop/삼성전자2/")

sched = BackgroundScheduler()
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1D7_U8eEJMbHSuM_IzKtSEtiAvSygQgjwckBE95XRkHk/edit#gid=0'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('시트1')

c = 1



@sched.scheduled_job('interval', seconds=1, id='realtime_wordtagging')
def realtime_wordtagging():
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


if __name__ == "__main__":
    print("start")
    sched.start()
    print('end')

    code_list = ['005930', '0006600']
    # for i in code_list:
    #     instane = crawling.crawling(code=code_list)
    #     sched.add_job(instane.web_scraping(),

    while True:
        time.sleep(1)
