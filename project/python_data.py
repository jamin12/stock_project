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
#주식 뉴스 가져오기
def stock_news(stock_name,stock_ailgn):
    #TODO : 정렬 기준 : 0 관련도순, 1 최신순
    url = f"https://search.naver.com/search.naver?where=news&query={stock_name}&sm=tab_srt&sort={stock_ailgn}&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=0&refresh_start=0&related=0"
    soup = into_request(url)
    #전체 뉴스 목록 가져오기
    all_news = soup.find("div", attrs = {"class" : "group_news"})
    pick_news = all_news.find("ul", attrs = {"class":"list_news"})
    #뉴스 고르기
    picks = pick_news.find_all("li",attrs = {"id": re.compile(r"sp_nws\d?")})
    news_title = []
    news_content = []
    # image_res = []
    news_link = []
    for idx,pick in enumerate(picks):
        #뉴스 타이틀
        news_title.append(pick.find("a",attrs = {"class" : "news_tit"}).get_text())
        #뉴스 내용  
        news_content.append(pick.find("a",attrs = {"class" : "api_txt_lines dsc_txt_wrap"}).get_text())
        #이미지 가져오기
    #     news_image = pick.find("img")["src"]
    #     if news_image.startswith("//"):
    #         news_image = "https:" + news_image
    # #TODO 16진수 이미지 파일 읽기
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
    



if __name__ == "__main__":
    stock_news("삼성전자",0)
    # a.securities_information()
    
    
    
