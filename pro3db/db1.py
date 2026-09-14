# SQLite : 개인용 DB, python에 기본 내장. 경량 DBMS
# 서버를 운영하지 않아 시스템 내에서 별도의 자원을 사용할 필요가 없다.

import sqlite3

print(sqlite3.sqlite_version)
print()
# conn = sqlite3.connect('exam.db') # DB연결 담당. 파일에 데이터 보관
conn = sqlite3.connect(':memory:')  # RAM에서만 작업. 휘발성

try:
    cur = conn.cursor();  # SQL 처리를 위한 객체 생성. SQL 실행 담당

    # 테이블 생성
    cur.execute("create table if not exists friends(name text, phone text, addr text)")

    # 자료 입력
    cur.execute("insert into friends values('홍길동','111-1111','서초1동')")
    cur.execute("insert into friends values(?,?,?)", ('이기자','111-2222','서초2동'))

    inputdatas = ('신기해','111-1234','서초3동')
    cur.execute("insert into friends values(?,?,?)", inputdatas)

    inputdatas2 = (('신기한','111-3333','역삼1동'),('신기루','111-4444','역삼2동'))
    cur.executemany("insert into friends values(?,?,?)", inputdatas2)
    conn.commit()

    # 자료 보기
    cur.execute("select * from friends")
    #print(cur.fetchone())   # 한 개의 행(레코드) 읽기 - record pointer가 있는 지점의 자료만 읽음
    #print(cur.fetchone())
    print(cur.fetchall())    # 모든 행(레코드) 읽기[('홍길동', '111-1111', '서초1동'), ...
    print()
    cur.execute("select name,addr,phone from friends")
    for r in cur:
        #print(r)
        print(r[0] + '님의 주소는 ' + r[1] + ' ' + r[2])
except Exception as e:
    print('err : ', e)
    conn.rollback()
finally:
    conn.close()