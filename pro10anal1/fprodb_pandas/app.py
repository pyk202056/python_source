from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
from markupsafe import escape
# 웹에 출력되는 입력값의 특수 문자(예:<,>,&,")를 안전한 HTML 엔티티(예:&lt;,&gt;)로 변환하여 XSS 공격 방지

# 직원번호, 직원명, 부서명, 부서전화, 연봉, 직급 자료 읽어 출력

app = Flask(__name__)

config = {
    'host':'127.0.0.1', 'user':'root', 'password':'123', 'database':'test',
    'port':3306, 'charset':'utf8mb4'
}

def get_connection():
    return pymysql.connect(**config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dbshow", methods=['GET', 'POST'])
def dbshow():
    # 부서명을 입력받아 해당 부서에 근무 직원 출력
    dept = request.args.get("dept", "").strip()

    sql = """
        select j.jikwonno as 직원번호,j.jikwonname as 직원명,
        b.busername as 부서명,b.busertel as 부서전화,
        j.jikwonpay as 연봉,j.jikwonjik as 직급
        from jikwon j inner join buser b
        on j.busernum=b.buserno
    """
    params = []
    if dept:
        sql += " where b.busername like %s"
        params.append(f"{dept}%")

    sql += " order  by j.jikwonno asc"

    # SQL 실행
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]  # description:칼럼 등 여러 정보 반환

    df = pd.DataFrame(rows, columns=cols)
    # print(df.to_html(index=False))

    # DataFrame을 table tag로 만들기
    if not df.empty:
        jikwondata = df[['직원번호','직원명','부서명','부서전화','연봉']].to_html(index=False)
        # jikwondata = df.to_html(index=False)
    else:
        jikwondata = "직원 정보가 없어요"

    # print(jikwondata)

    # 직급별 연봉 통계
    if not df.empty:
        stats_df = (
            df.groupby("직급")["연봉"]
            .agg(평균 = "mean", 표준편차=lambda x:x.std(ddof=0)) # ddof=0(모표준편차),1(표본표준편차)
            .round(2)
            .reset_index()
            .sort_values(by='평균', ascending=False)
        )
        stats_df['표준편차'] = stats_df['표준편차'].fillna(0)
        # print(stats_df.to_html(index=False))
        statsdata = stats_df.to_html(index=False)
    else:
        statsdata = "통계 대상 자료가 없어요"

    # 부서별 직급별 직원 수 교차표
    if not df.empty:
        crosst = pd.crosstab(
            index=df['부서명'], columns=df['직급'], margins=True, margins_name='합계'
        )
        crossdata = crosst.to_html()
    else:
        crossdata = "교차표 대상 자료가 없어요"

    # return render_template("dbshow.html", jikwondata=df.to_html(index=False))
    return render_template("dbshow.html", \
                        jikwondata=jikwondata,
                        statsdata=statsdata,
                        crossdata=crossdata,
                        dept=escape(dept)  # xss 방지
    )


if __name__ == '__main__':
    app.run(debug=True)