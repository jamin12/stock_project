from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String

Base = declarative_base()
class user(Base):
    __tablename__ = "user"
    user_name = Column(String(45),primary_key=True)

    def __init__(self,user_name):
        self.user_name = user_name

    def __repr__(self):
        return "<user(%s)>"%(self.user_name)
    