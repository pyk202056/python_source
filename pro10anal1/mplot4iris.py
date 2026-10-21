# iris dataset : 150행, 꽃 종류 : 3가지, 4개의 특성(꽃받침, 꽃잎의 너비와 길이)

import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

iris_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/iris.csv")
print(iris_data.info())
print(iris_data.head(3))
print(iris_data.tail(3))

# 산점도 차트
plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'])
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃잎 길이')
plt.title('붓꽃 자료')
plt.show()

# 꽃의 종류에 따라 다른색(3가지)으로 출력
print()
print(iris_data['Species'].unique())  # ['setosa', 'versicolor', 'virginica']

cols = []
for s in iris_data['Species']:
    choice = 0
    if s == 'setosa':choice=1
    elif s == 'versicolor':choice=2
    elif s == 'virginica':choice=3
    cols.append(choice)

plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'], c=cols)
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃잎 길이')
plt.title('붓꽃 자료')
plt.show()

# pandas의 시각화 기능
from pandas.plotting import scatter_matrix
iris_col = iris_data.loc[:, 'Sepal.Length':'Petal.Length']
scatter_matrix(iris_col, diagonal='kde')  
# 커널밀도 추정(kde) : 데이터의 분포를 부드러운 곡선으로 추정하는 방법
plt.show()

# seaborn
import seaborn as sns
sns.pairplot(iris_data, hue='Species', height=2)
plt.show()
