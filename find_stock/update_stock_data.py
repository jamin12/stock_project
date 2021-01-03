import requests
from bs4 import BeautifulSoup
import re
import sqlalchemy as db

#requests로 접속하는 방법
def into_request(url):
    #유저 에이전트
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    # 사이트 url에 접속 후 Beautifulsoup 객체에 lxml로 저장
    res = requests.get(url,headers = headers)
    res.raise_for_status() # 위에 코드가 이상이 있을 경우 아래 코드 실행 안됨
    soup = BeautifulSoup(res.text,"lxml")
    return soup

def update_stock_database():
    #데이터 베이스 연결 설정
    sqlalchemy_database_url = 'mysql+pymysql://root:1234@localhost:3306/stockproject'
    engine = db.create_engine(sqlalchemy_database_url,echo=False)
    connection = engine.connect()

    # 데이터 베이스 테이블 결정
    metadata = db.MetaData()
    table = db.Table('stock_info',metadata,autoload=True,autoload_with=engine)
    url = ""
    stock_type = ''
    for i in range(2):
        page = 1
        url = f"https://finance.naver.com/sise/sise_market_sum.nhn?sosok={i}&page="
        # 0 : 코스피 , 1 코스닥
        while True:
            soup = into_request(url+str(page))
            #주식 전체 테이블
            stock_table = soup.find("table",attrs = {'class':'type_2'}).find('tbody')
            if not stock_table:
                break
            stock_lines = stock_table.find_all("tr")
            try:
                stock_lines[1]
            except:
                break
            for idx,stock_line in enumerate(stock_lines):
                try:
                    #기업 이름
                    stock_name = stock_line.find_all('td')[1].text
                    #기업 코드
                    stock_code = re.findall("\d+",stock_line.find_all('td')[1].find('a')["href"])
                except:
                    continue
                #코스피 코스닥 설정
                if i == 0:
                    stock_type = "KOSPI"
                else:
                    stock_type = "KOSDAQ"
                try:
                    query = db.insert(table).values({'stock_name':stock_name,'stock_code':stock_code[0],'stock_type':stock_type})
                    result_proxy = connection.execute(query)
                    result_proxy.close()
                except:
                    continue
            page = page + 1
