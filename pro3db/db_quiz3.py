# 문3) 직원별 관리 고객 수 출력 (관리 고객이 없으면 출력에서 제외)
# ​
# 직원번호 직원명 관리 고객 수
# 1 홍길동 3
# 2 한송이 1

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
    "charset": os.getenv("DB_CHARSET")
}

def LoginFunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        sql = """
        select j.jikwonno as 직원번호,
                j.jikwonname as 직원명,
                count(g.gogekno) as `관리 고객 수`
                from jikwon j inner join gogek g on j.jikwonno = g.gogekdamsano
                group by j.jikwonno, j.jikwonname
                order by j.jikwonno asc
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        print("=== 직원별 관리 고객 수 ===")
        for row in rows:
            print(f"직원번호:{row[0]}  직원명:{row[1]}  관리 고객 수:{row[2]}")

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    LoginFunc()