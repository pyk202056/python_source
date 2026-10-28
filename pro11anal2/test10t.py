# 독립 표본 t-검정( independent two sample t-test)
# 실습) 두 가지 교육방법에 따른 평균시험 점수에 대한 검정 수행 two_sample.csv

# 귀무 : 두 가지 교육방법에 따른 평균시험 점수에 차이가 없다.
# 대립 : 두 가지 교육방법에 따른 평균시험 점수에 차이가 있다.

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/two_sample.csv")
print(data.head(3))
# print(data.isnull().sum())
# print(data['score'].isnull().sum())   # 2
# print(data.isnull().any)

# 교육방법(method), 점수(score)만 분리
ms = data[['method', 'score']]
m1 = ms[ms['method'] == 1]   # 교육방법1
m2 = ms[ms['method'] == 2]   # 교육방법2
print(m1.head(3))
print(m2.head(3))

# 교육방법에서 score만 별도 기억
score1 = m1['score']
score2 = m2['score']
print(score1.isnull().sum())   # 0
print(score2.isnull().sum())   # 2

# NaN 처리? 삭제, 0 또는 평균으로 대체
# score2 = score2.fillna(0)   # NaN을 0으로 대체
score2 = score2.fillna(score2.mean())   # NaN을 평균으로 대체

# 선행 조건 : 두 집단의 정규성 만족 여부, 등분산 만족 여부.
# 정규성 검정
print('score1 정규성 : ', stats.shapiro(score1).pvalue)  # 0.3679911  만족
print('score2 정규성 : ', stats.shapiro(score2).pvalue)  # 0.6714233  만족

# 정규성 시각화 : histplot
import koreanize_matplotlib
plt.figure(figsize=(10, 5))
sns.histplot(score1, kde=True, color='red', alpha=0.5, label='교육방법1')
sns.histplot(score2, kde=True, color='blue', alpha=0.5, label='교육방법2')
plt.xlabel('시험점수')
plt.ylabel('빈도')
plt.legend()
plt.show()

# 정규성 시각화2 : Q-Q plot
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
#교육 방법1
stats.probplot(score1, dist='norm', plot=ax[0])  # dist='norm' : 비교기준은 정규분포
ax[0].set_title('교육방법1')
ax[0].set_xlabel('이론적 분위수')
ax[0].set_ylabel('표본 분위수')
ax[0].grid()
#교육 방법2
stats.probplot(score2, dist='norm', plot=ax[1])
ax[1].set_title('교육방법2')
ax[1].set_xlabel('이론적 분위수')
ax[1].set_ylabel('표본 분위수')
ax[1].grid()
plt.tight_layout()
plt.show()

# 등분산 만족 여부
from scipy.stats import levene
print('등분산 만족 여부 : ', levene(score1, score2).pvalue)  #  0.4568427  만족

result = stats.ttest_ind(score1, score2, equal_var=True)
print('result : ', result) # statistic=-0.19649386, pvalue=0.84505322
# 해석 : pvalue=0.84505322 > alpha 0.05 이므로 귀무가설 채택
# 두 가지 교육방법에 따른 평균시험 점수에 차이가 없다.
