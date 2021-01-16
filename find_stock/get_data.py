import stock_evaluation_table as st
import requests
import json

url = "http://localhost:8000/items"

data = {"return_datas":st.get_data(['삼성전자'])}

res = requests.post(url,json=data)

print(res.text)


