from flask import Flask, request, render_template, redirect, url_for, flash
import pymysql
import os

app = Flask(__name__)
app.secret_key = "DEV_SECRET_KEY"     # flash용

# MariaDB 접속 정보 (필요에 맞게 수정)
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
        database=DB_NAME, charset="utf8mb4", 
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )

@app.get("/")
def index():
    return redirect(url_for("show_main"))   

# 목록 + 검색
@app.get("/main")
def show_main():
    q = (request.args.get("q") or "").strip()

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            if q:
                like = f"%{q}%"
                # SQL의 LIKE 검색을 “부분 포함 검색”으로 만들기 위해 사용한 문자열이다.
                # q가 사용자가 검색창에 입력한 단어(예: "길동")라면 "%" + q + "%" 와 같고 결과는 "%길동%" 이 됨. 
                # 예시 매칭 : "홍길동", "길동입니다", "홍길동님 반가워요" ...
                cur.execute(
                    """
                    SELECT id, name, message, created_at FROM guestbook
                    WHERE name LIKE %s OR message LIKE %s ORDER BY id DESC
                    """,
                    (like, like)
                )
            else:
                cur.execute(
                    """
                    SELECT id, name, message, created_at FROM guestbook
                    ORDER BY id DESC
                    """
                )
            rows = cur.fetchall()

        return render_template("main.html", rows=rows, q=q)
    finally:
        conn.close()

# 추가 폼
@app.get("/add")
def add_form():
    return render_template("add.html")

# 추가 처리
@app.post("/add")
def add_save():
    name = (request.form.get("name") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not name or not message:
        # flash("메세지")는 사용자에게 “한 번만 보여줄 알림 메시지”를 세션에 저장하는 코드
        flash("이름과 메시지는 필수입니다.")  # 메시지를 저장해두면 html에서 get_flashed_messages()로 읽음
        return redirect(url_for("add_form"))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # id는 MariaDB가 자동으로 1부터 넣어줌. AUTO_INCREMENT
            cur.execute(
                "INSERT INTO guestbook (name, message) VALUES (%s, %s)", (name, message)
            )
        conn.commit()
        return redirect(url_for("show_main"))
    finally:
        conn.close()

# 수정 폼
@app.get("/edit/<int:gid>")
def edit_form(gid: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, message, created_at FROM guestbook WHERE id=%s", (gid,)
            )
            row = cur.fetchone()
        if not row:
            flash("수정할 글을 찾을 수 없음.")   # 사용자에게 “한 번만 보여줄 알림 메시지”를 세션에 저장
            return redirect(url_for("show_main"))

        return render_template("edit.html", row=row)
    finally:
        conn.close()

# 수정 처리
@app.post("/edit/<int:gid>")
def edit_save(gid: int):
    name = (request.form.get("name") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not name or not message:
        flash("이름과 메시지는 필수입니다.")
        return redirect(url_for("edit_form", gid=gid))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE guestbook SET name=%s, message=%s WHERE id=%s",
                (name, message, gid)
            )
        conn.commit()
        return redirect(url_for("show_main"))
    finally:
        conn.close()

# 삭제 처리 (POST)
@app.post("/delete/<int:gid>")
def delete_row(gid: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM guestbook WHERE id=%s", (gid,))
        conn.commit()
        return redirect(url_for("show_main"))
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
