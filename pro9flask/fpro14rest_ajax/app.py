from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymysql

app = Flask(__name__);

@app.get("/")
def index():
    return render_template("main.html")

@app.get("/legacy")
def legacy_f():
    pass    # 생략

@app.get("/async")
def async_f():
    pass    # 생략

@app.get("/fetch")
def fetch_f():
    return render_template("show3.html")

@app.get("/axios")
def axios_f():
    return render_template("show4.html")

@app.get("/api/sangdata")
def sangdata():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123",
        database="test",
        charset="utf8"
    )

    cur = conn.cursor()
    cur.execute("select code,sang,su,dan from sangdata")
    columns = [col[0] for col in cur.description]  # 칼럼명 얻기
    rows = cur.fetchall()
    result = [dict(zip(columns, row)) for row in rows]   # [{'code':1,'sang':'장갑','su': 3,'dan':10000}, ...
    print(result)
    cur.close()
    conn.close()

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);