# 과적합(Overfitting)
# 선형 회귀 모델이 훈련 데이터(Training Data)에 너무 과하게 학습되어, 
# 데이터에 포함된 노이즈(잡음)나 지엽적인 특성까지 암기해 버리는 현상.
# 훈련 데이터에 대한 예측 오차는 매우 낮지만, 처음 보는 테스트 데이터(Test Data)나 
# 새로운 데이터가 들어왔을 때 예측 성능(일반화 능력)이 크게 떨어진다.

# Linear Regression에서 과적합을 해결하는 방법
# 특성(Feature) 줄이기, 정규화(Regularization) 적용, Train/Test split, 더 많은 데이터 수집하기 ...

# 이 중에서 정규화(Regularization) 적용하기로 실습 진행 ----
# 회귀계수 값이 너무 커지지 않도록 비용 함수(Cost Function)에 페널티를 부과(규제)
# Ridge (L2 규제): 가중치들의 제곱합을 최소화하여 계수들을 0에 가깝게 작게 만든다.
# Lasso (L1 규제): 가중치들의 절대값 합을 최소화하며, 중요하지 않은 특성의 계수를 아예 0으로 만들어 제거.
# ElasticNet (Ridge + Lasso)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

iris = load_iris()
# print(iris)
print(iris.keys())  # ['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module']

pd.set_option('display.max_columns', None)

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df['target_names'] = iris.target_names[iris.target]
print(iris_df.head(2))
# sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)   target target_names 
# 0            5.1               3.5                1.4               0.2     0     setosa
# 1            4.9               3.0                1.4               0.2     0     setosa
print(iris_df.shape)   # (150, 6)

# train(학습) / test(검증) 데이터로 분리  -  7 : 3
train_set, test_set = train_test_split(iris_df, test_size=0.3, random_state=12, shuffle=True)
print(train_set.shape, test_set.shape)   # (105, 6) (45, 6)
# print(train_set.head(3))
# print(test_set.head(3))

print(train_set.iloc[:, [2]])   # petal length (cm),  독립변수
print(train_set.iloc[:, [3]])   # petal width (cm)  종속변수

# 회귀분석 방법1 - LinearRegression
# 학습은 train dataset 사용
model_linear = LinearRegression().fit(
                    X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])
print('slope : ', model_linear.coef_)      # [[0.42259168]]
print('bias : ', model_linear.intercept_)  # [-0.39917733]

# 모델 평가는 test dataset으로 작업
pred = model_linear.predict(test_set.iloc[:, [2]])
print('예측값 : ', np.round(pred[:5].flatten(), 1))
print('실제값 : ', test_set.iloc[:, [3]][:5].values.flatten())
# 예측값 :  [0.2 1.7 0.2 1.3 2.1]
# 실제값 :  [0.3 1.9 0.2 1.3 2.3]

print(f'r2_score(결정계수) : {r2_score(test_set.iloc[:, [3]], pred)}')  # 0.93833219
# 시각화
plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]], color='red')
plt.plot(np.array(test_set.iloc[:, [2]]), 
        model_linear.predict(test_set.iloc[:, [2]]))
plt.show()

print('\nRidge -----------')
# 회귀분석 방법 - Ridge: alpha값을 조정(가중치 제곱합을 최소화)하여 과대/과소적합을 피한다. 다중공선성 문제 처리에 효과적.
from sklearn.linear_model import Ridge
model_ridge = Ridge(alpha=10).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_ridge.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]]))  # 0.91880
print(model_ridge.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))    # 0.94101
pred_ridge = model_ridge.predict(test_set.iloc[:, [2]])
print('ridge predict : ', pred_ridge[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_ridge)))  # 0.9410

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='blue')
plt.plot(np.array(test_set.iloc[:, [2]]), model_ridge.predict(test_set.iloc[:, [2]]))
plt.show()

print('\nLasso -----------')
# 회귀분석 방법 - Lasso: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
from sklearn.linear_model import Lasso
model_lasso = Lasso(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_lasso.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
print(model_lasso.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
pred_lasso = model_lasso.predict(test_set.iloc[:, [2]])
print('lasso predict : ', pred_lasso[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_lasso)))

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='green')
plt.plot(np.array(test_set.iloc[:, [2]]), model_lasso.predict(test_set.iloc[:, [2]]))
plt.show()

