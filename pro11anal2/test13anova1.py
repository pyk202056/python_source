# 분산분석 (ANOVA, ANalysis Of Variance)
# : 세 개 이상의 모집단에 대한 가설검정 
# : 분산이 발생한 과정을 분석하여 요인에 의한 분산과 
# 요인을 통해 나누어진 각 집단 내의 분산으로 나누고 요인에 의한 분산이 
# 의미 있는 크기를 가지는지를 검정하는 것을 의미한다.
# 세 집단 이상의 평균비교에서는 독립인 두 집단의 평균 비교를 반복하여 
# 실시할 경우에 제1종 오류가 증가하게 되어 문제가 발생한다.
# 이를 해결하기 위해 Fisher가 개발한 분산분석을 이용하게 된다.
# 분산이 발생한 과정을 분석하여 요인에 의한 분산과 요인을 통해 나눠진 각 집단내의 
# 분산으로 나누고, 요인에 의한 분산이 의미 있는 크기를 가지는지를 검정한다.

# 분산분석은 3개 이상의 그룹 간 평균에 유의미한 차이가 있는지를 분산을 이용해 검정하는 통계적 방법
# f값 = 집단간분산 / 집단내분산

# 서로 독립인 세 집단의 평균차이 검정
# 실습) 세 가지 교육방법을 적용하여 1개월 동안 교육받은 교육생 80명을 대상으로 
# 실기시험을 실시.   three_sample.csv
# 독립변수(범주형) : 요인은 한 개(교육방법) - 방법의 종류가 3가지(그룹이 세 개)
# 종속변수(연속형) : 실기시험 평균 점수

# 귀무(영 가설)  : 세 가지 교육방법에 따른 실기시험 평균 점수에 차이가 없다.
# 대립(연구가설) : 세 가지 교육방법에 따른 실기시험 평균 점수에 차이가 있다.

import pandas as pd
import scipy.stats as stats
from statsmodels.formula.api import ols   # 추정 및 검정, 회귀, 시계열 분석 등의 기능 제공
# ols (Ordinary Least Squares - 최소제곱법 회귀)

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/three_sample.csv")
print(data.head(3), ' ', len(data))  # 80
print(data.describe())

# 이상치(outlier) 시각화
# import matplotlib.pyplot as plt
# plt.boxplot(data.score)
# plt.show()

# 이상치 값과 갯수 확인 - IQR 이용 --------------
q1 = data['score'].quantile(0.25)
q3 = data['score'].quantile(0.75)
iqr = q3 - q1
# 이상치 기준
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
print(f"Q1:{q1}, Q3:{q3}, IQR:{iqr}")
print("이상치 하한 값 : ", lower)  # 25.75
print("이상치 상한 값 : ", upper)  # 111.75
outlier = data[(data['score'] < lower) | (data['score'] > upper)]
print('outlier : ', outlier)
# outlier :      no  method  survey  score
#            7    8       2       1    500
#            59  60       1       0    438
print('outlier 갯수 : ', len(outlier))  # 2
# ----------------------------------------------
data = data.query("score <= 100")   # 시험 점수이므로 100점 이내의 값만 작업에 참여
print(len(data))   # 78
print(data.describe())

# 교육 방법별 만족 건수 - 교차표 -----------
ctab = pd.crosstab(data['method'], data['survey'])
ctab.index = ['방법1','방법2','방법3']
ctab.columns = ['만족','불만족']
print(ctab)
# -------------------------

print('ANOVA 검정')
# F통계값을 얻기 위해 회귀분석모델 사용
import statsmodels.api as sm
lin_model = ols("data['score'] ~ data['method']", data=data).fit()  # 회귀분석모델 객체 생성
result = sm.stats.anova_lm(lin_model, type=1) 
pd.set_option('display.max_columns', None)
print(result)
#             df(자유도) sum_sq(제곱합) mean_sq(제곱평균)  F(F값) PR(>F)(p값)
# data['method']   1.0     27.980888    27.980888(MSR)  0.122228  0.727597
# Residual        76.0  17398.134497   228.922822(MSE)     NaN       NaN
# F 검정통계량 : 0.122228    p-value : 0.727597
# 판정 : p-value : 0.727597 > alpha : 0.05 이므로 귀무 채택
# 세 가지 교육방법에 따른 실기시험 평균 점수에 차이가 없다.

f_value = result.loc["data['method']", "F"]
p_value = result.loc["data['method']", "PR(>F)"]
print('f_value : ', f_value)  # 0.122228476
print('p_value : ', p_value)  # 0.727596911

print("\n교육방법별 평균 점수 : \n")
print(data.groupby('method')['score'].mean())
# method
# 1    67.384615
# 2    68.357143
# 3    68.875000

# ANOVA는 각 method별 1:1 평균비교는 알려 주지 않는다.
# 이 때 사후분석을 이용하면 어느 그룹과의 평균값이 의미가 있는지 없는지를 알 수 있다.
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukResult = pairwise_tukeyhsd(endog=data['score'], groups=data['method'])
print(tukResult)
# Multiple Comparison of Means - Tukey HSD, FWER=0.05 
# ====================================================
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#      1      2   0.9725 0.9702 -8.9458 10.8909  False : 유의미한 차이가 없으면 False
#      1      3   1.4904 0.9363 -8.8183  11.799  False : 유의미한 차이가 없으면 True
#      2      3   0.5179 0.9918 -9.6125 10.6483  False

# tukeyhsd 시각화
import matplotlib.pyplot as plt
tukResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()
# Tukey HSD : 원래 반복 수가 동일하다는 가정하에 고안된 방법
# 집단 간 평 균 차이를 정밀하게 확인 가능
# 각 집단의 표본 수의 차이가 크면 결과의 신뢰가 떨어짐
