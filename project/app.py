from flask import Flask, render_template, request
import python_data

#플라스크 서버 인스턴스
app = Flask(__name__)

#/페이지 연결
@app.route('/')
def get_news():
    if request.args.get("align-keyword"):
        #정렬 기준
        align_crite = int(request.args.get("align-keyword"))
    else:
        align_crite = 0
    # 정보 가져와서 뿌리기
    stock_news = python_data.stock_info('삼성전자',align_crite)
    news_info = stock_news.stock_news()
    news_title = next(news_info)
    news_contant = next(news_info)
    news_link = next(news_info)
    news = [news_title,news_contant,news_link]

    return render_template('index.html',news = news,align_crite = align_crite)


if __name__ == "__main__":
    app.run(debug=True)
