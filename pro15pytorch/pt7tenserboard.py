# 텐서보드는 머신러닝 실험에 필요한 시각화 및 도구를 제공합니다.
# 손실 및 정확도와 같은 측정항목 추적 및 시각화
# 모델 그래프(작업 및 레이어) 시각화
# 시간의 경과에 따라 달라지는 가중치, 편향, 기타 텐서의 히스토그램 확인
# 저차원 공간에 임베딩 투영
# 이미지, 텍스트, 오디오 데이터 표시
# 그 외 다양한 도구 제공

# python -m pip install tensorboard

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

from sklearn.datasets import load_diabetes
from torch.utils.tensorboard import SummaryWriter
import datetime
import os

# data load 
diabetes = load_diabetes()     # 당뇨병 환자의 1년 후 질병 진행 정도를 나타내는 정량적 수치
xdata = diabetes.data
ydata = diabetes.target.reshape(-1, 1)  # s6:혈당 수치
print(xdata[:2], ' ', xdata.shape)  # [[ 0.03807591  0.05068012 ...  (442, 10)
print(ydata[:2], ' ', ydata.shape)  # [[151.] [ 75.]]  (442, 1)
print('feature names : ', diabetes.feature_names)
# ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
# age:나이, Sex:성별, bmi	:체질량지수, bp:평균 혈압
# s1:총 콜레스테롤, s2:저밀도 지단백 콜레스테롤, s3:고밀도 지단백 콜레스테롤
# s4:총 콜레스테롤 / HDL 비율, s5:혈청 중성지방 수치의 로그값으로 추정,  

# 데이터 표준화 : 딥러닝에서는 feature의 스케일링 강력 추천
# diabetes은 사실 표준화 되어 있으나 연습을 위해 표준화 하기
scaler = StandardScaler()
xdata_scaled = scaler.fit_transform(xdata)

# train / test split
x_train, x_test, y_train, y_test = train_test_split(
    xdata_scaled, ydata, test_size=0.3, shuffle=True, random_state=123
)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

# Tensor로 변환
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# train data의 일부를 validation data로 분리
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
vali_size = int(len(train_dataset) * 0.2)
train_size = int(len(train_dataset) - vali_size)

train_subset, vali_subset = random_split(
    train_dataset, [train_size, vali_size], 
    generator=torch.Generator().manual_seed(123)
)

batch_size = 32

train_loader = DataLoader(
    train_subset, batch_size=batch_size, shuffle=True
)
vali_loader = DataLoader(
    vali_subset, batch_size=batch_size, shuffle=False
)
print(len(train_loader.dataset), len(vali_loader.dataset))  # 248 61

# 모델 정의
class DiabetRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.hidden_layer1 = nn.Linear(10, 64)
        self.hidden_layer2 = nn.Linear(64, 32)
        self.hidden_layer3 = nn.Linear(32, 16)
        self.output_layer = nn.Linear(16, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        # net = self.hidden_layer1(x)
        # net = self.relu(net)
        net = self.relu(self.hidden_layer1(x))   # 위 두줄을 한줄로
        net = self.relu(self.hidden_layer2(net))
        net = self.relu(self.hidden_layer3(net))
        net = self.output_layer(net)
        return net

model = DiabetRegressionModel()
print(model)

# loss function, optimizer 정의
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# TensorBoard 로그 저장 경로
log_dir = os.path.join(
    "runs", "diabet_regression",
    datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
)

writer = SummaryWriter(log_dir=log_dir)  # 저장 로그 위치 지정
print("텐서보드 로그 저장 위치 : ", log_dir)
# 텐서보드에 모델 그래프 기록
sample_input = x_train_tensor[:1]
writer.add_graph(model, sample_input)


epochs = 200
train_loss_history = []
vali_loss_history = []

for epoch in range(epochs):
    model.train()
    train_loss_sum = 0

    for x_batch, y_batch in train_loader:
        pred = model(x_batch)   # 예측값 계산
        loss = criterion(pred, y_batch) # 손실 계산
        optimizer.zero_grad()   # gradient 초기화
        loss.backward()         # 역전파
        optimizer.step()        # 파라미터 갱신
        train_loss_sum += loss.item()

    train_loss = train_loss_sum / len(train_loader)

    model.eval()
    vali_loss_sum = 0
    with torch.no_grad():
        for x_vali, y_vali in vali_loader:
            vali_pred = model(x_vali)
            vali_loss = criterion(vali_pred, y_vali)
            vali_loss_sum += vali_loss.item()

    vali_loss = vali_loss_sum / len(vali_loader)

    train_loss_history.append(train_loss)
    vali_loss_history.append(vali_loss)

    # 텐서보드에 기록 --------
    writer.add_scalar("Loss/train", train_loss, epoch)  # (태그명, 기록값, x축값)
    writer.add_scalar("Loss/validation", vali_loss, epoch)  # (태그명, 기록값, x축값)

    # 각 레리어의 weight histogram 기록
    for name, param in model.named_parameters():
        writer.add_histogram(name, param, epoch)  # 여러 파라미터 분포 변화 기록
    # ----------------------

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{epochs}] train_loss:{train_loss:.4f}, vali_loss:{vali_loss:.4f}')

# test data로 학습이 끝난 모델 검증
model.eval()
with torch.no_grad():
    test_pred = model(x_test_tensor)
    test_loss = criterion(test_pred, y_test_tensor)

print('test loss : ', test_loss.item())
test_pred_np = test_pred.numpy()
print('설명력(R2) : ', r2_score(y_test, test_pred_np))

# 텐서보드에 최종 test loss 기록
writer.add_scalar("Loss/test", test_loss.item(), epochs)
writer.close()

# loss 시각화
plt.plot(train_loss_history, label = 'train loss')
plt.plot(vali_loss_history, label='validation loss')
plt.xlabel('학습횟수')
plt.ylabel('손실(loss)')
plt.legend()
plt.show()

# 예측값 일부 확인
print('예측값 : ', test_pred_np[:5].ravel())
print('실제값 : ', y_test[:5].ravel())
