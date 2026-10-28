# 어느 음식점의 매출과 날씨 자료를 이용해 강수 여부에 따른 매출액 평균의 차이 검정 -------------------------
# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여 
# 강수 여부에 따른 매출액의 평균에 차이가 있는지 검정.
# 두 집단 : 강수량이 있을 때, 맑을 때

# 매출 데이터 : tsales.csv
# 날씨 데이터 : tweather.csv

# 귀무 : 강수 여부에 따라 매출액의 평균에 차이가 없다.
# 대립 : 강수 여부에 따라 매출액의 평균에 차이가 있다.

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

# 독립표본 t검정
# print(data['sumRn'] > 0)   # 강수량이 있으면 True

# 칼럼 추가 : rain_yn <-- 강수량이 있으면 1, 없으면 0
# data['rain_yn'] = (data['sumRn'] > 0).astype(int)    # 방법1
# print(True * 1, ' ', False * 1)   # 1   0
data['rain_yn'] = (data.loc[:, ('sumRn')] > 0) * 1     # 방법2
print(data.head())
#         YMD     AMT  maxTa  sumRn  rain_yn
# 0  20190514       0   26.9    0.0        0

# 데이터 분포 box plot으로 시각화
sp = np.array(data.iloc[:, [1, 4]])   # AMT, rain_yn
print(sp)
# [[      0       0]     # 0번째 열 AMT, 1번째 열 rain_yn
#  [  18000       1] ...
tg1 = sp[sp[:, 1] == 0, 0]   # 집단1 : 강수 없을 때 매출액
tg2 = sp[sp[:, 1] == 1, 0]   # 집단2 : 강수 있을 때 매출액
print(tg1[:3])   # [     0  50000 125000]
print(tg2[:3])   # [ 18000 274000 318000]
print('tg1 : 강수 없을 때 매출액 평균 : ', np.mean(tg1))  # 761040.25
print('tg2 : 강수 있을 때 매출액 평균 : ', np.mean(tg2))  # 757331.52

plt.boxplot([tg1, tg2], meanline=True, showmeans=True, notch=True)
plt.show()

# 정규성 검정
print(len(tg1), ' ', len(tg2))   # 236   92
print(stats.shapiro(tg1).pvalue) # 0.05605063   만족
print(stats.shapiro(tg2).pvalue) # 0.88275031

# 등분산성 검정
print(stats.levene(tg1, tg2).pvalue)  # 0.71234523 만족

# 독립 표본 t검정
print(stats.ttest_ind(tg1, tg2, equal_var=True))
# statistic=0.101098286, pvalue=0.91953458
# 해석 : 정규성, 등분산성 조건은 충족함.
# pvalue=0.91953458 > alpha 0.05 이므로 귀무가설 채택
# 강수 여부에 따라 매출액의 평균에 차이가 없다.라는 생각이 유지됨.
