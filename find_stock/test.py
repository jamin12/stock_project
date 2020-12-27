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
    options.headless = True
    #유저 에이전트 설정
    #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    broswer = webdriver.Chrome("./find_stock/chromedriver.exe",options = options)
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
        if "삼성전자" == stocknum[0].value:
            stock_code = str(stocknum[4].value)
            break
    
    broswer = into_selenium(f"https://navercomp.wisereport.co.kr/v2/company/c1030001.aspx?cmp_cd={stock_code}&cn=")
    #손익 계산서
    broswer.find_element_by_id("rpt_tab1").click()
    #매출액,매출 총이익, 영업이익, 당기순이익
    total_sales = []
    profit_sales = []
    operating_profit = []
    net_profit = []
    for i in range(2,7):
        total_sales.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text)
        profit_sales.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[26]/td[{i}]').text)
        operating_profit.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[58]/td[{i}]').text)
        net_profit.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[218]/td[{i}]').text)

    #재무 상태표
    broswer.find_element_by_id("rpt_tab2").click()
    time.sleep(0.5)
    #자산 총계, 유동 자산, 현금 및 현금성 자산, 총 부채, 유동 부채,이익 잉여금
    total_assets = []
    liquid_assets = []
    cash_assets = []
    total_debt = []
    current_liabilities = []
    surplus_profit = []
    for i in range(2,7):
        total_assets.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text)
        liquid_assets.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[2]/td[{i}]').text)
        cash_assets.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[47]/td[{i}]').text)
        total_debt.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[127]/td[{i}]').text)
        current_liabilities.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[127]/td[{i}]').text)
        surplus_profit.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[243]/td[{i}]').text)

    #현금 흐름표
    broswer.find_element_by_id("rpt_tab3").click()
    time.sleep(0.5)
    #영업활동으로 인한 현금흐름, 투자활동으로 인한 현금 흐름, 재무활동으로 인한 현금 흐름
    business_activities = []
    investment_activities = []
    financial_activities = []
    for i in range(2,7):
        business_activities.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text)
        investment_activities.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[144]/td[{i}]').text)
        financial_activities.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[242]/td[{i}]').text)

    broswer.get(f"https://navercomp.wisereport.co.kr/v2/company/c1040001.aspx?cmp_cd={stock_code}&cn=")
    #EPS, PER, EV_EBITDA, PSR, PBR, INDUSTRIES_AVG_PER
    EPS = []
    PER = []
    EV_EBITDA = []
    PSR = []
    PBR = []
    industries_avg = broswer.find_element_by_xpath('/html/body/div/form/div[1]/div/div[2]/div[1]/div/table/tbody/tr[3]/td/dl/dt[4]/b').text
    for i in range(2,7):
        EPS.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[1]/td[{i}]').text)
        PER.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[17]/td[{i}]').text)
        EV_EBITDA.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[29]/td[{i}]').text)
        PSR.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[26]/td[{i}]').text)
        PBR.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[17]/td[{i}]').text)

    #수익성
    broswer.find_element_by_id("val_td1").click()
    time.sleep(0.5)
    #영업 이익률, 순이익률, ROE
    operating_profit_ratio = []
    net_profit_rate = []
    ROE = []
    for i in range(2,7):
        operating_profit_ratio.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[4]/td[{i}]').text)
        net_profit_rate.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[7]/td[{i}]').text)
        ROE.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[13]/td[{i}]').text)

    #안전성
    #부채비율, 유동부채 비율, 순 부채 비율, 유동 비율, 당좌비율
    broswer.find_element_by_id("val_td3").click()
    time.sleep(0.5)
    debt_ratio = []
    current_liability_ratio = []
    net_debt_ratio = []
    current_rate = []
    current_account_ratio = []
    for i in range(2,7):
        debt_ratio.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text)
        current_liability_ratio.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[4]/td[{i}]').text)
        net_debt_ratio.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[10]/td[{i}]').text)
        current_rate.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[13]/td[{i}]').text)
        current_account_ratio.append(broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[16]/td[{i}]').text)
    
    
    #평가기준
    for i in range(4):
        #매출액이 매년 상승 했는지
        if total_sales[i] < total_sales[i+1]:
            pass




