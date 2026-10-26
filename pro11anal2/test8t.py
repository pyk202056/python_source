# 단일 모집단의 평균에 대한 가설검정(One Sample t-test)

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 실습예제1)
# A중학교 1학년 1반 학생들의 시험결과가 담긴 파일을 읽어 처리(국어점수 평균검정) student.csv
# 귀무 : 학생들의 국어 점수 평균은 80이다. (지금까지의 알려진 평균)
# 대립 : 학생들의 국어 점수 평균은 80이 아니다.

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/student.csv")
print(data.head(3))
print(data.describe())
print(data["국어"].mean())   # 72.9
print(len(data))   # 20      30행이 넘으면 '중심극한정리'에 의해 정규성을 따른다고 가정.
# 중심극한정리 : 표본의 크기(n)가 충분히 커지면 표본평균들의 분포가 정규분포에 가까워진다
# 일반적으로 표본의 크기가 n ≥ 30 이상이면 정규분포에 충분히 가까워진다고 본다.
# 30개가 넘지 않으므로 정규성 검정을 선행한다. 
# 수집한 데이터가 정규분포(Normal Distribution)를 따르는지 확인
# 샤피로-윌크 검정 (Shapiro-Wilk Test)으로 데이터가 정규분포를 가지는 지에 대해 확인.
# p값은 alpha 0.05 보다 커야 정규성을 따른다고 할 수 있다.
print(stats.shapiro(data["국어"]))  # alpha 0.05 > pvalue=0.0129597 정규성 만족 못함

# 정규성을 만족 못한 경우 대안 : Wilcoxon test
from scipy.stats import wilcoxon
wilcoxon_result = wilcoxon(data["국어"] - 80)
print('wilcoxon_result : ', wilcoxon_result) # statistic=74.0, pvalue=0.39777620658
# 해석 : alpha 0.05 < pvalue=0.397776 이므로 귀무가설 채택

# 정규성을 만족한 경우는 ttest_1samp() 수행
ttest_result = stats.ttest_1samp(data["국어"], popmean=80)
print('ttest_result : ', ttest_result) # statistic=-1.332180166, pvalue=0.1985605182
# 해석 : alpha 0.05 < pvalue=0.1985605 이므로 귀무가설 채택

# 결론 : 정규성은 부족하나 귀무가설 채택이라는 동일 결론을 얻음
# 만약 표본 수가 크다면 그냥 ttest_1samp을 써도 된다.
# 보고서 작성 시에는 "shapiro-wilk 검정 결과 정규성 가정이 다소 위배되었으나
# 비모수검정(wilcoxon) 결과도 동일하므로 ttest_1samp 결과를 신뢰할 수 있다" 라고 명시한다.

print("--------------")
# 실습예제2)
# 여아 신생아 몸무게의 평균검정 수행 babyboom.csv
# 여아 신생아의 몸무게는 평균이 2800(g)으로 알려져 왔으나 이보다 더 크다는 주장이 나왔다.
# 표본으로 여아 18명을 뽑아 체중을 측정하였다고 할 때 새로운 주장이 맞는지 검정해 보자.
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/babyboom.csv")
print(data2.head(3))
pd.set_option("display.max_columns", None)
print(data2.describe())
print()
fdata = data2[data2.gender == 1]   # 1:여아, 2:남아
print(fdata, ' ', len(fdata))   # 18
print("여아 신생아 몸무게 평균:", np.mean(fdata.weight))  # 3132.44
# 평균 2800과 3132는 평균에 차이가 있는가?  t-test로 검정
print("여아 신생아 몸무게 표준편차:", np.std(fdata.weight)) # 613.787

# One sample t-test
result2 = stats.ttest_1samp(fdata['weight'], popmean=2800)
print("result2 : ", result2)  # statistic=2.2331876, pvalue=0.0392684, df=17
# 해석1 (p값 사용) : 유의수준 0.05 > pvalue=0.0392684 이므로 귀무 기각
# 해석2 (t분포표 사용) : 
# t값:2.2331876, df:17, alpha:0.05, cv(임계값)? 1.740
# t값이 cv값 오른쪽(귀무 기각영역)에 있으므로 귀무 기각

print("t-test 선행 조건으로 정규성 확인 (n < 30) --------")
# 정규성 확인방법1 : shapiro test
print(stats.shapiro(fdata['weight'])) 
# pvalue=0.0179847 < 0.05 이므로 정규성을 만족하지 못함.

# 정규성 확인방법2 시각화 : histplot
sns.histplot(fdata['weight'], kde=True)    # 왜곡된 데이터 분포를 확인할 수 있다.
plt.show()

# 정규성 확인방법3 시각화 : Quantile-Quantile plot (Q-Q plot)
stats.probplot(fdata['weight'], plot=plt)  # Q-Q plot 상에서 잔차가 정규성을 만족 못함.
plt.show()

# 정규성 만족 못해 wilcoxon 검정
result3 = wilcoxon(fdata['weight'] - 2800)
print("result3 : ", result3) # statistic=37.0, pvalue=0.0342330
# 해석 : pvalue=0.0342330 < 0.05 이므로 귀무 기각.
