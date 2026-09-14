# mariadb : jikwon, buser table

# 직원번호, 직원명을 입력하여 로그인에 성공하면 해당 직원, 부서 정보 출력
import MySQLdb
import json
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

def loginfunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)  
        cursor = conn.cursor()  # SQL 처리를 위한 객체 생성
        jikwon_no = input('직원번호 : ')
        jikwon_name = input('직원이름 : ')
        if jikwon_no == '' or jikwon_name == '':
            print('로그인 정보를 입력하세요')
            return

        buser_sql = """
        select 
        j.jikwonno as 직원번호, j.jikwonname as 직원명,
        b.busername as 부서명, b.busertel as 부서전화, j.jikwonjik as 직급, j.jikwongen as 성명        
        from jikwon j
        left join buser b on j.busernum = b.buserno
        WHERE j.busernum = (
            SELECT j.busernum FROM jikwon j
            WHERE j.jikwonno=%s and j.jikwonname=%s
        )
        ORDER BY
            CASE j.jikwonjik
                WHEN '사원' THEN 1
                WHEN '대리' THEN 2
                WHEN '과장' THEN 3
                WHEN '차장' THEN 4
                WHEN '부장' THEN 5
                ELSE 6
            END ASC,
            j.jikwonname ASC;
        """

        gogek_sql = """
        SELECT g.gogekno as 고객번호, g.gogekname as 고객명, g.gogektel as 고객전화, 
        (CASE WHEN SUBSTR(g.gogekjumin,8,1) IN ('1','2') THEN 2026 - (1900 + SUBSTR(g.gogekjumin,1,2)) + 1
                ELSE 2026 - (2000 + SUBSTR(g.gogekjumin,1,2)) + 1
        END) AS 나이
        FROM jikwon j
        LEFT JOIN gogek g ON j.jikwonno = g.gogekdamsano
        WHERE j.jikwonno=%s and j.jikwonname=%s
        """

        # sql 실행
        cursor.execute(buser_sql, (jikwon_no, jikwon_name))  # sql 실행

        # 로그인 성공 직원 정보 출력
        jikwon_data = cursor.fetchall()

        if jikwon_data:
            print('로그인 성공\n')
            print('부서 명단')
            print('직원번호 직원명\t부서명\t부서전화\t직급\t성별')
            for row in jikwon_data:
                print(row[0],'\t',row[1],row[2],'\t',row[3],'\t',row[4],'\t',row[5])

            print("직원 수 : ", len(jikwon_data))
        else:
            print("로그인 실패 : 입력 자료 확인하세요")
            return

        print()
        # sql 실행
        cursor.execute(gogek_sql, (jikwon_no, jikwon_name))  # sql 실행

        # 직원이 맡은 고객 정보 출력
        gogek_data = cursor.fetchall()

        if gogek_data:
            print('관리 고객 명단')
            print('고객번호 고객명\t고객전화\t나이')
            for row in gogek_data:
                print(row[0],'\t',row[1],row[2],'\t',int(row[3]))
            print("관리 고객 수 : ", len(gogek_data))
        else:
            print("관리하는 고객이 없습니다.")
        
    except Exception as e:
        print('에러:',e)
    finally:
        if conn: 
            conn.close()  # 연결 종료 


if __name__ == '__main__':
    loginfunc()
