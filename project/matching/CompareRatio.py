import csv
import os
import datetime

# 각자에게 맞는 환경 변수 설정
os.chdir("/Users/parkn/Desktop/주가변동 및 매칭율")

'''
CompareRatio.py

주가 변동폭과 상승 하락 비교해서 매칭율

def compare_ratio(stock_filename, posneg_filename) : 매칭된 날짜 수/전체 비교되는 날짜 수

'''

def compare_ratio(stock_filename, posneg_filename):

    match_rate = 0 # 매칭되는 개수
    total_count = 0 # 전체 비교되는 날짜 수

    # 주가 파일 불러오기
    with open(stock_filename + '.csv', 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        
        for a in reader:
            if a[1] == 'date':
                continue
            stock = datetime.date.fromisoformat(a[1]) # 주가 날짜 가져오기

            # 보합일 때는 중립글이 많은 것이 매칭율이 잘 된건가 뭘까 ** 여기 한번더 보기!
            # if -0.5 < stock < 0.5 : 
            #     continue

            total_count + = 1 

            # 매칭 비교할 파일 불러오기
            with open(posneg_filename + '.csv', 'r', encoding='UTF8') as f:
                reader = csv.reader(f)
                
                for b in reader:
                    if b[2] == 'end date':
                        continue
                    st = b[2].replace(" 15:30:00", "") # 뒤에 시간은 빼줌
                    # print(st)
                    posneg = datetime.date.fromisoformat(st) # 긍부정 날짜 가져오기
                    
                    if stock == posneg: # 날짜가 같으면
                        if float(a[2]) <= 0: # 변동폭이 -를 띄면
                            if float(b[3]) <= float(b[4]): # 그리고 부정이 더 크면
                                match_rate = match_rate + 1 # 매칭 성공
                                continue
                        if float(a[2]) > 0:
                            if float(b[3]) > float(b[4]):
                                match_rate = match_rate + 1 # 매칭 성공
                                continue

                        # if float(a[2]) > 0:
                        #     if float(b[5]) < 0:
                        #         not_match_rate = not_match_rate + 1
                        # if float(a[2]) < 0:
                        #     if float(b[5]) > 0:
                        #         not_match_rate = not_match_rate + 1

    print(match_rate)

    result_rate = match_rate / total_count # 전체 날짜 수에서 매칭된 날짜 수
    
    print(result_rate)


if __name__ == '__main__':
    compare_ratio('2020 068270.KS_주가변동 폭', '2020 068270_직접은어주가_긍부정포함데이터 장중 매칭율')