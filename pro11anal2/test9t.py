# 독립 표본 t-검정( independent two sample t-test )
# 서로 다른 두 집단의 평균에 대한 통계 검정에 사용된다.
# 비교를 위해 평균과 표준편차 통계량을 사용한다.
# 두 집단의 평균과 표준편차 비율에 대한 대조 검정법이다.

# 서로 독립인 두 집단의 평균차이 검정
# 남녀의 성적, A반과 B반의 키,경기도와 충청도의 소득따위의 서로 독립인 
# 두 집단에서 얻은 표본을 독립표본(twosample)이라고 한다.

# 선행 조건 : 두 집단이 정규분포를 따르고, 분산이 동일하다(등분산)는 가정이 필요하다.

# 실습1) 남녀 두 집단 간 파이썬 시험의 평균차이 검정
# 남녀의 시험 평균이 우연히 같을 확률은 얼마일까?
# 만약 우연히 발생했다면 평균은 같을 것이고, 우연이 아니면 평균은 다른 것이다.
# 95% 신뢰 구간에서 우연히 발생할 확률이 5% 이상이면 귀무가설 채택이다.

# 귀무 : 남녀 두 집단 간 파이썬 시험의 평균의 차이는 없다.
# 대립 : 남녀 두 집단 간 파이썬 시험의 평균의 차이는 있다.
# 독립변수(x) : 남녀 두 집단(범주형), 종속변수(y) : 시험 평균 점수(연속형)

from scipy import stats
import pandas as pd
import numpy as np

male = [75, 85, 100, 72.5, 86.5]
female = [63.2, 76, 52, 100, 70]
print(np.mean(male), ' ', np.mean(female))   # 83.8   72.24

# 두 개의 집단에 대한 표본 자료이므로 '독립표본 t-검정' 수행
# two_sample = stats.ttest_ind(male, female)
two_sample = stats.ttest_ind(male, female, equal_var=True)  # 위와 동일. 두 집단의 분산이 같다고 가정
# print(two_sample)
tv, pv = two_sample
print('t 검정 통계량 : ', tv)  # 1.233193127514512
print('p 값 : ', pv)          # p 값 :  0.2525076844853276
# 해석 : p값 0.252507 > 알파 0.05 이므로 귀무가설 채택. 통계적으로 유의하지 않다.

print("------")
# 선행 조건 1) 두 집단이 각각 정규분포를 따라야 한다.
print('male의 정규성 : ', stats.shapiro(male))      # p:0.6003714036
print('female의 정규성 : ', stats.shapiro(female))  # p:0.7780431096
# p-value가 모두 0.05보다 크므로 정규성을 만족.
# 만약 표본 데이터 수가 많다면 정규성 검정을 하지 않아도 된다. (중심극한의 원리 때문)
# 만약 정규성을 만족하지 못하면 비모수 검정인 Mann-whitney test를 한다.
# 데이터가 정규분포를 따르지 않거나, 표본크기가 작을 때 사용하는 독립 표본 t-검정의 대표적인 대안.
# stats.mannwhitneyu(group1, group2)  

print()
# 선행 조건 2) 두 집단의 분산이 같다는 가정이 필요. 등분산성(데이터의 퍼짐 정도)
from scipy.stats import levene, bartlett
# levene : 정규성과 상관없이 사용. 이상치에 민감, 어떤 분포도 사용이 가능.
# bartlett : 정규성이 있을 때만 사용. 이상치에 덜민감, 정규분포일 때만 사용이 가능.
leven_stat, leven_p = levene(male, female)
print('p-value : ', leven_p)   # 0.49565116069 > 0.05 등분산성 만족

# 등분산성이 만족되므로 아래 명령 사용
# two_sample = stats.ttest_ind(male, female, equal_var=True)

# 등분산성이 만족되지 않을 경우에는 아래 명령 사용 (Welch's t-test)
# two_sample = stats.ttest_ind(male, female, equal_var=False)
