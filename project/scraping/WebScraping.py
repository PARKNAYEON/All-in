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
WebScraping.py
네이버 종목 토론방에서 작성일자/제목(댓글 수도 제목에 포함)/조회수/추천수/비추천수를 수접함

def web_scraping(code, start_page,end_page, count) : 종목토론방 긁어오는 함수
def concating(code, title_result,date_result,views_result,like_result,dislike_result,count) : 긁어온 데이터를 합치는 함수

'''

# 디렉토리 재설정
try:
    os.chdir("C:\\Users\\SAMSUNG\\Desktop\\") # Chromewebdriver가 있는 경로로 설정 
    print("Directory changed")
except OSError: # 예외처리
    print("Can't change the Current Working Directory")
In [ ]:
def mkdir_data(directory): # 하위 디렉토리 생성
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Directory created")
    except OSError:
        print('Error: Creating directory.')


def web_scraping(code, start_page,end_page, count): 
    title_result=[]
    date_result=[]
    like_result=[]
    dislike_result=[]
    views_result=[]

    driver=webdriver.Chrome("chromedriver.exe", options=options)
    url="https://finance.naver.com/item/board.nhn?code="+code+"&page="+str(start_page)
    driver.get(url)
    while (start_page<=end_page):
        if (start_page==1): # 첫 페이지
            page=start_page
        elif (start_page<=10): # 2~10 페이지, 밑의 페이지 bar 구성이 다름
            page=start_page+1
        else:
            if (start_page%10==0): # view의 마지막 페이지인 경우
                page=12
            else:
                page=start_page%10+2
        html = driver.page_source
        soup=bs(html,'lxml') # selenium의 각 화면에서 bs4를 이용하여 긁어옴
        
        # 각 요소를 끌어오는 부분
        title_css_selector="#content > div.section.inner_sub > table.type2 > tbody > tr > td.title > a"
        title=soup.select(title_css_selector)
        for i in title: 
            title_result.append(i.text.replace('\t','').replace('\n',''))
    
        date_css_selector="#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(1) > span"
        date=soup.select(date_css_selector)
        for j in date:
            date_result.append(j.text)
    
        views_css_selector="#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(4) > span"
        views=soup.select(views_css_selector)
        for k in views:
            views_result.append(k.text)
    

        like_css_selector="#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(5) > strong"
        like=soup.select(like_css_selector)
        for l in like:
            like_result.append(l.text)
    
        dislike_css_selector="#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(6) > strong"
        dislike=soup.select(dislike_css_selector)
        for m in dislike:
            dislike_result.append(m.text)
        
        # 자동으로 다음 새 10개 페이지로 이동하는 부분
        nextpg_css_selector=f"#content > div.section.inner_sub > table:nth-child(3) > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child({page+1}) > a"
        nextpg_element=driver.find_element_by_css_selector(nextpg_css_selector)
        nextpg_element.click()
        start_page+=1
    # 모인 요소들을 합치는 부분
    concating(code+'.KS', title_result,date_result,views_result,like_result,dislike_result,count)
    driver.quit()


def concating(code, title_result,date_result,views_result,like_result,dislike_result,count): # 긁어온 데이터를 합치는 함수
    concat_data={'title':title_result,
                'date':date_result,
                'views':views_result,
                'like':like_result,
                'dislike':dislike_result}
    scraping_df=pd.DataFrame(concat_data)
    scraping_df['Code']=code
    scraping_df.to_csv('./title_scraping_'+code+'_'+str(count)+'.csv',mode='w',encoding='utf-8-sig',header=True,index=True)


if __name__ == '__main__':
    code=input("기업 코드를 입력해주세요.: ")
    start_page=int(input("첫 번째 페이지를 입력해주세요.: "))
    end_page=int(input("마지막 페이지를 입력해주세요.: "))
    mkdir_data(code+'_data') # 디렉토리 생성
    count=1
    while (start_page<=end_page):
        if (end_page-start_page<100): # (1)
            web_scraping(code,start_page,end_page,count)
        else:
            web_scraping(code,start_page,start_page+100,count) # (2)
        print("%d번째 스크래핑이 끝났습니다."%count)
        start_page+=101 # (3), (1)~(3)의 숫자는 임의 조정 가능. 
        count+=1