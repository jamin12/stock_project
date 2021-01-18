from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from dao import stock_info_dao


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

def get_data(mylist = []):
    result_set = stock_info_dao.stock_find_name(mylist)
    print(result_set)
    return_datas = []
    return_data = {}
    for stock_info in result_set:
        try:
            broswer = into_selenium(f"https://navercomp.wisereport.co.kr/v2/company/c1030001.aspx?cmp_cd={stock_info[1]}&cn=")
            #손익 계산서
            broswer.find_element_by_id("rpt_tab1").click()
            #매출액,매출 총이익, 영업이익, 당기순이익
            total_sales = []
            profit_sales = []
            operating_profit = []
            net_profit = []
            for i in range(2,7):
                total_sales.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text).replace(',',''))
                profit_sales.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[26]/td[{i}]').text).replace(',',''))
                operating_profit.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[58]/td[{i}]').text).replace(',',''))
                net_profit.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[218]/td[{i}]').text).replace(',',''))
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
                total_assets.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text).replace(',',''))
                liquid_assets.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[2]/td[{i}]').text).replace(',',''))
                cash_assets.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[47]/td[{i}]').text).replace(',',''))
                total_debt.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[127]/td[{i}]').text).replace(',',''))
                current_liabilities.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[127]/td[{i}]').text).replace(',',''))
                surplus_profit.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[243]/td[{i}]').text).replace(',',''))
            #현금 흐름표
            broswer.find_element_by_id("rpt_tab3").click()
            time.sleep(0.5)
            #영업활동으로 인한 현금흐름, 투자활동으로 인한 현금 흐름, 재무활동으로 인한 현금 흐름
            business_activities = []
            investment_activities = []
            financial_activities = []
            for i in range(2,7):
                business_activities.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text).replace(',',''))
                investment_activities.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[144]/td[{i}]').text).replace(',',''))
                financial_activities.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[242]/td[{i}]').text).replace(',',''))
            broswer.get(f"https://navercomp.wisereport.co.kr/v2/company/c1040001.aspx?cmp_cd={stock_info[1]}&cn=")
            #EPS, PER, EV_EBITDA, PSR, PBR, INDUSTRIES_AVG_PER
            EPS = []
            PER = []
            EV_EBITDA = []
            PSR = []
            PBR = []
            INDUSTRIES_AVG_PER = (broswer.find_element_by_xpath('/html/body/div/form/div[1]/div/div[2]/div[1]/div/table/tbody/tr[3]/td/dl/dt[4]/b').text).replace(',','')
            for i in range(2,7):
                EPS.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[1]/td[{i}]').text).replace(',',''))
                PER.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[17]/td[{i}]').text).replace(',',''))
                EV_EBITDA.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[29]/td[{i}]').text).replace(',',''))
                PSR.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[26]/td[{i}]').text).replace(',',''))
                PBR.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[9]/table[2]/tbody/tr[17]/td[{i}]').text).replace(',',''))
            #수익성
            broswer.find_element_by_id("val_td1").click()
            time.sleep(0.5)
            #영업 이익률, 순이익률, ROE
            operating_profit_ratio = []
            net_profit_rate = []
            ROE = []
            for i in range(2,7):
                operating_profit_ratio.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[4]/td[{i}]').text).replace(',',''))
                net_profit_rate.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[7]/td[{i}]').text).replace(',',''))
                ROE.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[13]/td[{i}]').text).replace(',',''))
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
                debt_ratio.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text).replace(',',''))
                current_liability_ratio.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[4]/td[{i}]').text).replace(',',''))
                net_debt_ratio.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[10]/td[{i}]').text).replace(',',''))
                current_rate.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[13]/td[{i}]').text).replace(',',''))
                current_account_ratio.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[16]/td[{i}]').text).replace(',',''))
            #성장성
            #매출액 증가율, 영업 이익 증가율, 순이익 증가율
            broswer.find_element_by_id("val_td2").click()
            time.sleep(0.5)
            sales_growth_rate = []
            operating_profit_growth_rate = []
            net_profit_growth_rate = []
            for i in range(2,7):
                sales_growth_rate.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[1]/td[{i}]').text).replace(',',''))
                operating_profit_growth_rate.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[4]/td[{i}]').text).replace(',',''))
                net_profit_growth_rate.append((broswer.find_element_by_xpath(f'/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[7]/td[{i}]').text).replace(',',''))
            return_data = {
                #매출액,매출 총이익, 영업이익, 당기순이익
                "total_sales":total_sales,"profit_sales":profit_sales,"operating_profit":operating_profit,"net_profit":net_profit,
                #자산 총계, 유동 자산, 현금 및 현금성 자산, 총 부채, 유동 부채,이익 잉여금
                "total_assets":total_assets,"liquid_assets":liquid_assets,"cash_assets":cash_assets,"total_debt":total_debt,"current_liabilities":current_liabilities,"surplus_profit":surplus_profit,
                #영업활동으로 인한 현금흐름, 투자활동으로 인한 현금 흐름, 재무활동으로 인한 현금 흐름
                "business_activities":business_activities,"investment_activities":investment_activities,"financial_activities":financial_activities,
                #EPS, PER, EV_EBITDA, PSR, PBR, INDUSTRIES_AVG_PER
                "EPS":EPS,"PER":PER,"EV_EBITDA":EV_EBITDA,"PSR":PSR,"PBR":PBR,"INDUSTRIES_AVG_PER":INDUSTRIES_AVG_PER,
                #영업 이익률, 순이익률, ROE
                "operating_profit_ratio":operating_profit_ratio,"net_profit_rate":net_profit_rate,"ROE":ROE,
                #부채비율, 유동부채 비율, 순 부채 비율, 유동 비율, 당좌비율
                "debt_ratio":debt_ratio,"current_liability_ratio":current_liability_ratio,"net_debt_ratio":net_debt_ratio,"current_rate":current_rate,"current_account_ratio":current_account_ratio,
                #매출액 증가율, 영업 이익 증가율, 순이익 증가율
                "sales_growth_rate":sales_growth_rate,"operating_profit_growth_rate":operating_profit_growth_rate,"net_profit_growth_rate":net_profit_growth_rate,
                #stock_info
                "stock_info":stock_info
            }
            broswer.quit()
            return_datas.append(return_data)
        except:
            print("get_data_error")
            continue
    return return_datas

