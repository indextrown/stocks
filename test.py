import requests
import bs4

from bs4 import BeautifulSoup

 

res = requests.get("https://finance.naver.com/item/sise_day.nhn?code=005930&page=1")

res1 = requests.get("https://finance.naver.com/item/main.nhn?code=005930")

soup = BeautifulSoup(res.text, 'lxml')
soup1 = BeautifulSoup(res1.text, 'lxml')





my_headers = {
    "referer": "https://finance.naver.com/item/sise_day.nhn?code=005930&page=1", 
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}



res = requests.get(
    url = "https://finance.naver.com/item/sise_day.nhn?code=005930&page=1",
    headers = my_headers
)




total_data_list = []
for page_number in range(1, 2):
    url = "https://finance.naver.com/item/sise_day.nhn?code=005930&page={}".format(page_number)
    res = requests.get(url=url, headers = my_headers)
    soup = bs4.BeautifulSoup(res.text)
    
soup.select("table.type2 > tr[onmouseover='mouseOver(this)'] > td[align='center']")
twoStep = soup.select("table.type2 > tr[onmouseover='mouseOver(this)']")[0:]


날짜 = []
종가 = []
전일비 = []
거래량 = []

시가총액 = soup1.select("em#_market_sum")[0].text.replace('\t' , '').strip().replace('\n' , '')
for i in twoStep:
    날짜.append(i.select('td[align="center"] > span')[0].text)
    종가.append(int(i.select('td.num > span')[0].text.replace(',', '')))
    전일비.append(int(i.select('td.num > span.tah.p11')[1].text.strip().replace(',', '')))
    거래량.append(int(i.select('td.num > span')[5].text.replace(',', '')))

l = []

for i in range(len(날짜)):
    l.append({
        '날짜':날짜[i],
        '종가':종가[i],
        '전일비':전일비[i],
        '거래량':거래량[i],

    })
    
##파일을 쓴다
import csv
import json

with open('data.js', "w", encoding="UTF-8-sig") as f_write:
    json.dump(l, f_write, ensure_ascii=False, indent=4)
##파일을 다시 읽는다
data = ""
with open('data.js', "r", encoding="UTF-8-sig") as f:
    line = f.readline()
    while line:
        data += line
        line = f.readline()
#파일에 변수명을 추가하여 다시 쓴다.
final_data = f"var data = {data};"
final_data = f"var 시가총액 = '{시가총액}';\n\" + final_data
with open('data.js', "w", encoding="UTF-8-sig") as f_write:
    f_write.write(final_data) 
