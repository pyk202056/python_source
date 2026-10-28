# 어느 음식점의 매출과 날씨 자료를 이용해 온도에 따른 매출액 평균의 차이 검정 -------------------------

# 세 집단 : 추움, 보통, 더움

# 매출 데이터 : tsales.csv
# 날씨 데이터 : tweather.csv

# 귀무 : 온도에 따라 매출액의 평균에 차이가 없다.
# 대립 : 온도에 따라 매출액의 평균에 차이가 있다.

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

pd.set_option('display.max_columns', None)

# 매출 데이터 읽기
sales_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv", dtype={'YMD':'object'})  # int -> object로 변환해 읽기
print(sales_data.head(2))
print(sales_data.info())   # 328 * 3

# 날씨 데이터 읽기
wt_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv")
print(wt_data.head(2))
print(wt_data.info())      # 702 * 9

print()
# sales_data : YMD 20190514,  wt_data : tm 2018-06-01 이므로 병합을 위해 변환 필요
wt_data.tm = wt_data.tm.map(lambda x:x.replace("-", ""))
print(wt_data.head(2))
#    stnId        tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  20180601   23.8   17.5   30.2    0.0    4.3    1.9    0.0

print()
# 두 데이터 병합
frame = sales_data.merge(wt_data, how='left', left_on='YMD', right_on='tm')
print(frame.columns) 
# ['YMD', 'AMT', 'CNT', 'stnId', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn','maxWs', 'avgWs', 'ddMes']
print(frame.head(3), ' ', len(frame))   # 328

data = frame.iloc[:,  [0, 1, 7, 8]]  # YMD  AMT  maxTa  sumRn
print(data.head())
print('결측치 확인 : ', data.isnull().sum())

# plt.boxplot(data.maxTa)
# plt.show()
# print(data['maxTa'].describe())  # min:-4.90, mean:18.59, max:36.80

# 온도를 세 그룹으로 분리 (연속형 -> 범주형)
data['ta_gubun'] = pd.cut(data['maxTa'], bins=[-5, 8, 24, 37], labels=[0, 1, 2])
print(data.head(3), ' ', data['ta_gubun'].unique())
# 요인1개(온도) : 그룹3개(0,1,2)

# 정규성 / 등분산성 확인
x1 = np.array(data[data['ta_gubun']==0].AMT)  # 추움 그룹 매출액
x2 = np.array(data[data['ta_gubun']==1].AMT)  # 보통 그룹 매출액
x3 = np.array(data[data['ta_gubun']==2].AMT)  # 더움 그룹 매출액
print(x1[:5])  # [1050500  770000 1054500  969000 1061500]

print()
print(stats.shapiro(x1).pvalue)   # 0.24819  > 0.05 정규성 만족
print(stats.shapiro(x2).pvalue)   # 0.03882  < 0.05 정규성 만족 X
print(stats.shapiro(x3).pvalue)   # 0.31829  > 0.05 정규성 만족

print(stats.levene(x1, x2, x3).pvalue)  # 0.0390023 < 0.05 등분산성 만족X

print("\n온도별 매출액 평균")
# Pandas 지수 표기법 해제
pd.set_option('display.float_format', '{:,.2f}'.format)

spp = data.loc[:, ['AMT', 'ta_gubun']]
print(spp.groupby('ta_gubun').mean())
print(f'{np.mean(x1):.2f}')  # 1032362.32
print(f'{np.mean(x2):.2f}')  # 818106.87
print(f'{np.mean(x3):.2f}')  # 553710.94

group1, group2, group3 = x1, x2, x3
print(stats.f_oneway(group1, group2, group3))
# F_onewayResult : statistic=99.190801, pvalue=2.36073710e-34
# 해석 : pvalue=2.36073710e-34 < alpha 0.05 이므로 귀무 기각
# 해당 음식점은 온도에 따라 매출액의 평균에 차이가 있다.라는 의견을 수렴한다.

print()
# 정규성 깨지면 stats.kruskal() 사용, 등분산성이 깨지면 welch's ANOVA
# Kruskal-Wallis 검정
print(stats.kruskal(group1, group2, group3))

print()
# welch's ANOVA 검정 - 등분산 가정 불필요
print(stats.f_oneway(group1, group2, group3, equal_var=False))

print()
# 참고 : 검정 방법을 제공하는 라이브러리는 다양하다.
# 예를 들어 다른 라이브러리로 welch's ANOVA 검정 수행
# pip install pingouin
from pingouin import welch_anova
print(welch_anova(dv = 'AMT', between='ta_gubun', data=data))

print("\n사후 검정")
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog=spp['AMT'], groups=spp['ta_gubun'])
print(tukResult)

# 시각화
tukResult.plot_simultaneous(xlabel='매출액 평균', ylabel='온도 분류')
plt.show()
