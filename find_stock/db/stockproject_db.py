from sqlalchemy import create_engine

def connect_database():
    #데이터 베이스 연결 설정
    sqlalchemy_database_url = 'mysql+pymysql://root:qwer1234@localhost:3306/stockproject'
    engine = create_engine(sqlalchemy_database_url,echo=False)

    return engine