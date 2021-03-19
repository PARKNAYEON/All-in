# 파이선 데이터베이스 연동

'''
Dictionary.py
감성사전 테이블 생성 및 삽입

'''

import sqlite3
import string

# 각자 환경에 따라 경로 설정하기
conn = sqlite3.connect('C:/Users/netid/Desktop/project/db/dic.db', isolation_level=None)
c = conn.cursor()

def createTable():
    c.execute("CREATE TABLE IF NOT EXISTS neutral(word text)") 
    c.execute("CREATE TABLE IF NOT EXISTS positive(word text)") 
    c.execute("CREATE TABLE IF NOT EXISTS negative(word text)") 

def insertData(filename, name):
    
    with open(filename) as f:
        file_data = f.readlines()

        for i in file_data:
            temp = string.split(i)
            word = str(temp)
            c.execute("INSERT INTO " + name + "(word) VALUES(?)",word)

if __name__ == '__main__':
    createTable()
    # insertData("긍정_전체형태소_감성사전.txt", "positive")
    conn.close()
