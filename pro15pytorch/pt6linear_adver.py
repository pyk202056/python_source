# 다중선형회귀모델 - tv,radio,newspaper가 sales에 얼마나 영향을 주는지 분석
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import r2_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head(2))
del data['no']    # python명령
# data.drop('no', axis=1, inplace=True)  # 위와 동일. pandas명령
print(data.head(2))

# feature, label 분리
fdata = data[['tv','radio','newspaper']]
ldata = data.iloc[:, 3]   # sales
print(fdata.head(2))
print(ldata.head(2))

# feature 정규화 - 모델 성능 향상에 효과적
fnomaldata = minmax_scale(fdata, axis=0, copy=True)  # 0 ~ 1 범위로 정규화
print(fnomaldata[:2])  # [[0.77578627 0.76209677 0.60598065]...

# train / test split
x_train,x_test,y_train,y_test = train_test_split(
    fnomaldata, ldata, shuffle=True, test_size=0.3, random_state=123
)
print(x_train.shape, x_test.shape)   # (140, 3) (60, 3)

# Tensor로 변환
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).reshape(-1, 1)
# y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).reshape(-1, 1)
y_test_tensor = torch.tensor(y_test.to_numpy(), dtype=torch.float32).reshape(-1, 1)

# validation dataset을 운영 (20%를 학습 중 검증 데이터로 사용)  --------
# TensorDataset : x와 y를 하나의 DataSet으로 묶음(쌍으로) -> train/validation으로 나눔
# feature(x)와 label(y)을 같은 인덱스 끼리 한쌍으로 묶어 DataSet으로 만든다.
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)

vali_size = int(len(train_dataset) * 0.2)
train_size = len(train_dataset) - vali_size

train_subset, vali_subset = random_split(
    train_dataset, [train_size, vali_size], 
    generator=torch.Generator().manual_seed(123)
)
print(len(train_dataset), '-->', len(train_subset), len(vali_subset))  # 140 --> 112 28
# -------------------------------------------------------------------

batch_size = 32   # 미니배치 크기

# DataLoader : data를 미니배치 단위로 꺼내주는 역할 
# - 전체 데이터를 한방에 모델에 주지 않고, 지정한 수 만큼 잘라서 반복적으로 모델에 공급
# - GPU나 CPU의 병렬 연산을 극대화 할 수 있다.
train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
vali_loader = DataLoader(vali_subset, batch_size=batch_size, shuffle=False)

test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 모델 학습 함수 정의 : 모델을 학습시키고, 매 epoch마다 loss를 기록
def train_modelFunc(model, train_loader, vali_loader, criterion, optimizer, epochs=100):
    # model 학습 -> 예측값계산 -> 손실계산 -> gradient초기화 -> 역전파 -> 파라미터갱신 -> loss 계산
    history = {
        "loss":[],
        "vali_loss":[]
    }

    for epoch in range(epochs):
        model.train()   # 모델을 핫습모드로 변경함을 알림
        train_loss_sum = 0   # 각 배치의 loss를 누적

        for x_batch, y_batch in train_loader:  # DataLoader에서 데이터를 batch단위로 가져옴
            # print(x_batch.shape)   # torch.Size([32, 3])
            pred = model(x_batch)            # 1) 예측값 계산
            loss = criterion(pred, y_batch)  # 2) 손실값 계산
            optimizer.zero_grad()            # 3) 이전 gradient초기화
            loss.backward()                  # 4) 역전파
            optimizer.step()                 # 5) 파라미터갱신(weight, bias)

            train_loss_sum += loss.item()    # loss 누적

        train_loss = train_loss_sum / len(train_loader)  # 1개의 epoch에서 평균 loss
        model.eval()   # 검즈 / 평가 모드로 전환 ( 직접 평가 수행 X )
        
        vali_loss_sum = 0  # validation 데이터에 대한 loss 누적
        with torch.no_grad():
            for x_vali, y_vali in vali_loader:
                vali_pred = model(x_vali)
                vali_loss = criterion(vali_pred, y_vali)
                vali_loss_sum += vali_loss.item()

        vali_loss = vali_loss_sum / len(vali_loader)  # 1개의 epoch에서 평균 validation loss

        history["loss"].append(train_loss)
        history["vali_loss"].append(vali_loss)

        # 학습 진행 상황 출력 
        if (epoch + 1) % 10 == 0:
            print(
                f'Epoch [{epoch + 1} / {epochs}] '
                f'train loss [{train_loss:.5f}] '
                f'vali loss [{vali_loss:.5f}] '
            )

    return history


