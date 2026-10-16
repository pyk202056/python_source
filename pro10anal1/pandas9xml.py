# Pandas는 URL을 이용해 웹상의 CSV 파일이나 HTML 표 데이터를 DataFrame으로 읽기 가능.
# XML은 데이터를 태그 형태로 구조화해서 저장/전송하는 문서 형식

import xml.etree.ElementTree as etree

xmlfile = etree.parse("pandas9my.xml")
print(xmlfile, type(xmlfile))

root = xmlfile.getroot()
print(root.tag)
print(root[0].tag)
print(root[0][0].tag)
# ...
print()
myname = root.find("item").find("name").text
mytel = root.find("item").find("tel").text
print(myname + " " + mytel)

print("\n--- 기상청 제공 XML 자료 읽기 ---")
import requests

url = "https://www.kma.go.kr/XML/weather/sfc_web_map.xml"
headers = {"User-Agent":"Mozila/5.0"}

res = requests.get(url, headers=headers)
res.raise_for_status()   # 응답 코드 확인
print(res.text, type(res.text))  # ... <class 'str'>

root = etree.fromstring(res.text)
print(root)  # <Element '{current}current' at 0x000001E48F7D4900>

# {current"} namespace 제거
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]  # '}'를 기준으로 잘라 태그명만 남김
# {current"}weather  -> weather

print()
weather = root.find('weather')
year = weather.get('year')   # 속성값 얻기
month = weather.get('month')
day = weather.get('day')
hour = weather.get('hour')
print(f"{year}년 {month}월 {day}일 {hour}시 현재 예보")

# 각 지역 순회
for local in weather.findall("local"):
    name = local.text.strip()  # 지역명 (태그 안에 문자열)
    # print(name, local.attrib)
    desc = local.get("desc")   # 날씨 (요소의 desc 속성값)
    ta = local.get("ta")       # 온도 (요소의 ta 속성값)
    print(f"{name} 지역 날씨는 {desc} 온도는 {ta}")
