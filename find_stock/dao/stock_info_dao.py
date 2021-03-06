import sys
import os
# 상위 경로에 있는 파일 가져오기
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sqlalchemy.orm import sessionmaker
from db.stockproject_db import connect_database
from DTO.stock_info_vo import StockInfo
from DTO.user_vo import user

# 테이블을 조종할수 있는 세션 생성
Session = sessionmaker(bind=connect_database())
session = Session()

def stock_find_name(stock_name_list = []):
    code = []
    for i in session.query(StockInfo).filter(StockInfo.stock_name.in_(stock_name_list)).all():
        code.append((i.stock_name,i.stock_code,i.stock_type))

    return code


def create_user(user_name : str):
    session.add(user(user_name))
    session.commit()


if __name__ == "__main__":
    print(stock_find_name(["삼성전자","KCC건설","심텍","kcc","유니퀘스트"]))