def calculation_score(stock_datas):
    for stock_data in stock_datas:
        #평가기준
        score = 0
        score_criteria2 = 0 # 몇년간 상승했는지 체크
        evaluation_value = []
        #순 부채 비율이 30%이하 인지
        try:
            if float(stock_data["net_debt_ratio"][-1]) < 30:
                score = score + 3
                evaluation_value.append("net_debt_ratio")
        except:
            print("net_debt_error")
            pass
        #투자활동 활동과 재무활동이 모두 + 인지
        try:
            for i in range(1,4):
                if float(stock_data["investment_activities"][i+1]) > 0 and float(stock_data["financial_activities"][i+1]) > 0:
                    score_criteria2 = score_criteria2 + 1
                if score_criteria2 >= 2:
                    score = score - 3
                    score_criteria2 = 0
                    evaluation_value.append("investment_activities")
        except:
            score_criteria2 = 0
            print("investment_activities_error")
            pass
        score_criteria2 = 0
        # EPS와 ROE가 꾸준히 오르는가
        try:
            for i in range(1,4):
                if float(stock_data["EPS"][i]) < float(stock_data["EPS"][i+1]) or float(stock_data["ROE"][i]) < float(stock_data["ROE"][i+1]):
                    score_criteria2 = score_criteria2 + 1
                if score_criteria2 > 2:
                    score = score + 3
                    score_criteria2 = 0
                    evaluation_value.append("EPS")
        except:
            score_criteria2 = 0
            print("EPS_error")
            pass
        score_criteria2 = 0
        # 유동비율 ,당좌비율이 100%가 넘고 
        try:
            for i in range(1,4):
                if (float(stock_data["current_liability_ratio"][i+1]) > 100 and float(stock_data["current_account_ratio"][i+1]) > 100):
                    score_criteria2 = score_criteria2 + 1
                if score_criteria2 > 2:
                    score = score + 3
                    score_criteria2 = 0
                    evaluation_value.append("current_liability_ratio")
        except:
            score_criteria2 = 0
            print("currnet_liablility_error")
            pass
        score_criteria2 = 0
        #부채비율이 200%인지
        try:
            if float(stock_data["debt_ratio"][-1]) < 200:
                score = score + 3
                score_criteria2 = 0
                evaluation_value.append("debt_ratio")
        except:
            print("debt_ratio_error")
            pass
        score_criteria2 = 0
        # 영업이익률이, 매출이익률,계속 오르는지
        try:
            for i in range(1,4):
                if (float(stock_data["sales_growth_rate"][i+1]) > 0 and float(stock_data["operating_profit_growth_rate"][i+1]) > 0):
                    score_criteria2 = score_criteria2 + 1
                if score_criteria2 > 2:
                    score = score + 3
                    score_criteria2 = 0
                    evaluation_value.append("sales_growth_rate")
        except:
            score_criteria2 = 0
            print("sales_growth_rate_error")
            pass
        score_criteria2 = 0
        #당기 수익률이 오르는지
        try:
            for i in range(1,4):
                if float(stock_data["net_profit_growth_rate"][i+1]) > 0:
                    score_criteria2 = score_criteria2 + 1
                if score_criteria2 > 2:
                    score = score + 3
                    score_criteria2 = 0
                    evaluation_value.append("net_profit_growth_rate")
        except:
            score_criteria2 = 0
            print("net_profit_growth_rate_error")
            pass
        score_criteria2 = 0
        # 동종업계 평균보다 PER이 낮은가
        try:
            if float(stock_data["PER"][-1]) < float(stock_data["INDUSTRIES_AVG_PER"]):
                score = score + 3
                evaluation_value.append("PER")
        except:
            print("PER_error")
            pass

        
        print(stock_data["stock_info"][0],":",round((score/21)*100,2),evaluation_value)


if __name__ == '__main__':
    # a = get_data(["씨아이에스","일진머티리얼즈","포스코케미칼","에코프로비엠","삼화콘덴서","삼진엘앤디","피엔티"])
    a = get_data(["알서포트","신테카바이오","코리아센터","데이타솔루션","아이즈비전","머큐리","오픈베이스","기가레인"])
    # print(a)
    calculation_score(a)
    # for i in range(1,4):
    #     print(i)







