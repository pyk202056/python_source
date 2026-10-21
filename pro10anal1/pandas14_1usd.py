# 네이버의 증권 사이트에서 미국 usd 원화 출력하기 - JSON 자료
import requests

# naver.com -> 증권 -> 시장지표 -> F12 -> Network 탭 -> Fetch/XHR 탭 
# -> F5(새로 구침) -> 왼쪽메뉴 : latest클릭 한 후 Headers 탭에서 
# 하위 항목 중 Request header에서 :path의 /api... 에서 
# "https://api.stock.naver.com/에 marketindex/exchange/FX_USDKRW 만 붙인다.
# 그러면 json 자료를 얻을 수 있다.

url = "https://api.stock.naver.com/marketindex/exchange/FX_USDKRW"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://stock.naver.com/"  # 요청이 시작된 웹페이지의 주소를 전달
}

res = requests.get(url, headers=headers, timeout=10)
res.raise_for_status()  # HTTP 응답 상태 코드가 오류를 나타내면 예외를 발생시키는 메서드

data = res.json()

# exchangeInfo 내부에 closePrice 존재
price = float(data["exchangeInfo"]["closePrice"].replace(",", ""))
print(f"미국 USD 환율 : {price:,.2f}원")

# 실제 API 응답 구조는 다음과 같다. (일부 생략)
# {
#     "exchangeInfo": {
#         "name": "미국 USD",
#         "closePrice": "1,410.40",
#         "unit": "KRW",
#         "localTradedAt": "2026-08-10T09:06:34+09:00"
#     },
#     "marketIndexCdList": ["FX_USDKRW", "FX_USDKRW_SHB"],
#     "nationTypeCode": "USA"
# }