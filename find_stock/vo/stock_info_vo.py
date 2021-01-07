from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String

Base = declarative_base()

class StockInfo(Base):
    __tablename__ = "stock_info"
    stock_name = Column(String(45),primary_key=True)
    stock_code = Column(String(45),primary_key=True)
    stock_type = Column(String(45))

    def __init__(self,stock_name,stock_code,stock_type):
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.stock_type = stock_type

    def __repr__(self):
        return "<stock_info('%s','%s','%s')>" %(self.stock_name,self.stock_code,self.stock_type)