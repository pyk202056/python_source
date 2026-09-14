# 원격 데이터베이스와 연동 프로그래밍
# MariaDB : 
# 준비1) IP(네트워크에서 컴퓨터나 장치를 구분하기 위한 규약)) 주소 필요.  
# 준비2) 연결용 Driver file (모듈) 필요

# pip install mysqlclient

import MySQLdb

"""
# 연결 정보 매핑 방법1
conn = MySQLdb.connect( # DB연결 담당
    host='127.0.0.1',   # 192.168.0.32, localhost
    user='root',
    password='123',
    database='test',
    port=3306      # MariaDB/MySQL 서버가 기본적으로 사용하는 포트 번호
)
"""

# 연결 정보 매핑 방법2
"""
config_data = {
    "host":"127.0.0.1",
    "user":"root",
    "password":"123",
    "database":"test",
    "port":3306,
    "charset":"utf8"
}
"""

# 연결 정보 매핑 방법3
# 별도 저장된 json 파일 읽기
import json

with open('dbconnect.json', mode='r', encoding='utf-8') as f:
    config_data = json.load(f)

def myFunc():
    try:
        # 방법 2, 3
        conn = MySQLdb.connect(**config_data)
        # conn.autocommit(True)    # 자동 커밋
        # conn.autocommit(False)   # 수동 커밋 : 기본값

        cursor = conn.cursor()

        # 자료 추가
        # isql = "insert into sangdata(code,sang,su,dan) values(5,'마스크',5,'3000')"
        # cursor.execute(isql)
        # conn.commit()

        """
        isql = "insert into sangdata values(%s,%s,%s,%s)"
        # ins_data = (6,'커피',10,5000)   # tuple type
        ins_data = 6,'커피',10,5000       # tuple type
        cursor.execute(isql, ins_data)
        conn.commit()    # 원격 DB에 저장됨
        """

        # 자료 수정
        """
        usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"
        up_data = '물티슈', 3, 1000, 5   # ('물티슈', 3, 1000, 5)
        cursor.execute(usql, up_data)
        conn.commit()
        """

        """
        usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"
        up_data = '콜라', 11, 3000, 6   
        # insert, update, delete는 성공하면 성공 갯수, 실패하면 0을 반환
        cou = cursor.execute(usql, up_data)
        print("수정 갯수 : ", cou)
        conn.commit()
        """

        # 자료 삭제
        code = '6';
        # dsql = "delete from sangdata where code=" + code
        # print(dsql)
        # 참고 : secure coding 가이드라인에 맞게 프로그래밍 해야 한다. 
        # 해킹 위험 : SQL 인젝션은 사용자의 입력값을 검증하지 않는 웹 애플리케이션의 허점을 악용해 악의적인 SQL 쿼리문을 실행하고 데이터베이스를 조작하는 해킹 기법
        # dsql = "delete from sangdata where code='{0}'".format(code)
        
        dsql = "delete from sangdata where code=%s"  # 추천 : 권장
        # cursor.execute(dsql, (code,))

        cou = cursor.execute(dsql, (code,))  # 삭제 후 반환 값 얻기
        if cou != 0:
            print('삭제 성공')
        else:
            print('삭제 실패')

        conn.commit()

        # 자료 읽기
        # sql = "select * from sangdata"
        sql = "select code,sang,su,dan from sangdata"
        cursor.execute(sql)
        for data in cursor.fetchall():
            # print(data)
            print("%s %s %s %s"%data)

        print()
        cursor.execute(sql)
        for data in cursor:
            print(data[0], data[1], data[2], data[3])

        print()
        cursor.execute(sql)
        for code, sang, su, dan in cursor:
            print(code, sang, su, dan)

        print()
        cursor.execute(sql)
        for a, b, 수량, 단가 in cursor:
            print(a, b, 수량, 단가 * 1000)
    except Exception as e:
        print('처리 오류 : ', e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    myFunc()

