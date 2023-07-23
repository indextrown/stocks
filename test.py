import requests
from bs4 import BeautifulSoup
import json

url = "https://finance.naver.com/item/sise_day.nhn?code=005930&page=1"
referer_url = "https://finance.naver.com/item/sise_day.nhn?code=005930&page=1"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"

my_headers = {
    "referer": referer_url,
    "upgrade-insecure-requests": "1",
    "user-agent": user_agent
}

# 페이지 내용을 가져온다
res = requests.get(url, headers=my_headers)
soup = BeautifulSoup(res.text, 'lxml')

# 종목 정보 페이지 내용을 가져온다
info_url = "https://finance.naver.com/item/main.nhn?code=005930"
res_info = requests.get(info_url, headers=my_headers)
soup_info = BeautifulSoup(res_info.text, 'lxml')

# 시가총액 가져오기
시가총액 = soup_info.select("em#_market_sum")[0].text.replace('\t', '').strip().replace('\n', '')

# 데이터 파싱
data_list = []
rows = soup.select("table.type2 > tr[onmouseover='mouseOver(this)']")[0:]
for row in rows:
    날짜 = row.select('td[align="center"] > span')[0].text
    종가 = int(row.select('td.num > span')[0].text.replace(',', ''))
    전일비 = int(row.select('td.num > span.tah.p11')[1].text.strip().replace(',', ''))
    거래량 = int(row.select('td.num > span')[5].text.replace(',', ''))

    data = {
        '날짜': 날짜,
        '종가': 종가,
        '전일비': 전일비,
        '거래량': 거래량
    }
    data_list.append(data)

# 데이터를 역순으로 정렬
data_list.reverse()

# 데이터를 JSON 파일로 저장
file_name = 'data.js'
with open(file_name, "w", encoding="UTF-8-sig") as f_write:
    json.dump(data_list, f_write, ensure_ascii=False, indent=4)

# JSON 파일에 변수명을 추가하여 다시 쓴다
with open(file_name, "r", encoding="UTF-8-sig") as f:
    file_data = f.read()
final_data = f"var 시가총액 = '{시가총액}';\nvar data = {file_data}"
with open(file_name, "w", encoding="UTF-8-sig") as f_write:
    f_write.write(final_data)
