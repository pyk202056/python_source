import pandas as pd
from bs4 import BeautifulSoup
import requests
# pip install playwright
# playwright install chromium

print('\n\n네이버 증권 자료 읽기 --- ')
url = 'https://stock.naver.com/market/stock/kr/stocklist/capitalization'
headers = {'User-Agent':'Mozilla/5.0'}
stock = requests.get(url=url, headers=headers)
# print(stock.text[:1000])

soup = BeautifulSoup(stock.text, 'html.parser')
print(soup.text)
# 종목명, 현재가, 전일대비, 거래량, 거래대금, 고가, 저가, 시가총액

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = 'https://stock.naver.com/market/stock/kr'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # False면 브라우저 창이 실제로 뜸
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state('networkidle')       # 데이터 요청이 다 끝날 때까지 대기
    html = page.content()                         # 완성된 HTML
    browser.close()

soup = BeautifulSoup(html, 'html.parser')
# print(soup.get_text()[2000:8000])

# 이름 추출, 리스트 만들기
name = soup.select('div.stock-name-container span.SingleLineText_text__HI_cb')
name_list = []
for i in range(len(name)):
    imsi = name[i].get_text(strip=True)
    name_list.append(imsi)

# print(name_list)

# table명으로 필요한 자료 가져오기 / tr태그를 이용해서 행별로 분리
table = soup.find_all('tbody', class_='Table_tbody__EJrOg')
row = table[0].select('tr')

# tr태그를 따라 행 별로 분리한 후 'row[i].select('span.SingleLinePrice_price__g_6VV'를 이용해서 필요한 정보만 가져오기. 아직까진 숫자와 문자가 혼재해있음
# 숫자만 남겨서 리스트에 담기
lists = []
for i in range(10):
    print(row[i].get_text(strip=True))
    no = [int(tag.text.strip().replace(',','')) for tag in row[i].select('span.SingleLinePrice_price__g_6VV')]
    lists.append(no)

# print(lists)

# 리스트를 데이터 프레임으로 만들기
df = pd.DataFrame(lists, columns=['현재가', '거래량', '거래대금', '고가', '저가'], index=name_list)
print(df)


# cur_price = [int(tag.text.strip().replace(',','')) for tag in soup.select('td.Table_align-right__a9V79.Table_sticky-column__V8d8X.Table_has-row-divider__Q4BWX span.SingleLinePrice_price__g_6VV')]
# vol = soup.select('span.SingleLinePrice_single-line-price__bnpQv.SingleLinePrice_medium__QoN_F span.SingleLinePrice_price__g_6VV')
# df = pd.DataFrame({'종목명':name, '현재가':cur_price})
