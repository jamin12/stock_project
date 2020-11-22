from flask import Flask, render_template, request
import python_data

#플라스크 서버 인스턴스
app = Flask(__name__)

save_name = '삼성전자'

#index페이지 설정
@app.route('/')
def index():
    return render_template("index.html")



#/my_news페이지 연결
@app.route('/my_news')
def get_news():
    global save_name
    #Default값 설정
    if request.args.get("align-keyword"):
        #정렬 기준
        align_crite = int(request.args.get("align-keyword"))
    else:
        align_crite = 0
    
    if request.args.get("search-company"):
        company_name = request.args.get("search-company")
        save_name = company_name
    else:
        company_name = save_name

    # 정보 가져와서 뿌리기
    stock_news = python_data.stock_news(company_name,align_crite)
    news_title = next(stock_news)
    news_contant = next(stock_news)
    news_link = next(stock_news)
    news = [news_title,news_contant,news_link]

    return render_template('news.html',news = news,align_crite = align_crite)


if __name__ == "__main__":
    app.run(debug=True)
