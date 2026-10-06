from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from db import get_connFunc

app = Flask(__name__);

@app.get("/")
def index():
    return render_template("index.html")

"""
상품 CRUD라면 보통 이렇게 구성
GET    /api/sangdata       전체조회
GET    /api/sangdata/1     1번 상품 조회
POST   /api/sangdata       상품 추가
PUT    /api/sangdata/1     1번 상품 수정
DELETE /api/sangdata/1     1번 상품 삭제
"""

# 전체 자료 읽기
@app.get("/api/sangdata")
def list_sangdata():
    sql = "select code,sang,su,dan from sangdata order by code asc"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({"ok":True, "datas":rows})

# 새 상품 추가(insert)
@app.post("/api/sangdata")
def create_sangdata():
    data = request.get_json()
    # print("data : ", data)

    code = data["code"]
    sang = data["sang"]
    su = int(data["su"])  # 수량이 연산에 참여하지 않는다면 굳이 int X
    dan = int(data["dan"])
    isql = "insert into sangdata(code,sang,su,dan) values(%s,%s,%s,%s)"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(isql, (code,sang,su,dan))

    return jsonify({"ok":True})

# 상품 수정
@app.put("/api/sangdata/<int:code>")
def update_sangdata(code):
    data = request.get_json()

    sang = data["sang"]
    su = data["su"]
    dan = data["dan"]
    usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(usql, (sang,su,dan,code))

    return jsonify({"ok":True})


# 상품 삭제
@app.delete("/api/sangdata/<int:code>")
def delete_sangdata(code):
    try:
        dsql = "delete from sangdata where code=%s"

        with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(dsql, (code,))
                if cur.rowcount == 0:
                    return jsonify({"ok":False, "msg":"해당 자료 없음"})

        return jsonify({"ok":True, "msg":"삭제 완료"})
    except Exception as err:
        return jsonify({"ok":False, "msg":str(err)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);