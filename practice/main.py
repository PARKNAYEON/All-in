from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
import pandas as pd

_input = input(''' input page : ''')
user_input = quote_plus(_input)

url = f'https://finance.naver.com/item/board.nhn?code=005930&page={user_input}'
chromedriver = 'C:/Users/parkn/PycharmProjects/prac/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')  # 웹 브라우저를 띄우지 않는 headlss chrome 옵션 적용
options.add_argument('disable-gpu')  # GPU 사용 안함
options.add_argument('lang=ko_KR')  # 언어 설정
driver = webdriver.Chrome(chromedriver, options=options)

driver.get(url)

try:  # 정상 처리
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'title'))
    )  # 해당 태그 존재 여부를 확인하기까지 3초 정지
    title_list = []
    day_list = []
    #pageNum = int(driver.find_element_by_class_name('_totalCount').text)

    count = 0

    for i in range(1, 100):
        title_data = driver.find_elements_by_class_name('title')
        day_data = driver.find_elements_by_css_selector(f'#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(1) > span')
        for d in day_data:
            day_list.append(d.text.split('\n'))
        for k in title_data:
            title_list.append(k.text.split('\n'))
        print(title_data)
        driver.find_element_by_xpath("//td[@class='pgR']").click()
        time.sleep(2)  # 웹페이지를 불러오기 위해 2초 정지

except TimeoutException:  # 예외 처리
    print('해당 페이지에 정보가 존재하지 않습니다.')

finally:  # 정상, 예외 둘 중 하나여도 반드시 실행
    driver.quit()

# for i in range(len(title_list)):
#     title_list[i].append(title_list[i][1].split('~')[0])
#     title_list[i].append(title_list[i][1].split('~')[1])

title_df = pd.DataFrame({'날짜': day_list, '제목': title_list})
title_df.index = title_df.index + 1  # 인덱스 초기값 1로 변경
title_df.to_csv(f'samsung_prac_df.csv', mode='w', encoding='utf-8-sig',
                  header=True, index=True)

print('웹 크롤링이 완료되었습니다.')


