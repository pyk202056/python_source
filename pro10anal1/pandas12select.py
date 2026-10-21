# css 셀렉터를 이용
from bs4 import BeautifulSoup

html_page = """
<html><body>
<div id="hello">
    <a href="https://www.naver.com">naver</a>
    <span>
        <a href="https://www.daum.net">daum</a>
    </span>
    <ul class="world">
        <li>안녕</li>
        <li>반가워</li>
    </ul>
</div>
<div id="hi" class="good">
    두번째 div
</div>
</body></html>
"""
soup = BeautifulSoup(html_page, "html.parser")
# aa = soup.select_one("div")     # 반환값 1개
# aa = soup.select_one("div#hello")
# aa = soup.select_one("div.good")
aa = soup.select_one("div#hello > a")  # div의 직계 a 태그 중 첫번째 요소 검색
print("aa : \n", aa, " ", aa.string)

print()
# bb = soup.select("div")   # 반환값이 복수
# bb = soup.select("div#hello > ul.world")  # 직계
# bb = soup.select("div#hello ul.world")    # 자손
bb = soup.select("div#hello ul.world > li") 
print("bb : \n", bb)   # [<div id="hello"> ... ]
print()
for i in bb:
    print(i, " ", i.text)

print("\n\n위키백과 사이트에서 이순신으로 검색된 자료 읽기 ---")
import requests

url = "https://ko.wikipedia.org/wiki/이순신"
headers = {"User-Agent":"Mozilla/5.0"}
wiki = requests.get(url=url, headers=headers)
# print(wiki.text[:300])
#mwIA
soup = BeautifulSoup(wiki.text, "html.parser")
result = soup.select("p#mwIA")
# print(result)
for s in result:
    for sup in s.find_all("sup"):
        sup.decompose()  # 태그 삭제

    print(s.get_text(strip=True, separator=" "))  # tag를 제외하고 텍스트만 추출(공백과 줄바꿈 제거)


print("\n\n교촌 치킨 사이트에서 메뉴, 가격 자료 읽기 ---")
import pandas as pd

url = "https://kyochon.com/menu/chicken.asp"
headers = {"User-Agent":"Mozilla/5.0"}
kyochon = requests.get(url=url, headers=headers)
# print(kyochon.text)

soup2 = BeautifulSoup(kyochon.text, "html.parser")
# 메뉴명 얻기
names = soup2.select("dl.txt > dt")
# print(names)
prices = [int(tag.text.strip().replace(",","")) 
            for tag in soup2.select("p.money strong")]
# print(prices)

df = pd.DataFrame({"상품명":names, "가격":prices})
print(df.head(3))
print(f"가격 평균 : {df["가격"].mean():.2f}")     # 20422.08
print(f"가격 표준편차 : {df["가격"].std():.2f}")  # 5074.23
# 변동계수(cv, 표준편차를 산술평균으로 나눈 값) : 상대적 변동성 파악
cv = df["가격"].std() / df["가격"].mean() * 100
print(f"가격 변동계수(cv) : {cv:.2f}%")  # 24.85%
# 가격 변동계수(상대적인 산포 정도)가 24.85%이므로 평균 대비 적당히 퍼져있는 편
