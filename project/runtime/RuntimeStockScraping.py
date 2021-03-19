import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver # selenium 제어창에 대한 옵션
options=webdriver.ChromeOptions()
options.add_argument('--privileged')
options.add_argument('headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--start-maximized')
options.add_argument('disable-gpu')  # GPU 사용 안함
options.add_argument('lang=ko_KR')  # 언어 설정

'''
RuntimeStockScraping.py
네이버 금융에서 실시간으로 변하는 주가를 불러오는 부분.
scraping > WebScraping.py 과 비슷함 (참고)

'''

# 디렉토리 재설정
try:
    os.chdir("C:\\Users\\SAMSUNG\\Desktop\\") # Chromewebdriver가 있는 경로로 설정 
    print("Directory changed")
except OSError: # 예외처리
    print("Can't change the Current Working Directory")


def mkdir_data(directory): # 하위 디렉토리 생성
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Directory created")
    except OSError:
        print('Error: Creating directory.')


def stock_scraping(code, stock_date,stock_time):
    time_result=[]
    price_result=[]
    pivot=1
    
    driver=webdriver.Chrome("chromedriver.exe", options=options)
    url='https://finance.naver.com/item/sise_time.nhn?code='+code+'&thistime='+str(stock_date)+str('stock_time')
    driver.get(url)
    
    while True:
        if pivot==1:
            page=pivot
        elif(pivot<=10):
            page=pivot+1
        else:
            if(pivot%10==0):
                page=12
            else:
                page=(pivot%10)+2
            
        html = driver.page_source
        soup=bs(html,'lxml')

        time_css_selector="body > table.type2 > tbody > tr > td:nth-of-type(1) > span"
        now_time=soup.select(time_css_selector)
        for i in now_time:
            time_result.append(i.text)
    
        price_css_selector="body > table.type2 > tbody > tr > td:nth-of-type(2) > span"
        price=soup.select(price_css_selector)
        for j in price:
            price_result.append(j.text)
        
        nextpg_css_selector=f"body > table.Nnavi > tbody > tr > td:nth-child({page+1}) > a"    
        try:
            nextpg_element=driver.find_element_by_css_selector(nextpg_css_selector)
            nextpg_element.click()
        except NoSuchElementException:
            print("마지막 페이지")
            break
        pivot+=1

    concating(code, time_result,price_result,stock_time)
    driver.quit()


def concating(code, time_result, price_result, stock_time):
    date_result=stock_date
    concat_data={'date':date_result,
                 'time':time_result,
                'price':price_result}
    scraping_df=pd.DataFrame(concat_data)
    scraping_df.to_csv('./stock_crwaling_'+code+'_'+str(date_result)+'.csv',mode='w',encoding='utf-8-sig',header=True,index=True)


if __name__ =='__main__':
    code=input("기업 코드를 입력해주세요.: ")
    stock_date=int(input("날짜를 입력해주세요.(예시: 20210207): "))
    stock_time=int(input("시간을 입력해주세요.(예시: 161059): "))
    stock_scraping(code,stock_date,stock_time)
    print("완료")