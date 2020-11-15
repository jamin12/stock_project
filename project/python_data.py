import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image as pilimg

#requests로 접속하는 방법
def into_request(url):
    #유저 에이전트
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.107.16 Safari/537.36"}
    # 사이트 url에 접속 후 Beautifulsoup 객체에 lxml로 저장
    res = requests.get(url,headers = headers)
    res.raise_for_status() # 위에 코드가 이상이 있을 경우 아래 코드 실행 안됨
    soup = BeautifulSoup(res.text,"lxml")
    return soup

#selenium으로 접속하는 방법
def into_selenium(url):
    #브라우져 옵션 설정
    options = webdriver.ChromeOptions()
    #화면 안뜨게
    options.headless = True
    #유저 에이전트 설정
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.107.16 Safari/537.36")
    #화면 사이즈 설정
    options.add_argument("window-size=1920x1080")
    broswer = webdriver.Chrome(options = options)
    broswer.maximize_window()
    #브라우저 연결
    broswer.get(url)
    soup = BeautifulSoup(broswer.page_source,"lxml")
    return soup


#TODO : 다음 프로젝트 증권사 API활용하기
#주식 정보
class stock_info:
    def __init__(self,stock_name : str,stock_ailgn : int) -> list:
        self.stock_name = stock_name
        self.stock_ailgn = stock_ailgn

    #주식 뉴스 가져오기
    def stock_news(self):
        #TODO : 정렬 기준 : 0 관련도순, 1 최신순
        url = f"https://search.naver.com/search.naver?where=news&query={self.stock_name}&sm=tab_srt&sort={self.stock_ailgn}&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=0&refresh_start=0&related=0"
        soup = into_request(url)
        #전체 뉴스 목록 가져오기
        all_news = soup.find("div", attrs = {"class" : "group_news"})
        pick_news = all_news.find("ul", attrs = {"class":"list_news"})
        #뉴스 고르기
        picks = pick_news.find_all("li",attrs = {"id": re.compile(r"sp_nws\d?")})
        news_title = []
        news_content = []
        news_link = []
        # image_res = []
        for idx,pick in enumerate(picks):
            #뉴스 타이틀
            news_title.append(pick.find("a",attrs = {"class" : "news_tit"}).get_text())
            #뉴스 내용  
            news_content.append(pick.find("a",attrs = {"class" : "api_txt_lines dsc_txt_wrap"}).get_text())
            #이미지 가져오기
        #     news_image = pick.find("img")["src"]
        #     if news_image.startswith("//"):
        #         news_image = "https:" + news_image
        #TODO 16진수 이미지 파일 읽기
        #     image_res.append(requests.get(news_image))
        #     image_res[idx].raise_for_status()
        #뉴스 링크
            news_link.append(pick.find("a")["href"])
        # 뉴스 타이틀 반환
        yield news_title
        # 뉴스 내용 반환
        yield news_content
        # 뉴스 이미지 반환
        # yield image_res
        #뉴스 링크 반환
        yield news_link

    #주식 정보 가저오기
    def securities_information(self):
        #TODO: 주식 코드 가져오기
        stock_code = {"삼성전자" : "005930"}
        url = f"https://finance.naver.com/item/main.nhn?code={stock_code[self.stock_name]}"
        soup = into_request(url)
        
        '''
        웹에서 정보 가져오기
        '''
        #전체적인 주식 정보 가져오기
        web_securities_information = soup.find("div", attrs = {"class" : "rate_info"})
        #기본적인 정보(현재 금액 , 등락률 가져오기)
        web_basic_information = web_securities_information.find("div", attrs = {"class" : "today"})
        #현재 가격 가져오기
        web_current_costs = web_basic_information.find("p", attrs = {"class" : "no_today"})
        #전일 대비 등락률 저장
        web_compare_yesterday = web_basic_information.find("p", attrs = {"class" : "no_exday"})
        #전일 대비 가격
        web_updown_costs = web_compare_yesterday.find_all("em")[0]
        #전일 대비 등락률
        web_updown_rate = web_compare_yesterday.find_all("em")[1]
        #주식 세부 정보(전일 가격, 고가 , 저가 등)
        web_major_information = web_securities_information.find("table")
        #전일 가격 가져오기
        web_yesterday_costs = web_major_information.find_all("tr")[0].find_all("em")[0]
        #고가 정보
        web_high_costs = web_major_information.find_all("tr")[0].find_all("em")[1]
        #시가 정보
        web_start_costs = web_major_information.find_all("tr")[1].find_all("em")[0]
        #저가
        web_low_costs = web_major_information.find_all("tr")[1].find_all("em")[1]
        #차트 이미지
        web_img_chart = soup.find("img",attrs = {"id" : "img_chart_area"})["src"]
        if web_img_chart.startswith("//"):
            web_img_chart = "https:" + web_img_chart
        
        '''
        웹에서 가져온 정보 저장
        '''
        # 현재 가격 : 두번씩 나오는 버그가 있어 반 자름
        current_costs = web_current_costs.get_text().strip()
        current_costs = current_costs[len(current_costs)//2:].strip()
        #전일대비 가격
        updown_costs = re.sub("[^a-z0-9]",'',web_updown_costs.get_text().strip())
        updown_costs = updown_costs[len(updown_costs)//2:]
        #등락률
        updown_rate = re.sub("[^a-z0-9]",'',web_updown_rate.get_text().strip())
        updown_rate = updown_rate[len(updown_rate)//2:]
        #전일 가격 
        yesterday_costs = web_yesterday_costs.get_text().strip()
        yesterday_costs = yesterday_costs[len(yesterday_costs)//2:].strip()
        #고가
        high_costs = web_high_costs.get_text().strip()
        high_costs = high_costs[len(high_costs)//2:].strip()
        #시가
        start_costs = web_start_costs.get_text().strip()
        start_costs = start_costs[len(start_costs)//2:].strip()
        #저가
        low_costs = web_low_costs.get_text().strip()
        low_costs = low_costs[len(low_costs)//2:].strip()
        #이미지
        image_res = requests.get(web_img_chart)
        image_res.raise_for_status()
        
        # 정보 반환
        yield current_costs
        yield updown_costs
        yield updown_rate
        yield yesterday_costs
        yield high_costs
        yield low_costs



if __name__ == "__main__":
    a = stock_info("삼성전자",0)
    b = a.stock_news()
    c = next(b)
    d = next(b)
    f = next(b)
    for i in f:
        print(i)
        break
    
    # a.securities_information()
    
    
    
