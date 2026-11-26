# 다항회귀 : 광보비에 따른 매출액 예측

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import torch
import torch.nn as nn
import torch.optim as optim

np.random.seed(7)
torch.manual_seed(7)

"""
# 데이터 파일 작성 - csv
# 광고비가 증가하면 매출도 증가하지만, 어느 정도 이후에는 매출 증가폭이 둔화되는 자료
ad_cost = np.linspace(0, 100, 80)  # 광고비 자료
# sales = -0.06 * 광고비² + 7.5 * 광고비 + 40 + noise
sales = -0.06 * (ad_cost ** 2) + 7.5 * ad_cost + 40 + \
            np.random.normal(0, 25, size=len(ad_cost))
df = pd.DataFrame({'광고비':ad_cost, '매출':sales})
print(df.head(3))
df.to_csv('ad_sales.csv', index=False, encoding='utf-8-sig')
"""
# 데이터 파일 읽기 - csv
df = pd.read_csv('ad_sales.csv')
print(df.head(3))
print(df.info())

# 결측치가 있다면 제거
df = df.dropna()
print(df.shape)  # (80, 2)

# feature, label 분리
x = df[['광고비']].values.astype(np.float32)
y = df[['매출']].values.astype(np.float32)

# 데이터 시각화
plt.figure(figsize=(8, 5))
plt.scatter(x, y)
plt.xlabel('광고비')
plt.ylabel('매출')
plt.grid()
plt.show()

# train / split 
indices = np.arange(len(x))
np.random.shuffle(indices)
x = x[indices]
y = y[indices]
train_size = int(len(x) * 0.8)
x_train = x[:train_size]
x_test = x[train_size:]
y_train = y[:train_size]
y_test = y[train_size:]
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)  # (64, 1) (16, 1) (64, 1) (16, 1)

# Scaling(표준화) : train 데이터 기주느오 평균과 표준편차 계산
x_mean = x_train.mean(axis=0)
x_std = x_train.std(axis=0)
x_train_scaled = (x_train - x_mean) / x_std
x_test_scaled = (x_test - x_mean) / x_std

y_mean = y_train.mean(axis=0)
y_std = y_train.std(axis=0)
y_train_scaled = (y_train - y_mean) / y_std
y_test_scaled = (y_test - y_mean) / y_std

# 다항 특성 생성 함수  : degree=2이면 [x, x^2] 형태 자료 생성
def make_poly_features(x_scaled, degree=2):
    features = [x_scaled ** d for d in range(1, degree + 1)]
    return np.concatenate(features, axis=1).astype(np.float32)

x_train_poly = make_poly_features(x_train_scaled, degree=2)
x_test_poly = make_poly_features(x_test_scaled, degree=2)
print('선형회귀 입력 자료 shape : ', x_train_scaled.shape)  # (64, 1)
print('다항회귀 입력 자료 shape : ', x_train_poly.shape)    # (64, 2)

# Tensor로 변환
x_train_scaled_t = torch.tensor(x_train_scaled, dtype=torch.float32)
x_test_scaled_t = torch.tensor(x_test_scaled, dtype=torch.float32)

x_train_poly_t = torch.tensor(x_train_poly, dtype=torch.float32)
x_test_poly_t = torch.tensor(x_test_poly, dtype=torch.float32)

y_train_scaled_t = torch.tensor(y_train_scaled, dtype=torch.float32)
y_test_scaled_t = torch.tensor(y_test_scaled, dtype=torch.float32)

# 평가함수 : R2score, MSE, RMSE 직접 계산
def r2_score_npFunc(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)  # 잔차제곱합
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # 전체제곱합
    return 1 - (ss_res / ss_tot)   # 결정계수

# 모델 평가 후 출력 함수
def evaluateModelFunc(name, y_true, y_pred):
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)
    r2 = r2_score_npFunc(y_true, y_pred)
    print(f'\n[{name}] MSE:{round(mse, 3)}, RMSE:{round(rmse, 3)}, R2:{round(r2, 3)}')

