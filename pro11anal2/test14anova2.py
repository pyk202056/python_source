# 일원분산분석(One-Way ANOVA)으로 그룹 간 평균 차이 검정

# 서초구에 있는 GS 편의점 3개 지역(서초동, 반포동, 양재동)에 근무하는 알바생의 급여에 대한 평균 차이 검정

# 귀무 : GS 편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 없다.
# 대립 : GS 편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 있다.

import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.formula.api import ols 
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import koreanize_matplotlib
import urllib.request

uri = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3.txt"
# 읽기 1
# data = pd.read_csv(uri, header=None)
# print(data.values)

# 읽기 2
data = np.genfromtxt(urllib.request.urlopen(uri), delimiter=",")
# print(data)    # [[243.   1.] ... ]
print(data.shape)  # (22, 2)

# 세 개의 그룹에 월급 자료 얻기 - 평균
gr1 = data[data[:, 1] == 1, 0]
gr2 = data[data[:, 1] == 2, 0]
gr3 = data[data[:, 1] == 3, 0]
print(gr1, ' ', np.mean(gr1))   # 316.625
print(gr2, ' ', np.mean(gr2))   # 256.4444
print(gr3, ' ', np.mean(gr3))   # 278.0

print()
# 정규성 확인
print(stats.shapiro(gr1).pvalue)  # 0.33368 > 0.05 만족
print(stats.shapiro(gr2).pvalue)  # 0.65610
print(stats.shapiro(gr3).pvalue)  # 0.83248
# 정규성을 위반하고 표본도 작다면, 분포 형태에 의존하지 않는 비모수 검정을 사용.
# One-way ANOVA의 대안 - 크루스칼-왈리스 검정 (Kruskal-Wallis test)
# stats.kruskal(gr1, gr2, gr3)

print()
# 등분산성 확인
print(stats.levene(gr1, gr2, gr3).pvalue)    # 0.045846
print(stats.bartlett(gr1, gr2, gr3).pvalue)  # 0.350803
# ANOVA에서 등분산성을 만족하지 못한 경우 ---
# Welch's ANOVA (웰치 분산분석): 보편적으로 사용하는 대안.
# 데이터 변환 : 원래 데이터의 변화하는 방법도 있다. (로그 변환, 제곱근 변환, 표준화 ...)

# 일원분산분석 방법1 : anova_lm()
df = pd.DataFrame(data=data, columns=['pay','group'])
# print(df)
lmodel = ols('pay ~ C(group)', data=df).fit()   # C(group) : group은 범주형임을 명시적으로 표현
print(anova_lm(lmodel, type=1))
#             df        sum_sq      mean_sq         F    PR(>F)
# C(group)   2.0  15515.766414  7757.883207  3.711336  0.043589
# 해석 : p 0.043589 < alpha 0.05 이므로 귀무 기각

# 일원분산분석 방법2 : f_oneway()
f_stat, pv = stats.f_oneway(gr1, gr2, gr3)
print('f_stat : ', f_stat)   # 3.711335
print('p_value : ', pv)      # 0.043589
# GS 편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 있다. 얼마나?

print()
# 서초동, 반포동, 양재동 지역 간 평균 차이가 궁금하면? 사후 검정
df ['region'] = df['group'].map({1:'서초동',2:'반포동',3:'양재동'})  # 지역명 추가
print(df)

from statsmodels.stats.multicomp import pairwise_tukeyhsd
# tukResult = pairwise_tukeyhsd(endog=df.pay, groups=df.group)
tukResult = pairwise_tukeyhsd(endog=df.pay, groups=df.region)  # df['region']
print(tukResult)

# 시각화
tukResult.plot_simultaneous(xlabel='급여 평균', ylabel='지역')
plt.show()
