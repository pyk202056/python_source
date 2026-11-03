# 다항회귀분석 문제 : Servo Dataset (UCI)
# 제어 시스템(Servo System)의 응답 시간(Response Time) 예측
#
# 독립변수(X) : pgain, vgain
# 종속변수(Y) : class (응답 시간)
#
# 1차 선형회귀와 2차 다항회귀 비교
# 학습/테스트 분할(8:2) → 표준화 → 다항 특성 생성
# → 모델 학습 → 성능 평가 → 2차원 시각화(차트 1개)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

pd.set_option('display.max_columns', None)

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/servo/servo.data"

df = pd.read_csv(url, header=None)
df.columns = ['motor', 'screw', 'pgain', 'vgain', 'class']

print('데이터 확인 ---')
print(df.head(3))
print('데이터 크기 :', df.shape)  # (167, 5)

print('\n상관계수 ---')
print(df[['pgain', 'vgain', 'class']].corr())

# 2. 독립변수 / 종속변수
x = df[['pgain', 'vgain']].astype(float)
y = df['class'].values
print(x.head(3))
print(y[:3])

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

print('\n학습 / 테스트 데이터 크기 ---')
print('x_train :', x_train.shape)  # (133, 2)
print('x_test  :', x_test.shape)   # (34, 2)

scaler = StandardScaler()
# 학습 데이터의 평균과 표준편차를 이용해 표준화
x_train_scaled = scaler.fit_transform(x_train)

# 테스트 데이터는 학습 데이터 기준으로 변환
x_test_scaled = scaler.transform(x_test)

print('\n표준화된 독립변수 ---')
print(x_train_scaled[:3])


# 5. 다항 특성 생성 : degree=2
quad = PolynomialFeatures(degree=2,include_bias=False)

x_train_quad = quad.fit_transform(x_train_scaled)
x_test_quad = quad.transform(x_test_scaled)

print('\n2차 다항 특성 ---')
print(quad.get_feature_names_out(x.columns))
# ['pgain', 'vgain', 'pgain^2', 'pgain vgain', 'vgain^2']

print('다항 특성 크기 :', x_train_quad.shape)  # (133, 5)
print(x_train_quad[:3])

print('\n1차 선형회귀 ---')
model = LinearRegression()
model.fit(x_train_scaled, y_train)

# 학습 및 테스트 데이터 예측
y_lin_train_pred = model.predict(x_train_scaled)
y_lin_pred = model.predict(x_test_scaled)

model_train_r2 = r2_score(y_train, y_lin_train_pred)
model_r2 = r2_score(y_test, y_lin_pred)

print('회귀계수 :', model.coef_)
print('절편 :', model.intercept_)

print('학습 결정계수(R²) :', model_train_r2)
print('테스트 결정계수(R²) :', model_r2)
print('MAE :', mean_absolute_error(y_test, y_lin_pred))
print('RMSE :', np.sqrt(mean_squared_error(y_test, y_lin_pred)))

print('예측값 :', y_lin_pred[:5].round(3))
print('실제값 :', y_test[:5].round(3))

print('\n2차 다항회귀 ---')
model_quad = LinearRegression()
model_quad.fit(x_train_quad, y_train)

# 학습 및 테스트 데이터 예측
y_quad_train_pred = model_quad.predict(x_train_quad)
y_quad_pred = model_quad.predict(x_test_quad)

q_train_r2 = r2_score(y_train, y_quad_train_pred)
q_r2 = r2_score(y_test, y_quad_pred)

print('회귀계수 :', model_quad.coef_)
print('절편 :', model_quad.intercept_)

print('학습 결정계수(R²) :', q_train_r2)
print('테스트 결정계수(R²) :', q_r2)
print('MAE :', mean_absolute_error(y_test, y_quad_pred))
print('RMSE :', np.sqrt(mean_squared_error(y_test, y_quad_pred)))

print('예측값 :', y_quad_pred[:5].round(3))
print('실제값 :', y_test[:5].round(3))

print('\n모델 성능 비교 ---')
result_df = pd.DataFrame({
    '모델': ['1차 선형회귀', '2차 다항회귀'],
    'Train R2': [model_train_r2, q_train_r2],
    'Test R2': [model_r2, q_r2],
    'MAE': [
        mean_absolute_error(y_test, y_lin_pred),
        mean_absolute_error(y_test, y_quad_pred)
    ],
    'RMSE': [
        np.sqrt(mean_squared_error(y_test, y_lin_pred)),
        np.sqrt(mean_squared_error(y_test, y_quad_pred))
    ]
})

print(result_df.round(4))

# 9. 시각화용 데이터 생성
# 독립변수가 2개이므로 pgain을 X축으로 사용하고 vgain은 평균값으로 고정
pgain_fit = np.linspace( x['pgain'].min(), x['pgain'].max(), 100)

# 학습 데이터의 vgain 평균값
vgain_mean = x_train['vgain'].mean()

# 그래프용 데이터
x_fit = pd.DataFrame({
    'pgain': pgain_fit,
    'vgain': np.full(len(pgain_fit), vgain_mean)
})

# 학습 시 사용한 표준화 기준 적용
x_fit_scaled = scaler.transform(x_fit)

# 1차 선형회귀 예측
y_lin_fit = model.predict(x_fit_scaled)

# 2차 다항회귀 예측
x_fit_quad = quad.transform(x_fit_scaled)
y_quad_fit = model_quad.predict(x_fit_quad)


# 10. 시각화 : 1차 회귀선과 2차 회귀곡선 비교 :하나의 2차원 차트에 표시
plt.figure(figsize=(10, 6))

# 실제 데이터 산점도
plt.scatter(x['pgain'], y, color='gray', alpha=0.5, label='실제 데이터')

# 1차 회귀직선
plt.plot(pgain_fit, y_lin_fit, linestyle=':', linewidth=3,
    color='blue', label='linear fit(d=1), $R^2=%.3f$' % model_r2
)

# 2차 회귀곡선
plt.plot(pgain_fit, y_quad_fit, linestyle='-', linewidth=3,
    color='red', label='quad fit(d=2), $R^2=%.3f$' % q_r2
)

plt.xlabel('pgain (비례 이득)')
plt.ylabel('응답 시간(class)')
plt.title(
    f'Servo 선형회귀와 다항회귀 비교 '
    f'(vgain={vgain_mean:.2f} 고정)'
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()