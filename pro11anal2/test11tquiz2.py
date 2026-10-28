# [two-sample t 검정 : 문제2]  
# 아래와 같은 자료 중에서 남자와 여자를 각각 15명씩 무작위로 비복원 추출하여 혈관 내의 콜레스테롤 양에 차이가 있는지를 검정하시오.
# 수집된 자료 :  
#   남자 : 0.9 2.2 1.6 2.8 4.2 3.7 2.6 2.9 3.3 1.2 3.2 2.7 3.8 4.5 4 2.2 0.8 0.5 0.3 5.3 5.7 2.3 9.8
#   여자 : 1.4 2.7 2.1 1.8 3.3 3.2 1.6 1.9 2.3 2.5 2.3 1.4 2.6 3.5 2.1 6.6 7.7 8.8 6.6 6.4

# 귀무 : 남녀의 모집단 평균 콜레스테롤 양은 같다.
# 대립 : 남녀의 모집단 평균 콜레스테롤 양은 다르다.

from scipy import stats
import pandas as pd
import numpy as np

M = [0.9, 2.2, 1.6, 2.8, 4.2, 3.7, 2.6, 2.9, 3.3, 1.2, 3.2, 2.7, 3.8, 4.5, 4, 2.2, 0.8, 0.5, 0.3, 5.3, 5.7, 2.3, 9.8]
W = [1.4, 2.7, 2.1, 1.8, 3.3, 3.2, 1.6, 1.9, 2.3, 2.5, 2.3, 1.4, 2.6, 3.5, 2.1, 6.6, 7.7, 8.8, 6.6, 6.4]

m_choice = np.random.choice(M, size=15, replace=False)
w_choice = np.random.choice(W, size=15, replace=False)

# 평균
print('남자 평균 :', np.mean(m_choice))   # 2.880000
print('여자 평균 :', np.mean(w_choice))   # 3.233333

# 정규성 검정
print('남자 정규성 :', stats.shapiro(m_choice))  # 0.612885
print('여자 정규성 :', stats.shapiro(w_choice))  # 0.003778

# 등분산성 검정
print('등분산성 :', stats.levene(m_choice, w_choice).pvalue)    # 등분산성 : 0.99190664

# 독립 표본 t검정
result = stats.ttest_ind(m_choice, w_choice, equal_var=True)
print(result)

if result.pvalue < 0.05:
    print('귀무가설 기각 : 남녀 평균 콜레스테롤 양에 차이가 있다')
else:
    print('귀무가설 채택 : 남녀 평균 콜레스테롤 양에 차이가 없다')
