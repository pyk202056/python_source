# web server : html 서비스가 가능한 서버
# 웹 서버(Web Server)는 클라이언트(웹 브라우저)의 요청을 받아 
# HTTP 또는 HTTPS를 통해 HTML 문서, 이미지, CSS, 자바스크립트 같은 
# 정적 웹 콘텐츠를 제공하는 하드웨어 및 소프트웨어 시스템

# 단순한 HTTPServer 구축 - 기본적인 socket 연결

from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7777

# get 요청에 대해 문서를 읽어 클라이언트로 전송하는 역할
handler = SimpleHTTPRequestHandler

# HTTPServer 객체 생성
serv = HTTPServer(('192.168.0.32', PORT), handler)  # 127.0.0.1
print('웹 서비스 시작 ...')

serv.serve_forever()   # 무한 웹 서비스 진행