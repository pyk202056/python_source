# 집단 간 차이분석 : 평균 또는 비율 차이를 분석
# :모집단에서 추출한 표본정보를 이용하여 모집단의 다양한 특성을 과학적으로 추론할 수 있다

# 단일 표본 t검정(One-sample t-test)
# 정규분포의 표본에 대한 기대값을 조사하는 검정방법이다.
# 예상평균값과 표본 자료 간에 평균의 차이를 검정
# 독립변수:범주형, 종속변수:연속형
# 하나의 집단에 대한 표본 평균이 예측된 평균(모집단)과 같은지 여부를 확인

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 실습1 : 에이콘 교육센터 2층의 교육생 : 과거 5년 간 남성 집단의 평균 키 검정
# 귀무 : 해당 집단의 평균 키가 177이다. (모수)
# 대립 : 해당 집단의 평균 키가 177이 아니다  (양측 검정)
# 대립 : 해당 집단의 평균 키가 177보다 크다  (단측 검정)
one_sample = [167.0, 182.7, 169.7, 176.8, 180.0]
print(np.array(one_sample).mean())   # 175.24인 경우 177.0과 차이가 있는가? 검정

# 단일표본 t-검정(One-Sample t-test)
# 하나의 표본집단 평균이 특정기준값(모집단의 가설평균)과 통계적으로 유의한 차이가 있는지 검정
result = stats.ttest_1samp(one_sample, popmean=177.0)  # (데이터, 모수의평균값)
print(result)
# statistic=-0.58775, pvalue=0.5882740, df=4
# 해석 : 유의수준 0.05 < pvalue=0.5882740 이므로 귀무가설 채택

print()
result2 = stats.ttest_1samp(one_sample, popmean=165.0)  # 모수의평균값:160.0
print(result2)
# statistic=3.4196846, pvalue=0.026787, df=4
# 해석 : 유의수준 0.05 > pvalue=0.026787 이므로 귀무가설 기각

sns.displot(one_sample, bins=10, kde=False, color='skyblue', edgecolor='black')
plt.axvline(np.mean(one_sample), color='green', linestyle='-', label='표본평균')
plt.axvline(177, color='red', linestyle='--', label='가설평균 177cm')
plt.title("교육생 키 분포")
plt.xlabel("키(cm)")
plt.ylabel("빈도(명)")
plt.legend()
plt.show()
