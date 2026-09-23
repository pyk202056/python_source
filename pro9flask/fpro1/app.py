# pip install flask
# pip install waitress    # 실무용 서버

from flask import Flask   # 웹서버(WAS, Application Server) 생성에 필요
# 현재 WAS : py 프로그램 코드를 실행해서 요청을 처리하는 서버

# Flask 기본 웹서버는 실무용 아님, 개발/학습용  - Light-weight server
# 실무용 서버 : gunicorn, waitress, Nginx ...
from waitress import serve   # waitress 서버 서비스 용

app = Flask(__name__);  # Flask 객체 생성. 현재 모듈의 이름을 생성자에 전달

@app.route("/")   # URL 매핑(라우팅). 클라이언트 요청이 '/'일 때 아래 함수 수행
def abc():  # 클라이언트 요청을 처리하는 핸들러 함수
    return "<h2>안녕하세요</h2> 반가워요";   # 클라이언트 브라우저에 반환(전송)

@app.route("/about")
def about():
    return "플라스크에 대해 ...";

@app.route("/user/<name>")   # URL에 변수에 값이 담긴 경우
def user(name):
    return f"네 친구 {name}";

if __name__ == '__main__':
    # app.run()   # 실습용 기본 서버로 서비스 실행
    # app.run(debug=False, host='127.0.0.1', port=5000); 위와 동일
    # app.run(debug=True, host='0.0.0.0', port=5000);

    # waitress 서버 사용 시
    print("웹 서버 서비스 중...");
    serve(app=app, host='0.0.0.0', port=8000);
