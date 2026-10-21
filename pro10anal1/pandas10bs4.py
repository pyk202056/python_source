# BeautifulSoup 객체를 이용한 문서(html, xml) 처리
import requests  
from bs4 import BeautifulSoup

baseurl = "https://www.naver.com/"
headers = {"User-Agent":"Mozilla/5.0"}

source = requests.get(baseurl, headers=headers)
print(source, type(source))  # <class 'requests.models.Response'>
print(source.status_code)    # 200
# print(source.text, type(source.text))   # <class 'str'>
# print(source.content)

conv_data = BeautifulSoup(source.text, 'html.parser')
# print(conv_data, type(conv_data))  # <class 'bs4.BeautifulSoup'>

for atag in conv_data.find_all("a"):
    href = atag.get("href")
    title = atag.get_text(strip=True)
    if title:
        print(href)
        print(title)
        print('---')
