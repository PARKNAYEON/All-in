import csv
import os
import datetime


os.chdir("/Users/parkn/Desktop/주가변동 및 매칭율")



def compare_ratio(stock_filename, posneg_filename):
    match_rate = 0
    not_match_rate = 0
    with open(stock_filename + '.csv', 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        for a in reader:
            if a[1] == 'date':
                continue
            stock = datetime.date.fromisoformat(a[1])
            # print(stock)
            with open(posneg_filename + '.csv', 'r', encoding='UTF8') as f:
                reader = csv.reader(f)
                for b in reader:
                    if b[2] == 'end date':
                        continue
                    st = b[2].replace(" 15:30:00", "")
                    # print(st)
                    posneg = datetime.date.fromisoformat(st)
                    if stock == posneg:
                        if float(a[2]) <= 0:
                            if float(b[5]) <= 0:
                                print(posneg)
                                print(a[2])
                                print(b[5])
                                match_rate = match_rate + 1
                        if float(a[2]) > 0:
                            if float(b[5]) > 0:
                                print(posneg)
                                print(a[2])
                                print(b[5])
                                match_rate = match_rate + 1
                        if float(a[2]) > 0:
                            if float(b[5]) < 0:
                                not_match_rate = not_match_rate + 1
                        if float(a[2]) < 0:
                            if float(b[5]) > 0:
                                not_match_rate = not_match_rate + 1

    print(match_rate)
    print(not_match_rate)
    result_rate = match_rate / (match_rate + not_match_rate)
    print(result_rate)

compare_ratio('2020 068270.KS_주가변동 폭', '2020 068270_직접은어주가_긍부정포함데이터 장중 매칭율')