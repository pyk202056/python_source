# --- DB(RDBMS) 연동 관련 -----------
# 문1) 부서명을 입력해 해당 부서에 근무하는 직원 출력
# 부서명 입력 : _______
# 직원번호 직원명 부서번호 부서전화 직급 성별
#     1   홍길동  10    111-1111     이사 남 
# ...

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')), 
    'charset':os.getenv('DB_CHARSET'),
    }

def buserFunc():
    conn = None

    try:
        # DB 연결
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        # 부서명 입력
        buser_name = input("부서명 입력 : ")

        if buser_name == "":
            print("부서명을 입력하세요.")
            return

        # 직원 + 부서 JOIN
        sql = """
            SELECT
                j.jikwonno,j.jikwonname,b.buserno,b.busertel,
                j.jikwonjik,j.jikwongen
            FROM jikwon j
            INNER JOIN buser b ON j.busernum = b.buserno
            WHERE b.busername = %s
        """

        cursor.execute(sql, (buser_name,))
        datas = cursor.fetchall()

        # 결과 출력
        if datas:
            print("\n직원번호\t직원명\t부서번호\t부서전화\t직급\t성별")

            for data in datas:
                print(
                    data[0],data[1],data[2],data[3],data[4],data[5],sep="\t"
                )
        else:
            print("해당 부서의 직원이 없습니다.")

    except Exception as e:
        print("처리 오류 :", e)

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    buserFunc()