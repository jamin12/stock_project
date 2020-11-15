from flask import Flask, render_template, request
import python_data

#플라스크 서버 인스턴스
app = Flask(__name__)

@app.route('/')
def get_news():
    stock_news = python_data.stock_info('삼성전자',0)
    news_info = stock_news.stock_news()
    news_title = next(news_info)
    news_contant = next(news_info)

    return render_template('index.html',news_title = news_title)


if __name__ == "__main__":
    app.run(debug=True)
    
