import pandas_datareader.data as web
from datetime import datetime

'''
StockScraping.py
pandas-datareader사용, 최근 5년의 주가데이터를 일단위로 불러온다.
pandas-datareader를 사용하는 이유? = 야후 사이트만이 수정종가를 제공하기 때문

'''
if __name__ == '__main__':
    code={} # 코드 딕셔너리를 불러와 Datareader 인수로 전달한다.
    code=code_dict(code)


    for stock_code, stock_name in code.items():
        stock_data=web.DataReader(stock_code,'yahoo')
        stock_data['기업명']=stock_name
        stock_data.to_csv(stock_name+'_alltime_주가데이터.csv',encoding='utf-8-sig')

    print('작업완료')