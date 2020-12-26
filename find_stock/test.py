import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
from openpyxl import load_workbook

#selenium으로 접속하는 방법
def into_selenium(url):
    #브라우져 옵션 설정
    options = Options()
    #화면 안뜨게
    # options.headless = True
    #유저 에이전트 설정
    #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    broswer = webdriver.Chrome(options = options)
    # broswer.maximize_window()
    #브라우저 연결
    broswer.get(url)
    return broswer

if __name__ == '__main__':
    #엑셀파일에서 종목 코드 찾기
    wb = load_workbook("./find_stock/stock_codenum.xlsm",data_only = True)
    ws = wb.active
    stock_code = ""
    for stocknum in ws.iter_rows(min_row=1):
        if "세미콘라이트" == stocknum[0].value:
            stock_code = str(stocknum[4].value)
            break
    
    print(stock_code)



