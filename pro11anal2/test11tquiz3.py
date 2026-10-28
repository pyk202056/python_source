# [two-sample t 검정 : 문제3]
# DB에 저장된 jikwon 테이블에서 총무부, 영업부 직원의 연봉의 평균에 차이가 존재하는지 검정하시오.
# 연봉이 없는 직원은 해당 부서의 평균연봉으로 채워준다.

# 귀무가설 : 총무부와 영업부의 평균 연봉은 같다.
# 대립가설 : 총무부와 영업부의 평균 연봉은 다르다

import pymysql
from scipy import stats
import pandas as pd

alpha = 0.05

config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database' : 'test',
    'port' : 3306,
    'charset':'utf8'
}

sql = """
SELECT j.jikwonno 사번, j.jikwonname 이름, b.busername 부서, j.jikwonpay 연봉
from jikwon as j INNER JOIN buser AS b ON j.busernum = b.buserno
WHERE b.busername IN ('총무부', '영업부')
"""

conn = pymysql.connect(**config)

try:
    with conn.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=['사번', '이름', '부서', '연봉'])
finally:
    conn.close()

# print(df)

df['연봉'] = pd.to_numeric(df['연봉'], errors='coerce')

# 부서별 직원 자료 분리
chongmu = df[df['부서'] == '총무부']
youngup = df[df['부서'] == '영업부']

# 각 부서에서 연봉 열만 선택
pay1 = chongmu['연봉']
pay2 = youngup['연봉']

print('\n총무부 현황')
print('전체 인원:', len(pay1))
print('연봉이 있는 인원:', pay1.count())
print('평균 연봉:', pay1.mean())
print('연봉 결측치 수:', pay1.isnull().sum())

print('\n영업부 현황')
print('전체 인원:', len(pay2))
print('연봉이 있는 인원:', pay2.count())
print('평균 연봉:', pay2.mean())
print('연봉 결측치 수:', pay2.isnull().sum())

pay1 = pay1.fillna(pay1.mean())
pay2 = pay2.fillna(pay2.mean())

# 정규성 확인
if len(pay1) >= 3 and len(pay2) >= 3:
    print('\n총무부 정규성 p값:', stats.shapiro(pay1).pvalue)
    print('영업부 정규성 p값:', stats.shapiro(pay2).pvalue)
else:
    print('\n정규성 검정은 각 부서에 자료가 최소 3개씩 필요합니다.')

# 등분산성 확인
levene_result = stats.levene(pay1, pay2)
print('등분산성 p값:', levene_result.pvalue)

if levene_result.pvalue >= alpha:
    print('등분산 귀무가설을 기각 X: 등분산 가정한 t 검정')
    result = stats.ttest_ind(pay1, pay2, equal_var=True)
else:
    print('등분산을 가정하지 않는 Welch t 검정')
    result = stats.ttest_ind(pay1, pay2, equal_var=False)

print('\n독립표본 t 검정 결과')
print('총무부 평균 연봉:', pay1.mean())
print('영업부 평균 연봉:', pay2.mean())
print('t 통계량:', result.statistic)
print('p값:', result.pvalue)
print('유의수준:', alpha)

if result.pvalue < alpha:
    print('귀무가설 기각')
    print('총무부와 영업부의 평균 연봉에 통계적으로 유의한 차이가 있다.')
else:
    print('귀무가설 채택')
    print('총무부와 영업부의 평균 연봉에 통계적으로 유의한 차이가 없다.')
