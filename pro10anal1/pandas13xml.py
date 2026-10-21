# BeautifulSoup 객체로 XML 문서 처리
from bs4 import BeautifulSoup

with open("pandas9my.xml", mode="r", encoding="utf-8") as f:
    xmlfile = f.read()
    print(xmlfile, type(xmlfile))  # <class 'str'>

soup = BeautifulSoup(xmlfile, "lxml")
print(type(soup))  # <class 'bs4.BeautifulSoup'>

itemTag = soup.find_all("item")
print(itemTag[1])  # <name id="ks2">고릴라</name> ...
print()
nameTag = soup.find_all("name")
print(nameTag[1])
print(nameTag[1]["id"])   # ks2

print("---")
for i in itemTag:
    nameTag = i.find_all("name")
    for j in nameTag:
        print("id:" + j["id"] + " name:" + j.string)
        tel = i.find("tel")
        print("tel:", tel.string)

    for j in i.find_all("exam"):
        print("kor:" + j["kor"] + ", eng:" + j["eng"])
    print()

print("\n\n서울시 제공 도서관 XML 샘플 문서 정보 읽기")
import urllib.request as req
import pandas as pd

url = "http://openapi.seoul.go.kr:8088/sample/xml/SeoulLibraryTimeInfo/1/5/"
plainText = req.urlopen(url).read().decode()
# print(plainText)

xmlObj = BeautifulSoup(plainText, "xml")  # lxml하면 태그명이 소문자가 됨
libData = xmlObj.select("row")
# print(libData)
rows = []
for data in libData:
    name = data.find("LBRRY_NAME").string
    addr = data.find("ADRES").string
    print("도서관명:", name)
    print("주소:", addr)
    print()
    rows.append({"도서관명":name,"주소":addr})

df = pd.DataFrame(rows)
print(df)
print("건수 : ", len(df))
