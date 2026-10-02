from flask import Flask, render_template, request, redirect, url_for, flash
# pip install pymysql
import pymysql
import os

from flask import get_flashed_messages   # 저장해 둔 메세지를 꺼내는 함수
# 예: flash("에러~~") -> 메세지를 세션에 잠시 저장 후 get_flashed_messages()하면 메세지 읽기 가능

from dotenv import load_dotenv
load_dotenv()  # .env 파일이 있다면 로딩

app = Flask(__name__);
app.secret_key = "abcd1234"   # 쿠키 서명용 비밀키

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
    # DictCursor : select 결과를 'dict type' 형태로 접근 가능
    # 예: {'code':1,'sang':'mouse' ...} --> row['code'], row['sang'] 가능. 원래는 row[0] 이런 식

@app.get("/")
def index():
    return redirect(url_for("show_list"))

@app.get("/show/")
def show_list():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("select code,sang,su,dan from sangdata order by code asc")
            rows = cur.fetchall()

        messages = list(get_flashed_messages())
        return render_template("list.html", rows=rows, messages=messages)
    except pymysql.err.IntegrityError as e:
        print(e)
    except Exception as e2:
        return f"에러 발생 {e2}"
    finally:
        conn.close()

@app.get("/add/")
def add_form():
    messages = list(get_flashed_messages())
    return render_template("form_add.html", messages=messages)   # 추가 폼 호출

@app.post("/add/")
def add_save():    # 추가 처리
    sang = (request.form.get("sang") or "").strip()
    su_raw = (request.form.get("su") or "").strip()    # "23"
    dan_raw = (request.form.get("dan") or "").strip()

    # 서버에서도 클라이언트가 전달한 입력자료 검사
    if not sang or not su_raw.isdigit() or not dan_raw.isdigit():
        flash("sang은 필수, su, dan은 숫자만 허용")
        return redirect(url_for("add_form"))

    su = int(su_raw)   # 연산없이 추가할 경우라면 숫자화하지 않아도 됨
    dan = int(dan_raw)

    # 새상품 추가 처리
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # code는 자동증가를 위해 프로그램으로 작성
            cur.execute("select max(code) as max_code from sangdata")
            row = cur.fetchone()
            max_code = row["max_code"] if row else None
            next_code = (max_code + 1) if max_code is not None else 1

            # 추가
            cur.execute(
                "insert into sangdata(code,sang,su,dan) values (%s,%s,%s,%s)",
                (next_code, sang, su, dan)    
            )

        conn.commit()
        return redirect(url_for("show_list"))   # 추가 후 목록 보기
    except Exception as e:
        conn.rollback()
        flash(f"저장 실패 : {e}")
        return redirect(url_for("add_form"))
    finally:
        conn.close()


@app.get("/edit/<int:code>/")   # <a href="/edit/1/">수정</a>
def edit_form(code:int):   # 수정 폼 호출
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("select * from sangdata where code=%s", (code,))
            row = cur.fetchone()

        if not row:
            flash("해당 자료가 없어요")
            return redirect(url_for("show_list"))

        messages = list(get_flashed_messages())
        return render_template("form_edit.html", row=row, messages=messages)
    finally:
        conn.close()

@app.post("/edit/<int:code>")
def edit_save(code:int):   # 수정 처리
    sang = (request.form.get("sang") or "").strip()
    su_raw = (request.form.get("su") or "").strip() 
    dan_raw = (request.form.get("dan") or "").strip()

    # 서버에서도 클라이언트가 전달한 입력자료 검사
    if not sang or not su_raw.isdigit() or not dan_raw.isdigit():
        flash("sang은 필수, su, dan은 숫자만 허용")
        return redirect(url_for("edit_form", code=code))

    su = int(su_raw)   # 연산없이 추가할 경우라면 숫자화하지 않아도 됨
    dan = int(dan_raw)

    # 수정하기
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("update sangdata set sang=%s,su=%s,dan=%s where code=%s", 
            (sang, su, dan, code))

        conn.commit()
        return redirect(url_for("show_list"))   # 수정 후 목록 보기
    except Exception as e:
        conn.rollback()
        flash(f"수정 실패 : {e}")
        return redirect(url_for("edit_form", code=code))
    finally:
            conn.close()

@app.post("/delete/<int:code>/")
def delete_row(code:int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # 삭제하기
            cur.execute("delete from sangdata where code=%s", (code,))

        conn.commit()
        return redirect(url_for("show_list"))  # 삭제 후 목록 보기
    except Exception as e:
        conn.rollback()
        flash(f"삭제 실패 : {e}")
        return redirect(url_for("show_list"))
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);