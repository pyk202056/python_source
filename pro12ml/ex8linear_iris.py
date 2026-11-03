# 단순선형회귀 - iris dataset 사용
# 상관관계가 약한 경우와 강한 경우로 회귀모델을 각가 생성 후 비교

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib. pyplot as plt

iris = sns.load_dataset('iris')
print(iris.head(3), type(iris))
print(iris.iloc[:, 0:4].corr())
#               sepal_length  sepal_width  petal_length  petal_width
# sepal_length      1.000000    -0.117570      0.871754     0.817941
# sepal_width      -0.117570     1.000000     -0.428440    -0.366126
# petal_length      0.871754    -0.428440      1.000000     0.962865
# petal_width       0.817941    -0.366126      0.962865     1.000000

print('\n연습1 : 상관관계가 약한 변수를 사용 : -0.117570')
result1 = smf.ols(formula='sepal_length ~ sepal_width', data=iris).fit()
print(result1.summary())
print('R squared : ', result1.rsquared)       # 0.0138226
print('P-value : ', result1.pvalues.iloc[1])  # 0.1518982 > 0.05 이 모델은 유의하지 모델

# 시각화
plt.scatter(iris.sepal_width, iris.sepal_length)
plt.plot(iris.sepal_width, result1.predict(), color='r')
plt.show()

print('\n연습2 : 상관관계가 강한 변수를 사용 : 0.871754')
result2 = smf.ols(formula='sepal_length ~ petal_length', data=iris).fit()
print(result2.summary())
print('R squared : ', result2.rsquared)       # 0.759954
print('P-value : ', result2.pvalues.iloc[1])  # 1.038667e-47 < 0.05 이 모델은 유의한 모델

# 시각화
# plt.scatter(iris.petal_length, iris.sepal_length)
# plt.plot(iris.petal_length, result2.predict(), color='b')
# plt.show()

sns.regplot(
    data=iris,
    x='petal_length',
    y='sepal_length',
    ci=None,   # 회귀직선 주변의 신뢰구간(Confidence Interval)을 표시X
    line_kws={'color': 'blue'}
)
plt.title(f'강한 상관관계 (R²={result2.rsquared:.3f})')
plt.show()

print('\n모델 예측값 확인')
print('실제값 : ', iris.sepal_length[:10].values.round(1))
print('예측값 : ', result2.predict()[:10].round(1))
# 실제값 :  [5.1 4.9 4.7 4.6 5.  5.4 4.6 5.  4.4 4.9]
# 예측값 :  [4.9 4.9 4.8 4.9 4.9 5.  4.9 4.9 4.9 4.9]

print('\n새로운 petal_length로 sepal_length를 예측')
new_data = pd.DataFrame({'petal_length':[1.1, 0.5, 6.0]})
y_pred = result2.predict(new_data)
print('예측된 꽃받침의 길이 : ', y_pred.values.round(5))  # [4.75642 4.51106 6.76014]
# 여기까지는 독립변수 1개 : 단순선형회귀

print('\n독립변수가 복수인 경우 - 다중선형회귀')
# result3 = smf.ols(formula='sepal_length ~ petal_length + petal_width', data=iris).fit()
column_select = "+".join(iris.columns.difference(['sepal_length','sepal_width', 'species']))
print(column_select)   # petal_length+petal_width
result3 = smf.ols(formula='sepal_length ~ ' + column_select, data=iris).fit()
print(result3.summary())
