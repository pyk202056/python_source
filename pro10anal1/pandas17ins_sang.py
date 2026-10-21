# DataFrame의 자료를 MariaDB(MySQL)  테이블(sangdata)에 저장하기

# pip install sqlalchemy     : DB연결 + 관리 + 추상화를 지원

import pandas as pd
from sqlalchemy import create_engine

data = {
    'code':[10, 11, 12],
    'sang':['맥주','사이다','와인'],
    'su':[20, 22, 5],
    'dan':[5000,3000,70000]
}

engine = None
frame = pd.DataFrame(data)
print(frame)

try:
    # DB 연결
    engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test?charset=utf8mb4")

    # DB에 저장
    cnt = frame.to_sql(name="sangdata", con=engine, if_exists='append', index=False)
    print('저장 행 수 : ', cnt)

    # 저장된 자료 읽기
    df = pd.read_sql("select * from sangdata", engine)
    print(df)
except Exception as e:
    print('처리 오류 : ', e)
finally:
    if engine is not None:
        engine.dispose()    # DB 연결 자원 해제