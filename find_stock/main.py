from fastapi import FastAPI
from pydantic import BaseModel
import stock_evaluation_table as st
import requests
import json
app = FastAPI()

class Item(BaseModel):
    return_datas : list


@app.post('/items/')
async def read_root(item:Item):
    return {"item_list":item}


def request(stock_name:list):
    url = "http://localhost:8000/items"
    data = {"return_datas":st.get_data(stock_name)}
    requests.post(url,json=data)

if __name__ == "__main__":
    request(['삼성전자'])
