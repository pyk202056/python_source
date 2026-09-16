# cgi-bin/hello.py : 웹용 파이썬
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 한글 깨짐 방지

ss = "파이썬 자료 출력"  # 파이썬 실행문
# print(ss)   개발자가 자신의 컴 표준 출력장치로 출력

ss2 = 123 + 200   # 파이썬 실행문

# 클라이언트 브라우저로 파이썬 처리 값 출력
print("Contet-Type:text/html; charset=utf-8")
print()
print("<!DOCTYPE html>")
print("<html lang='ko'>")
print("<head>")
print("<meta charset='UTF-8'>")
print("</head>")
print("<html>")
print("<body>")
print("<h2>파이썬 문서의 자료 출력</h2>")
print(f"파이썬 변수 값1 : {ss}<br/>")
print(f"파이썬 변수 값2 : {ss2}<br/>")
print("</body>")
print("</html>")