# 평가 함수 정의 (test dataset으로)
def evaluate_modelFunc(model, x_test_tensor, y_test_tensor, criterion):
    model.eval()  # 평가 모드로 전환 (빼고 되나 관습적으로 적음)
    with torch.no_grad():
        pred = model(x_test_tensor)
        loss = criterion(pred, y_test_tensor)

    return loss.item(), pred


print('\n모델 작성 방법 1 : Sequential 클래스 사용 --------')
model = nn.Sequential(
    nn.Linear(3, 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)
print(model)

# 손실함수와 옵티마이저 정의
criterion = nn.MSELoss()
# optimizer = optim.Adam(model.parameters())  # lr=0.001이 기본값
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 모델 학습
history = train_modelFunc(
    model=model, train_loader=train_loader, vali_loader=vali_loader,
    criterion=criterion, optimizer=optimizer, epochs=100
)

# 모델 평가
ev_loss, pred_tensor = evaluate_modelFunc(
    model=model, 
    x_test_tensor=x_test_tensor, y_test_tensor=y_test_tensor, 
    criterion=criterion
)
print('ev_loss : ', ev_loss)

pre = pred_tensor.numpy()
actual = y_test_tensor.numpy()
print('MSE : ', ev_loss)
print('RMSE : ', np.sqrt(ev_loss))
print('설명력 : ', r2_score(actual, pre))

# history 값 확인
# print('history vali_loss : ', history['vali_loss'])
# print('history loss : ', history['loss'])

# loss 시각화
plt.plot(history['vali_loss'], label="vali_loss")
plt.plot(history['loss'], label="loss")
plt.legend()
plt.show()

# 기존 데이터로 예측
with torch.no_grad():
    pred_5 = model(x_test_tensor[:5])

print('예측값 : ', pred_5.numpy().ravel())
print('실제값 : ', y_test[:5].values.ravel())


print('\n\n모델 작성 방법 2 : nn.Module 클래스를 상속받아 사용 --------')
class AdverRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        # layer 정의
        self.hidden_layer1 = nn.Linear(3, 16)
        self.hidden_layer2 = nn.Linear(16, 8)
        self.output_layer = nn.Linear(8, 1)

        self.relu = nn.ReLU()  # activation 정의

    def forward(self, inputs):
        # 데이터 흐름을 정의
        net = self.hidden_layer1(inputs)
        net = self.relu(net)

        net = self.hidden_layer2(net)
        net = self.relu(net)

        outputs = self.output_layer(net)

        return outputs

model2 = AdverRegressionModel()
"""
print(model2)
# print(model2.parameters())
for param in model2.parameters():
    print(param)
"""
for name, param in model2.named_parameters():  # 각 파라미터의 이름 확인
    print(name, ":", param.data)

# optimizer는 다시 선언
optimizer = optim.Adam(model2.parameters(), lr=0.01)

# 모델 학습
history2 = train_modelFunc(
    model=model2, train_loader=train_loader, vali_loader=vali_loader,
    criterion=criterion, optimizer=optimizer, epochs=100
)

# 모델 평가
ev_loss2, pred_tensor2 = evaluate_modelFunc(
    model=model2, 
    x_test_tensor=x_test_tensor, y_test_tensor=y_test_tensor, 
    criterion=criterion
)
print('ev_loss2 : ', ev_loss2)

pre2 = pred_tensor2.numpy()
actual = y_test_tensor.numpy()
print('MSE : ', ev_loss2)
print('RMSE : ', np.sqrt(ev_loss2))
print('설명력 : ', r2_score(actual, pre2))
