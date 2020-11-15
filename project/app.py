from flask import Flask, render_template, request
import python_data

#플라스크 서버 인스턴스
app = Flask(__name__)

#/페이지 연결
@app.route('/')
def get_news():
    # 정보 가져와서 뿌리기
    stock_news = python_data.stock_info('삼성전자',0)
    news_info = stock_news.stock_news()
    news_title = next(news_info)
    news_contant = next(news_info)
    news_link = next(news_info)
    news = [news_title,news_contant,news_link]

    return render_template('index.html',news = news)


if __name__ == "__main__":
    app.run(debug=True)
