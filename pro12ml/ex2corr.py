# 공분산 / 상관계수
# 표준편차는 개별 변수의 흩어짐을 나타내고, 
# 공분산은 두 변수의 공동 변화 방향을 나타내며, 
# 상관계수는 그 방향과 선형관계의 강도를 표준화한 값

# 평균·표준편차 확인 → 공분산 계산 → 상관계수 계산 → 변수 간 산점도 작성 → 상관관계 해석

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv")
print(data.head())
print(data.describe())

print('평균 / 표준편차')
print(np.mean(data.친밀도), ' ', np.std(data.친밀도))
print(np.mean(data.적절성), ' ', np.std(data.적절성))
print(np.mean(data.만족도), ' ', np.std(data.만족도))

# plt.hist([np.std(data.친밀도), np.std(data.적절성), np.std(data.만족도)])
# plt.show()

print('공분산 ---')
print(np.cov(data.친밀도, data.적절성))   # numpy 함수  0.416422  
print(np.cov(data.친밀도, data.만족도))   # 0.375663
print()
print(data.cov())  # pandas DataFrame 함수

print('상관계수 ---')
print(np.corrcoef(data.친밀도, data.적절성))  # numpy 함수  0.4992
print(np.corrcoef(data.친밀도, data.만족도))  # 0.4671
print()
print(data.corr())  # pandas DataFrame 함수
print(data.corr(method='pearson'))     # 변수 연속형, 정규성을 따름
# print(data.corr(method='spearman'))  # 변수 서열형, 정규성을 따르지 않
# print(data.corr(method='kendall'))

print('\n만족도에 따른 다른 특성 사이의 관계')
co_re = data.corr()
print(co_re['만족도'].sort_values(ascending=False))

# 시각화
data.plot(kind='scatter', x='만족도', y='적절성')
plt.show()
plt.close()

from pandas.plotting import scatter_matrix
attr = ['친밀도', '적절성', '만족도']
scatter_matrix(data[attr], figsize=(10, 6))
plt.show()
plt.close()

import seaborn as sns
sns.heatmap(data.corr(), annot=True)
plt.show()

# heatmap에 텍스트 표시 추가사항 적용해 보기  ---------------
corr = data.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)  # 상관계수값 표시
mask[np.triu_indices_from(mask)] = True
# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
fig, ax = plt.subplots()     # Set up the matplotlib figure

sns.heatmap(corr, mask=mask, vmin=-vmax, vmax=vmax, square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    ax.text(i + 0.5, len(corr) - (i + 0.5), corr.columns[i], ha="center", va="center", rotation=45)
    for j in range(i + 1, len(corr)):
        s = "{:.3f}".format(corr.values[i, j])
        ax.text(j + 0.5, len(corr) - (i + 0.5), s, ha="center", va="center")
ax.axis("off")
plt.show()