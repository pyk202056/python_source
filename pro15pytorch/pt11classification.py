# 딥러닝으로 분류 모델 (이항분류)
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.metrics import accuracy_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

np.random.seed(42)
torch.manual_seed(42)

# 데이터 생성
x_data = np.array([[1,2],[2,3],[3,4],[4,3],[3,2],[2,1]], dtype=np.float32)
y_data = np.array([[0],[0],[0],[1],[1],[1]], dtype=np.float32)

x_tensor = torch.tensor(x_data, dtype=torch.float32)
y_tensor = torch.tensor(y_data, dtype=torch.float32)

# 두 모델에 대한 학습 공통 함수
def train_modelFunc(model, x_train, y_train, epochs=20, lr=0.01, batch_size=1):
    criterion = nn.BCELoss()   # Binary Cross Entropy : 이항분류
    optimizer = optim.Adam(model.parameters(), lr=lr)
    data_size = len(x_train)

    for epoch in range(epochs):
        indices = torch.randperm(data_size)  # 매 epoch 마다 데이터 섞기
        total_loss = 0

        for i in range(0, data_size, batch_size):
            # 섞은 인덱스에서 미니배치에 사용할 번호를 뽑아 데이터를 가져옴
            batch_idx = indices[i:i + batch_size]

            x_batch = x_train[batch_idx]
            y_batch = y_train[batch_idx]

            pred = model(x_batch)  # 순전파
            loss = criterion(pred, y_batch)  # 손실계산
            optimizer.zero_grad()
            loss.backward()   # 역전파
            optimizer.step()
            total_loss += loss.item()

    return model

# 공통 평가 함수
def evaluate_modelFunc(model, x, y):
    criterion = nn.BCELoss()

    with torch.no_grad():
        pred = model(x)
        loss = criterion(pred, y).item()
        pred_class = (pred >= 0.5).float()  # 확률값을 0 또는 1로 변환
        print('pred_class : ', pred_class)
        accuracy = (pred_class == y).float().mean().item()

    return loss, accuracy

print('\n모델 작성 1 : Sequential 클래스 사용 ---')
seq_model = nn.Sequential(
    nn.Linear(in_features=2, out_features=4),
    nn.ReLU(),
    nn.Linear(in_features=4, out_features=1),
    nn.Sigmoid()
)
print(seq_model)
# Sequential(
#   (0): Linear(in_features=2, out_features=4, bias=True)
#   (1): ReLU()
#   (2): Linear(in_features=4, out_features=1, bias=True)
#   (3): Sigmoid()
# )

# 모델 학습
seq_model = train_modelFunc(
    model=seq_model, x_train=x_tensor, y_train=y_tensor, \
    epochs=20, lr=0.01, batch_size=1
)
# 모델 평가
loss, acc = evaluate_modelFunc(model=seq_model, x=x_tensor, y=y_tensor)
print(f'방법1 평가 결과 : 손실={loss:.4f}, 분류 정확도={acc:.4f}')  # 손실=0.4389, 분류 정확도=1.0000

# 예측값과 확률값으로 시각화 ------------
# 2차원 입력(x1, x2)을 가진 모델을 x2는 고정하고, x1만 변화하며 sigmoid 형태의 출력
x1_range = np.linspace(0, 6, 100).astype(np.float32)
x2_fixed = 2.5
x_vis = np.column_stack([
    x1_range, np.full_like(x1_range, x2_fixed)
])
x_vis_tensor = torch.tensor(x_vis, dtype=torch.float32)

# 예측 확률 계산
with torch.no_grad():
    y_prob = seq_model(x_vis_tensor).numpy()

x1_real = x_data[:, 0]
y_real = y_data.ravel()

plt.figure(figsize=(7, 5))
plt.plot(x1_range, y_prob, label='sigmoid curve')
plt.scatter(x1_real, y_real, color='red', label='True data')
plt.xlabel('x_data')
plt.ylabel('probability')
plt.legend(loc='lower right')
plt.grid()
plt.show()

print('\n모델 작성 2 : Module 클래스 사용 (좀 더 일반적) ---')
class MyClassModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.dense1 = nn.Linear(in_features=2, out_features=4)
        self.relu = nn.ReLU()
        self.dense2 = nn.Linear(in_features=4, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, inputs):
        net = self.dense1(inputs)
        net = self.relu(net)
        net = self.dense2(net)
        net = self.sigmoid(net)
        return net

mymodel = MyClassModel()
print(mymodel)

mymodel = train_modelFunc(
    model=mymodel, x_train=x_tensor, y_train=y_tensor, \
    epochs=20, lr=0.01, batch_size=1
)

loss2, acc2 = evaluate_modelFunc(mymodel, x_tensor, y_tensor)
print(f'방법2 평가 결과 : 손실={loss2:.4f}, 분류 정확도={acc2:.4f}')  
