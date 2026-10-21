# 원격 DB 연동 : jikwon 자료를 읽어 DataFrame에 저장
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv

config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    sql = """
    select jikwonno,jikwonname,busername,jikwonjik,jikwongen,jikwonpay
    from jikwon inner join buser on jikwon.busernum=buser.buserno
    """
    cursor.execute(sql)

    # for(jikwonno,jikwonname,busername,jikwonjik,jikwongen,jikwonpay) in cursor:
    #     print(jikwonno,jikwonname,busername,jikwonjik,jikwongen,jikwonpay)

    # jikwon자료 -> DataFrame으로 저장 - 방법1 : DataFrame에 저장
    df1 = pd.DataFrame(cursor.fetchall(), 
            columns=['jikwonno','jikwonname','busername','jikwonjik','jikwongen','jikwonpay'])
    print(df1.head(3))
    print('연봉의 총합 : ', df1['jikwonpay'].sum())  # 159150

    print("DataFrame의 자료를 csv 파일로 저장")
    cursor.execute(sql)
    # 이미 읽은 자료는 DataFrame에 한 행씩 처리 완료되어 RAM에는 자료 소진됨. 그래서 다시 읽기 필요

    with open('pandas16.csv', mode='w', encoding='utf-8') as fobj:
        writer = csv.writer(fobj)
        for row in cursor.fetchall():
            writer.writerow(row)

    # csv 파일을 읽어 DataFrame에 저장
    dfcsv = pd.read_csv('pandas16.csv', header=None, 
                names=['번호','이름','부서','직급','성별','연봉'])
    print(dfcsv.head(3))

    print("\n\n")
    # jikwon자료 -> DataFrame으로 저장 - 방법2 : DataFrame에 저장
    df2 = pd.read_sql(sql, conn)   # 비공식
    df2.columns = ['번호','이름','부서','직급','성별','연봉']
    print(df2.head(3))
    print()
    print(df2[:3])    # 슬라이싱
    print()
    print(df2[:-27])
    print()
    print('건수 : ', df2['이름'].count(), ' ', len(df2))   # 30  30
    print('부서별 인원수:', df2['부서'].value_counts())
    print('연봉 8000 이상:', df2.loc[df2['연봉'] >= 8000])
    
    # 교차표 출력(성별, 직급별 인원수)
    ctab = pd.crosstab(df2['성별'], df2['직급'], margins=True)
    print('교차표:\n', ctab)

    # 시각화
    jik_ypay = df2.groupby(['직급'])['연봉'].mean()  # 직급별 연봉 평균
    print('jik_ypay : ', jik_ypay)

    plt.pie(jik_ypay, explode=(0.2, 0, 0, 0.3, 0), 
            labels=jik_ypay.index, shadow=True)
    plt.show()
except Exception as e:
    print('처리 오류 : ', e)
finally:
    cursor.close()
    conn.close()