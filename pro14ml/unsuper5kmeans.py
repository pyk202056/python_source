# 비계층적 군집 분석 : 학생 10명의 시험점수 사용

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans

students = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10']
scores = np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1, 1)
print('점수 : ', scores)

# k = 3
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
km_clusters = kmeans.fit_predict(scores)
print(km_clusters)   # [2 0 1 2 1 0 1 0 2 2]

df = pd.DataFrame({
    'student':students,
    'score':scores.ravel(),
    'cluster':km_clusters
})
print(df)

print('\n군집별 평균 점수')
groupd = df.groupby('cluster')['score'].mean()
print('군집별 평균 : ', groupd)

# 시각화
x_position = np.arange(len(students))
y_scores = scores.ravel()
colors = {0:'red',1:'blue',2:'green'}
plt.figure(figsize=(10, 6))

# 학생별 군집을 색으로 구분래 산점도
for i, (x, y, cluster) in enumerate(zip(x_position, y_scores, km_clusters)):
    plt.scatter(x, y, color=colors[cluster], s=100)
    plt.text(x, y + 1.5, students[i], fontsize=10, ha='center')

# 중심점
centers = kmeans.cluster_centers_
for center in centers:
    plt.scatter(len(students) // 2, center[0], marker='X', c='black', s=200)

plt.xticks(x_position, students)
plt.xlabel('학생명')
plt.ylabel('점수')
plt.grid()
plt.show()
