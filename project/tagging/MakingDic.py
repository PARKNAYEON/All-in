import csv
import os

'''
MakingDic.py

분류한 전체 데이터들을 각각의 사전으로 만들기

def write_data(data, filename, encoding='UTF8') : 사전 쓰기 함수
def classifyword(filename) : 긍부정 분류 함수

positive_data : 긍정적인 단어 추가하는 곳
negative_data : 부정적인 단어 추가하는 곳
neu_data : 중립 단어 추가하는 곳

'''

# 각자의 환경 설정
os.chdir("/Users/parkn/Desktop/삼성전자2/")




def write_data(data, filename, encoding='UTF8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)


def classifyword(filename):
    positive_data = ''
    negative_data = ''
    neu_data = ''
    count = 1
    with open(filename+'.csv','r',encoding='UTF8') as f:
        reader = csv.reader(f)

        for a in reader:
            if a[2] == '-1':
                negative_data += a[0] + "\n"
            elif a[2] == '1':
                positive_data += a[0] + "\n"
            else:
                neu_data += a[0] + "\n"

            count += 1

    write_data(positive_data,'긍정_전체형태소_감성사전.txt', encoding='UTF8')
    write_data(negative_data, '부정_전체형태소_감성사전.txt', encoding='UTF8')
    write_data(neu_data,'중립_감성사전.txt', encoding='UTF8')


if __name__ == '__main__':
    classifyword('전체형태소_삼성전자')