# 다항회귀 : 데이터가 비선형 분포인 경우
# 선형모델이 비선형 관계를 학습할 수 있도록 입력 feature를 변환

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

np.random.seed(7)
torch.manual_seed(7)

# 가상의 feature, label 생성
x = np.linspace(-3, 3, 40).reshape(-1, 1).astype(np.float32)
print(x[:5])  # [[-3.       ] [-2.8461537] ...
# y = x^2 + x + 2 + noise
y = ((x[:, 0] ** 2) + x[:,0] + 2 + \
    np.random.normal(0, 1.5, size=len(x))).astype(np.float32)
print(y[:5])

# plt.scatter(x, y)
# plt.show()

# tensor로 변환
x_tensor = torch.tensor(x, dtype=torch.float32)
y_tensor = torch.tensor(y.reshape(-1, 1), dtype=torch.float32)
# print(x_tensor[:5])
# print(y_tensor[:5])

# R2 score 계산 함수 작성 : 수식은 1 - (SSR / SST)
def r2scoreFunc(y_true, y_pred):
    y_true = y_true.reshape(-1)
    y_pred = y_pred.reshape(-1)

    ss_res = np.sum((y_true - y_pred) ** 2)           # 잔차제곱합
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # 전체제곱합
    return 1 - (ss_res / ss_tot)

# 1. 선형회귀 모델
linear_model = nn.Linear(in_features=1, out_features=1)
criterion = nn.MSELoss()
linear_optimizer = optim.Adam(linear_model.parameters(), lr=0.01)

epochs = 500

for epoch in range(epochs):
    y_pred = linear_model(x_tensor)
    loss = criterion(y_pred, y_tensor)
    linear_optimizer.zero_grad()
    loss.backward()
    linear_optimizer.step()

# 학습 데이터에 대한 예측
with torch.no_grad():
    y_pred_linear = linear_model(x_tensor).numpy()


# 2. 다항회귀 모델
# x_poly = [x, x^2]  # feature를 확장
x_poly = np.column_stack([x[:, 0], x[:, 0] ** 2]).astype(np.float32)
print(x_poly[:3])

x_poly_tensor = torch.tensor(x_poly, dtype=torch.float32)

poly_model = nn.Linear(in_features=2, out_features=1)  # 입력이 2개
poly_optimizer = optim.Adam(poly_model.parameters(), lr=0.01)

# 학습
for epoch in range(epochs):
    y_pred = poly_model(x_poly_tensor)
    loss = criterion(y_pred, y_tensor)
    poly_optimizer.zero_grad()
    loss.backward()
    poly_optimizer.step()

# 학습 데이터에 대한 예측
with torch.no_grad():
    y_pred_poly = poly_model(x_poly_tensor).numpy()

# 그래프용 예측 데이터 만들기 : 부드러운 x축 데이터
x_plot = np.linspace(x.min(), x.max(), 300).reshape(-1, 1).astype(np.float32)
x_plot_tensor = torch.tensor(x_plot, dtype=torch.float32)

# 선형회귀 모델의 그래프용 예측
with torch.no_grad():
    y_plot_linear = linear_model(x_plot_tensor).numpy()

# 다항회귀 모델은 입력으로 [x, x^2] 형태가 필요함
x_plot_poly = np.column_stack([x_plot[:, 0], x_plot[:, 0] ** 2]).astype(np.float32)
x_plot_poly_tensor = torch.tensor(x_plot_poly, dtype=torch.float32)

# 다항회귀 모델의 그래프용 예측
with torch.no_grad():
    y_plot_poly = poly_model(x_plot_poly_tensor).numpy()

# 모델 성능 계산
r2_linear = r2scoreFunc(y, y_pred_linear)
r2_poly = r2scoreFunc(y, y_pred_poly)
print('r2_linear : ', r2_linear)  # -0.02269828
print('r2_poly : ', r2_poly)      #  0.81812257

# 시각화
plt.figure(figsize=(9, 6))
plt.scatter(x, y, label="data")

plt.plot(x_plot, y_plot_linear, 
        label=f'Linear Regression(R²={r2_linear:.3f})')
plt.plot(x_plot, y_plot_poly, 
        label=f'Poly Regression(R²={r2_poly:.3f})')
plt.xlabel('feature')
plt.ylabel('label')
plt.legend()
plt.grid(True)
plt.show()