# Model 정의 (선형회귀) : feature 1
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

# Model 정의 (다항회귀) : feature 2
class PolyRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2, 1)

    def forward(self, x):
        return self.linear(x)

linear_model = LinearRegressionModel()
poly_model = PolyRegressionModel()
print('선형모델 : ', linear_model)
print('다항모델 : ', poly_model)

# 모델 학습 함수
def train_modelFunc(model, x_train_t, y_train_t, epochs = 2000, lr=0.01):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_history = []

    for epoch in range(epochs):
        model.train()
        y_pred = model(x_train_t)
        loss = criterion(y_pred, y_train_t)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_history.append(loss.item())

        if (epoch + 1) % 100 == 0:
            print(f'epoch:{epoch + 1:5d} / {epochs}, loss:{loss.item():.5f}')

    return loss_history

# 모델 학습
print('\n선형모델 학습')
linear_loss_history = train_modelFunc(
    linear_model, x_train_scaled_t, y_train_scaled_t, epochs = 2000, lr=0.01
)

print('\n다항모델 학습')
poly_loss_history = train_modelFunc(
    poly_model, x_train_poly_t, y_train_scaled_t, epochs = 2000, lr=0.01
)

# 평가(test dataset) 및 예측
linear_model.eval()
poly_model.eval()

with torch.no_grad():
    y_pred_linear_scaled_t = linear_model(x_test_scaled_t)  # 예측값은 scaled y 기준으로 나옴
    y_pred_poly_scaled_t = poly_model(x_test_poly_t)

# Tensor -> ndarray
y_pred_linear_scaled = y_pred_linear_scaled_t.numpy()
y_pred_poly_scaled = y_pred_poly_scaled_t.numpy()

# 표준화된 label을 원래 매출단위로 복원
y_pred_linear = y_pred_linear_scaled * y_std + y_mean
y_pred_poly = y_pred_poly_scaled * y_std + y_mean

# 두 모델 성능 비교
evaluateModelFunc("선형회귀", y_test, y_pred_linear)
evaluateModelFunc("다항회귀 degree=2", y_test, y_pred_poly)

# 손실 시각화
plt.figure(figsize=(8, 5))
plt.plot(linear_loss_history, label='선형회귀 손실')
plt.plot(poly_loss_history, label='다항회귀 손실')
plt.xlabel('학습횟수')
plt.ylabel('손실')
plt.legend()
plt.grid()
plt.show()

# 예측 회귀선 시각화
x_plot = np.linspace(x.min(), x.max(), 300).reshape(-1, 1).astype(np.float32)
x_plot_scaled = (x_plot - x_mean) / x_std
x_plot_poly = make_poly_features(x_plot_scaled, degree=2)

x_plot_scaled_t = torch.tensor(x_plot_scaled, dtype=torch.float32)
x_plot_poly_t = torch.tensor(x_plot_poly, dtype=torch.float32)

linear_model.eval()
poly_model.eval()
with torch.no_grad():
    y_plot_linear_scaled_t = linear_model(x_plot_scaled_t)  # 예측값은 scaled y 기준으로 나옴
    y_plot_poly_scaled_t = poly_model(x_plot_poly_t)

# Tensor -> ndarray
y_plot_linear_scaled = y_plot_linear_scaled_t.numpy()
y_plot_poly_scaled = y_plot_poly_scaled_t.numpy()

# 표준화된 label을 원래 매출단위로 복원
y_plot_linear = y_plot_linear_scaled * y_std + y_mean
y_plot_poly = y_plot_poly_scaled * y_std + y_mean

plt.figure(figsize=(8, 5))
plt.scatter(x_train, y_train, alpha=0.5, label='train data')
plt.scatter(x_test, y_test, alpha=0.8, label='test data')
plt.plot(x_plot, y_plot_linear, label='선형회귀')
plt.plot(x_plot, y_plot_poly, label='다항회귀')
plt.xlabel('광고비')
plt.ylabel('판매량')
plt.legend()
plt.grid()
plt.show()
