# [ANOVA 예제 2]
# DB에 저장된 buser와 jikwon 테이블을 이용하여 
# 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 있는지 검정하시오. 
# 만약에 연봉이 없는 직원이 있다면 작업에서 제외한다.

# 귀무 : 연봉 평균에 차이가 없다.
# 대립 : 연봉 평균에 차이가 있다.

import pandas as pd
import numpy as np
import pymysql
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import koreanize_matplotlib

config = {"host": "127.0.0.1", 
        "user": "root", 
        "passwd": "123",
        "db": "test", 
        "port": 3306, 
        "charset": "utf8"
}

try:
    conn = pymysql.connect(**config)
    sql = """
    select jikwonno,jikwonname,busername,jikwonjik,jikwongen,jikwonpay
    from jikwon inner join buser on jikwon.busernum=buser.buserno 
    where jikwonpay is not null
    """
    df = pd.read_sql(sql, conn)
    # print(df)
except Exception as e:
    pass
finally:
    conn.close()

gr1 = df[df["busername"] == "총무부"]["jikwonpay"]
gr2 = df[df["busername"] == "영업부"]["jikwonpay"]
gr3 = df[df["busername"] == "전산부"]["jikwonpay"]
gr4 = df[df["busername"] == "관리부"]["jikwonpay"]

print(f"총무부 연봉 평균 : {np.mean(gr1)}")   # 5414.2
print(f"영업부 연봉 평균 : {np.mean(gr2)}")   # 4908.3
print(f"전산부 연봉 평균 : {np.mean(gr3)}")   # 5328.5
print(f"관리부 연봉 평균 : {np.mean(gr4)}")   # 6262.5

# 평균 데이터 분포 시각화
plt.boxplot([gr1,gr2,gr3,gr4], label=["총무부","영업부","전산부","관리부"], meanline=True, showmeans=True)
plt.title("부서별 연봉 평균")
plt.xlabel("부서")
plt.ylabel("연봉")
plt.show()

# 1. 정규성 확인
print(stats.shapiro(gr1).pvalue)    # 0.026044 --> 0.05보다 작다   정규성 위반
print(stats.shapiro(gr2).pvalue)    # 0.025608 --> 0.05보다 작다   정규성 위반
print(stats.shapiro(gr3).pvalue)    # 0.419407 --> 0.05보다 크다   정규성 만족
print(stats.shapiro(gr4).pvalue)    # 0.907802 --> 0.05보다 크다   정규성 만족

print()
# 2. 등분산성 확인
print(stats.levene(gr1,gr2,gr3,gr4).pvalue) # 0.79807  --> 0.05보다 크다

print()
# 정규성 위반 --> Kruskal-Wallis test
# 3. Kruskal-Wallis test
print(stats.kruskal(gr1, gr2, gr3, gr4))
# KruskalResult : statistic=1.67125225, pvalue=0.6433438
# 결론: pvalue 0.64 > alpha 0.05 이므로 귀무 기각 실패 (채택)
# 부서별 연봉 평균에 차이가 없다.

# 사후 검정
tukResult = pairwise_tukeyhsd(endog=df.jikwonpay, groups=df.busername)  
print(tukResult)

# 시각화
tukResult.plot_simultaneous(xlabel='연봉 평균', ylabel='부서명')
plt.show()





# try:
#     conn = pymysql.connect(**config)
#     sql = """
#         select b.busername, j.jikwonpay 
#         from jikwon j 
#         join buser b on j.busernum = b.buserno
#     """
#     df = pd.read_sql(sql,conn)
# except Exception as e:
#     pass
# finally:
#     conn.close()
# df = df.dropna(subset=['jikwonpay']) # jikwonpay Na 제거