# 회귀분석 방법 4 - Elastic Net 회귀모형 : Ridge + Lasso의 형태로 가중치 절대값의 합(L1)과 제곱합(L2)을 동시에 제약 조건으로 가지는 모형
print('\nElasticNet -----------')
# 회귀분석 방법 - ElasticNet: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
from sklearn.linear_model import ElasticNet
model_elastic = ElasticNet(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

# 점수
print(model_elastic.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
print(model_elastic.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
pred_elastic = model_elastic.predict(test_set.iloc[:, [2]])
print('ElasticNet predict : ', pred_elastic[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_elastic)))

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='cyan')
plt.plot(np.array(test_set.iloc[:, [2]]), model_elastic.predict(test_set.iloc[:, [2]]))
plt.show()










# 다중선형회귀 - Iris 4개 특성을 독립변수로 사용
# LinearRegression, Ridge(L2), Lasso(L1), ElasticNet(L1+L2) 비교
# 주의 : target은 범주형이므로 회귀 알고리즘 비교를 위한 교육용 예제임

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, r2_score

# 1. Iris 데이터 준비
iris = load_iris()

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df['target_names'] = iris.target_names[iris.target]

print(iris_df.head(3))
print(iris_df.shape)  # (150, 6)

x = iris_df.iloc[:, 0:4]    # 독립변수 : sepal, petal 관련 4개 특성
y = iris_df['target']      # 종속변수 : 품종 번호 (0, 1, 2)
print(x.head(3))
print(y.head(3))

# 2. 학습 / 테스트 데이터 분리
x_train, x_test, y_train, y_test = train_test_split( x, y, test_size=0.3, random_state=12)
print('x_train :', x_train.shape)  # (105, 4)
print('x_test :', x_test.shape)    # (45, 4)

print('\nLinearRegression -----------')
model_linear = LinearRegression()
model_linear.fit(x_train, y_train)
pred_linear = model_linear.predict(x_test)
print('기울기(회귀계수) :', model_linear.coef_)

print('절편 :', model_linear.intercept_)
print('예측값 :', np.round(pred_linear[:5], 3))
print('실제값 :', y_test.iloc[:5].values)

print('Train R2 :', model_linear.score(x_train, y_train))
print('Test R2 :', model_linear.score(x_test, y_test))
print('MSE :', mean_squared_error(y_test, pred_linear))

print('\nRidge ---- L2 규제-------')
model_ridge = Ridge(alpha=10)
model_ridge.fit(x_train, y_train)
pred_ridge = model_ridge.predict(x_test)

print('기울기(회귀계수) :', model_ridge.coef_)
print('절편 :', model_ridge.intercept_)
print('예측값 :', np.round(pred_ridge[:5], 3))

print('Train R2 :', model_ridge.score(x_train, y_train))
print('Test R2 :', model_ridge.score(x_test, y_test))
print('MSE :', mean_squared_error(y_test, pred_ridge))

print('\nLasso ----L1 규제-------')
model_lasso = Lasso(alpha=0.1)
model_lasso.fit(x_train, y_train)
pred_lasso = model_lasso.predict(x_test)

print('기울기(회귀계수) :', model_lasso.coef_)
print('절편 :', model_lasso.intercept_)
print('예측값 :', np.round(pred_lasso[:5], 3))

print('Train R2 :', model_lasso.score(x_train, y_train))
print('Test R2 :', model_lasso.score(x_test, y_test))
print('MSE :', mean_squared_error(y_test, pred_lasso))

print('\nElasticNet ----L1 + L2 규제-------')
model_elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
model_elastic.fit(x_train, y_train)
pred_elastic = model_elastic.predict(x_test)

print('기울기(회귀계수) :', model_elastic.coef_)
print('절편 :', model_elastic.intercept_)
print('예측값 :', np.round(pred_elastic[:5], 3))

print('Train R2 :', model_elastic.score(x_train, y_train))
print('Test R2 :', model_elastic.score(x_test, y_test))
print('MSE :', mean_squared_error(y_test, pred_elastic))

print('\n모델 성능 비교 -----------')
models = {
    'LinearRegression': model_linear,
    'Ridge': model_ridge,
    'Lasso': model_lasso,
    'ElasticNet': model_elastic
}

result_list = []
for name, model in models.items():
    pred = model.predict(x_test)
    result_list.append({
        '모델': name,
        'Train R2': model.score(x_train, y_train),
        'Test R2': r2_score(y_test, pred),
        'MSE': mean_squared_error(y_test, pred)
    })

result_df = pd.DataFrame(result_list)
print(result_df.round(4))


# 8. 모델별 회귀계수 비교
print('\n모델별 회귀계수 비교 -----------')
coef_df = pd.DataFrame({
    '독립변수': x.columns,
    'LinearRegression': model_linear.coef_,
    'Ridge': model_ridge.coef_,
    'Lasso': model_lasso.coef_,
    'ElasticNet': model_elastic.coef_
})
print(coef_df.round(4))

# 9. 실제값과 예측값 비교 그래프
plt.figure(figsize=(9, 5))
for name, model in models.items():
    pred = model.predict(x_test)
    plt.scatter(y_test, pred, alpha=0.5, label=name)

plt.plot([0, 2], [0, 2], 'k--', label='실제값 = 예측값')
plt.xlabel('실제값(target)')
plt.ylabel('예측값')
plt.title('회귀모델별 실제값과 예측값 비교')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# 10. 회귀계수 비교 그래프
coef_df.set_index('독립변수').plot(kind='bar', figsize=(10, 5))
plt.title('모델별 회귀계수 비교')
plt.ylabel('회귀계수')
plt.xticks(rotation=15)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()