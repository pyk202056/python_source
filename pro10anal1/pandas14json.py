# JSON  자료 처리 : XML에 비해 경량이므로 빠른 처리 가능. 배열 개념만 있으면 됨
# BeautifulSoup 지원 X

import json

dict = {"name":"tom","age":23,"score":["90","80","88"]} # dict type
print(dict, type(dict))       # <class 'dict'>

print("\n\njson 인코딩 : dict -> str로 변환")
str_val = json.dumps(dict)
# str_val = json.dumps(dict, indent=4)
print(str_val, type(str_val))  # <class 'str'>
# print(str_val["name"])  # TypeError: string indices must be integers
print(str_val[0:20])  # 문자열 관련 함수만 처리 가능

print("\n\njson 디코딩 : str -> dict로 변환")
json_val = json.loads(str_val)
print(json_val, type(json_val))  # <class 'dict'>
print(json_val["name"])   # dict 관련 명령 처리 가능.  tom

print()
for k in json_val.keys():
    print(k)
print()
for v in json_val.values():
    print(v)

print("\n\n서울시 제공 도서관 JSON 샘플 문서 정보 읽기")
import urllib.request as req
import pandas as pd

url = "http://openapi.seoul.go.kr:8088/sample/json/SeoulLibraryTimeInfo/1/5/"
plainText = req.urlopen(url).read().decode()
# print(plainText)     # str

jsonData = json.loads(plainText)  # json 디코딩
print(type(jsonData))  # dict
print(jsonData["SeoulLibraryTimeInfo"]["row"][1]["LBRRY_NAME"]) # LH강남3단지작은도서관
# print(jsonData["SeoulLibraryTimeInfo"].get("row"))  # [{'LBRRY_SEQ_NO': '2413', 'LBRRY_NAME':...

print("---")
# dict의 get() 사용
libData = jsonData.get("SeoulLibraryTimeInfo").get("row")
# print(libData)
name = libData[0].get("LBRRY_NAME")  
print(name)   # BIBLIOTECA

print()
datas = []
for ele in libData:
    name = ele.get("LBRRY_NAME")
    tel = ele.get("TEL_NO")
    addr = ele.get("ADRES")
    print(name, " ", tel, " ", addr)
    datas.append([name, tel, addr])

df = pd.DataFrame(datas, columns=["도서관명", "전화", "주소"])
print(df)
