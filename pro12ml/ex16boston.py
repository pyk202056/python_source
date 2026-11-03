# 보스턴 주택 가격
# : 1978년에 발표된 데이터로 미국 보스턴 지역의 주택 가격에 영향을 미치는 요소들을 정리함

# CRIM	자치시(town)별 1인당 범죄율
# ZN	25,000 평방피트를 초과하는 거주지역 토지의 비율
# INDUS	비소매 상업지역 넓이 비율
# CHAS	찰스강(Charles River) 경계 위치 여부 (더미 변수: 강 주변=1, 그외=0)
# NOX	산화질소 농도 (10ppm 당)
# RM	주택당 평균 방의 개수
# AGE	1940년 이전에 건축된 자가 소유 주택의 비율
# DIS	5개의 보스턴 고용 센터까지의 가중 거리
# RAD	고속도로 접근성 지수
# TAX	재산세율 (10,000 달러당)
# PTRATIO	자치시(town)별 학생-교사 비율
# B	자치시별 흑인 거주 비율 관련 지표 (1000(Bk - 0.63)^2 형태)
# LSTAT	저소득층(lower status) 인구의 비율(%)
# MEDV	자가 소유 주택의 중간 가격 (Target, 단위: 1,000달러)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

pd.set_option('display.max_columns', None)

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/housing.data", header=None, sep=r'\s+')
df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
print(df.head(2))
print(df.corr())   # LSTAT(저소득층 인구), MEDV(주택가격) :  -0.737663 

x = df[['LSTAT']].values
y = df['MEDV'].values
print(x[:3])  # [[4.98][9.14][4.03]]
print(y[:3])  # [24.  21.6  34.7]

# 단항을 통한 단순선형회귀 모델
model = LinearRegression()

# 다항 특성(변수)
quad = PolynomialFeatures(degree=2)
cubic = PolynomialFeatures(degree=3)
x_quad = quad.fit_transform(x)
x_cubic = cubic.fit_transform(x)
print(x_quad[:3])
print(x_cubic[:3])

# 단순회귀
model.fit(x, y)
x_fit = np.arange(x.min(), x.max(), 1)[:, np.newaxis]
y_lin_fit = model.predict(x_fit)    # 그래프에 표시용
# print('y_lin_fit : ', y_lin_fit)
model_r2 = r2_score(y, model.predict(x))
print('model_r2 : ', model_r2)  # 0.544146

# 다항(2차)
model.fit(x_quad, y)
y_quad_fit = model.predict(quad.fit_transform(x_fit))
q_r2 = r2_score(y, model.predict(x_quad))
print('q_r2 : ', q_r2)   # 0.64071689

# 다항(3차)
model.fit(x_cubic, y)
y_cubic_fit = model.predict(cubic.fit_transform(x_fit))
c_r2 = r2_score(y, model.predict(x_cubic))
print('c_r2 : ', c_r2)   # 0.6578476

# 시각화
plt.scatter(x, y, label='초기 데이터')
plt.plot(x_fit, y_lin_fit, linestyle=':', label='linear fit(d=1), $R^2=%.2f$'%model_r2, lw=3, c='b')
plt.plot(x_fit, y_quad_fit, linestyle='-', label='quad fit(d=2), $R^2=%.2f$'%q_r2, lw=3, c='r')
plt.plot(x_fit, y_cubic_fit, linestyle='--', label='cubic fit(d=3), $R^2=%.2f$'%c_r2, lw=3, c='k')
plt.xlabel('하위계층비율')
plt.ylabel('주택가격')
plt.legend()
plt.show()