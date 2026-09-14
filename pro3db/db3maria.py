# MariaDB : jikwon, buser table
# 직원번호, 직원명을 입력하여 로그인에 성공하면 해당직원, 부서 정보 출력
import MySQLdb
import json

# DB 연결 정보 읽기 1 : json 파일 읽기
# with open('dbconnect.json', mode='r', encoding='utf-8') as f:
#     config = json.load(f)

# DB 연결 정보 읽기 2 : .env 파일 읽기 (환경 설정 값을 코드와 분리)
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')),      # port는 숫자 처리
    'charset':os.getenv('DB_CHARSET')
}

def LoginFunc():
    conn = None 

    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        jikwon_no = input("직원번호:")
        jikwon_name = input("직원이름:")
        if jikwon_no == "" or jikwon_name == "":
            print("로그인 정보를 입력하세요")
            return

        """
        sql = '''
            select jikwonno as 직원번호,jikwonname as 직원명,
            busername as 부서명,jikwonjik as 직급,jikwongen as 성별
            from jikwon 
            left outer join buser on jikwon.busernum = buser.buserno
            where jikwonno={0} and jikwonname={1}
        '''.format(jikwon_no, jikwon_name)
        """

        # 추천 방법
        sql = """
            select 
            j.jikwonno as 직원번호,j.jikwonname as 직원명,
            b.busername as 부서명,j.jikwonjik as 직급,j.jikwongen as 성별
            from jikwon j
            left outer join buser b on j.busernum = b.buserno
            where jikwonno=%s and jikwonname=%s
        """

        # sql 실행
        cursor.execute(sql, (jikwon_no, jikwon_name))

        # 로그인 성공 직원 정보 출력
        data = cursor.fetchone()

        if data:
            print("로그인 성공~~~")
            print("직원번호 : ", data[0])
            print("직원명 : ", data[1])
            print("부서명 : ", data[2])
            print("직급 : ", data[3])
            print("성별 : ", data[4])
        else:
            print("로그인 실패 : 입력자료 확인하세요")
    except Exception as e:
        print('에러:', e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    LoginFunc()