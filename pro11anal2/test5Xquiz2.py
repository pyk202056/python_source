#카이제곱 문제2) 지금껏 A회사의 직급과 연봉은 관련이 없다. 
#그렇다면 jikwon_jik과 jikwon_pay 간의 관련성 여부를 통계적으로 가설검정하시오.
#예제파일 : MariaDB의 jikwon table 
#jikwon_jik   (이사:1, 부장:2, 과장:3, 대리:4, 사원:5)
#jikwon_pay (1000 ~2999 :1, 3000 ~4999 :2, 5000 ~6999 :3, 7000 ~ :4)
#조건 : NA가 있는 행은 제외한다.

import pandas as pd
import numpy as np
import pymysql
import scipy.stats as stats

# 귀무가설 : 직급과 연봉은 관련이 없다.
# 대립가설 : 직급과 연봉은 관련이 있다.

config = {"host": "127.0.0.1", 
        "user": "root", 
        "passwd": "123",
        "db": "test", 
        "port": 3306, 
        "charset": "utf8"}

conn = pymysql.connect(**config)
df = pd.read_sql('select jikwonjik, jikwonpay from jikwon', conn)
df = df.dropna()

jik = {"이사":1, "부장 ":2, "과장":3, "대리":4,"사원":5}
df['jik'] = df['jikwonjik'].map(jik)

def get_pay(pay):
    if 1000 <= pay <=2999:
        return 1
    elif 3000 <= pay <=4999:
            return 2
    elif 5000 <= pay <=6999:
            return 3
    else:
        return 4

df['pay'] = df['jikwonpay'].apply(get_pay)
print(df)

print("---")
ctab = pd.crosstab(index=df['jik'], columns=df["pay"])
print(ctab)

chi2, pv,dof, _ = stats.chi2_contingency(ctab)
print("p-value :", pv)  # 0.000300
print("chi2 :", chi2)   # 30.96314
print("dof :", dof)     # 9

if pv < 0.05:
    print("유의수준 0.05보다 pv값이 작으므로 귀무가설 기각")
    print("직급과 연봉은 관련이 있다")
else:
    print("유의수준 0.05보다 pv값이 크므로 귀무가설 채택")
    print("직급과 연봉은 관련이 없다")