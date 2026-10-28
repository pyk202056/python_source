# [two-sample t 검정 : 문제1] 
# 다음 데이터는 동일한 상품의 포장지 색상에 따른 매출액에 대한 자료이다. 
# 포장지 색상에 따른 제품의 매출액에 차이가 존재하는지 검정하시오.
# 수집된 자료 :  
#    blue : 70 68 82 78 72 68 67 68 88 60 80
#    red : 60 65 55 58 67 59 61 68 77 66 66

from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import seaborn as sns
import numpy as np

blue = [70, 68, 82, 78, 72, 68, 67, 68, 88, 60, 80]
red = [60, 65, 55, 58, 67, 59, 61, 68, 77, 66, 66]

print('파랑 평균:', np.mean(blue)) # 72.8181
print('빨강 평균:', np.mean(red))  # 63.8181

# 선행조건 : 두 집단의 정규성 만족, 등분산 만족 여부.
# 정규성 검정
print('파랑 정규성 : ', stats.shapiro(blue).pvalue) # 파랑 정규성 :  0.51023100 > 0.05 만족
print('빨강 정규성 : ', stats.shapiro(red).pvalue) # 빨강 정규성 :  0.53479332 > 0.05 만족

# 등분산성 검정
print(stats.levene(blue, red).pvalue) # 0.4391644468 > 0.05 만족

# 독립표본 t검정
print(stats.ttest_ind(blue, red, equal_var=True))
# statistic=2.9280203225 pvalue=0.00831654571
# 해석:정규성, 등분산성 조건은 충족 / 
# pvalue=0.008316 < alpha 0.05이라 귀무가설 기각 
# 색에 따라 매출액의 평균에 차이가 있음. 파랑 > 빨강 (파랑이 좀 더 선호됨)
