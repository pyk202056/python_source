from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__);
app.secret_key = "abcd1234"

# MariDB 연결 정보   
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",  # 전세계문자(한글 포함) + 이모지까지 처리 가능
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

@app.get("/")
def index():
    return redirect(url_for("login_form"))

@app.get("/login")
def login_form():
    return render_template("login.html")

@app.post("/login")
def login_post():
    jikwonno_raw = (request.form.get("jikwonno") or "").strip()
    jikwonname = (request.form.get("jikwonname") or "").strip()

    if not jikwonno_raw.isdigit() or not jikwonname:
        flash("직원 번호는 숫자, 직원 이름은 필수입니다")
        return redirect(url_for("login_form"))

    jikwonno = int(jikwonno_raw)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # 로그인 체크
            cur.execute("""
                select jikwonno,jikwonname from jikwon 
                where jikwonno=%s and jikwonname=%s
            """, (jikwonno, jikwonname))

            me = cur.fetchone()
            if not me:
                flash("로그인 실패 : 직원 정보 불일치!!!")
                return redirect(url_for("login_form"))

            # 로그인 성공한 경우
            cur.execute("""
                select jikwonno,jikwonname,busername,jikwonjik,jikwonpay,
                year(jikwonibsail) as jikwonibsail_year
                from jikwon inner join buser
                on busernum=buserno order  by jikwonno
            """)
            rows = cur.fetchall()

        # 세션 생성 : 직원번호와 이름이 dicy type으로 기억
        session["jikwonno"] = me["jikwonno"]
        session["jikwonname"] = me["jikwonname"]

        return render_template("jikwonlist.html", rows=rows, login_user=me)
    finally:
        conn.close()

@app.get("/gogek/<int:jikwonno>")
def gogek_list(jikwonno:int):
    if "jikwonno" not in session:
        flash("로그인 후 이용하세요")
        return redirect(url_for("login_form"))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # gogekdamsano(담당직원번호)로 고객 검색
            cur.execute("""
                select gogekno,gogekname,gogektel from gogek 
                where gogekdamsano=%s order by gogekno
            """, (jikwonno,))
            rows = cur.fetchall()

            # 직원 이름도 같이 표시하기
            cur.execute("select jikwonname from jikwon where jikwonno=%s", (jikwonno,))
            emp = cur.fetchone()

        return render_template(
            "gogek_list.html", 
            rows=rows, empno=jikwonno, empname=(emp["jikwonname"] if emp else "")
        )
    finally:
        conn.close()
    
@app.get("/jikwon")
def jikwon_list():
    if "jikwonno" not in session:
        flash("로그인 후 이용하세요")
        return redirect(url_for("login_form"))

    conn = get_conn()
    try:
        with conn.cursor() as cur:  
            cur.execute("""
                select jikwonno,jikwonname,busername,jikwonjik,jikwonpay,
                year(jikwonibsail) as jikwonibsail_year
                from jikwon inner join buser
                on busernum=buserno order  by jikwonno
            """)
            rows = cur.fetchall()

        login_user = {
            "jikwonno": session["jikwonno"],
            "jikwonname": session["jikwonname"]
        }

        return render_template("jikwonlist.html", rows=rows, login_user=login_user)
    finally:
        conn.close()


@app.post("/logout")  # 로그아웃 - 세션 삭제
def log_out():
    session.clear()
    return redirect(url_for("login_form"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);