# 다항분류 - softmax
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

# softmax 함수 : 입력받은 실수 벡터를 0 ~ 1 사이의 확률값으로 변환
# softmax(x_i) = exp(x_i) / sum(exp(x))

def softmaxFunc(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    return exp_a / sum_exp_a

data = np.array([0.12, 2.34, 4.0])
print(softmaxFunc(data))
print(0.01705566 + 0.15703715 + 0.82590719)

# 예제 데이터 직접 작성
np.random.seed(42)
torch.manual_seed(42)
np.set_printoptions(suppress=True, precision=3)
print()

xdata = np.random.random((1000, 12)).astype(np.float32)
ydata = np.random.randint(5, size=(1000,))
print(xdata[:2])
print(ydata[:2])

x_tensor = torch.tensor(xdata, dtype=torch.float32)
y_tensor = torch.tensor(ydata, dtype=torch.long)  # nn.CrossEntropyLoss의 label의 long type이므로
print(x_tensor.shape)   # torch.Size([1000, 12])
print(y_tensor.shape)   # torch.Size([1000])

"""
이항분류와 다항분류 비교  -----------------------
구분            이항분류               다항분류
입력 데이터(x)   2차원 (N, features)   2차원 (N, features)  <== N:입력 데이터 개수(Batch Size)
모델 출력        2차원 (N, 1)          2차원 (N, C)  <== C:분류할 클래스 개수
정답 데이터(y)   2차원 (N, 1)          1차원 (N,)
Label 자료형     torch.float32         torch.long
손실함수         BCEWithLogitsLoss()   CrossEntropyLoss()
활성화 함수      Sigmoid               Softmax
"""

# 다항분류 모델 정의
class MultiClassClassifier(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(12, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 5),
        )

    def forward(self, x):
        return self.net(x)

model = MultiClassClassifier()
print(model)

logits = model(x_tensor)
print(torch.softmax(logits, dim=1).shape)  # torch.Size([1000, 5])
prob = torch.softmax(logits, dim=1)
print(prob.shape)                          # torch.Size([1000, 5])
print(torch.argmax(prob, dim=1).shape)     # torch.Size([1000])

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 모델 학습
EPOCHS = 500
BATCH_SIZE = 32

history = {"loss":[], "accuracy":[]}

data_size = len(x_tensor)

for epoch in range(EPOCHS):
    model.train()
    indices = torch.randperm(data_size)

    epoch_loss_sum = 0
    epoch_corect = 0
    epoch_total = 0

    for start in range(0, data_size, BATCH_SIZE):
        batch_idx = indices[start:start + BATCH_SIZE]
        x_batch = x_tensor[batch_idx]
        y_batch = y_tensor[batch_idx]

        logits = model(x_batch)
        loss = criterion(logits, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss_sum += loss.item() * x_batch.size(0)
        pred_class = torch.argmax(logits, dim=1)  # 예측 class

        epoch_corect += (pred_class == y_batch).sum().item()
        epoch_total += y_batch.size(0)

    epoch_loss = epoch_loss_sum / epoch_total
    epoch_acc = epoch_corect / epoch_total
    history["loss"].append(epoch_loss)
    history["accuracy"].append(epoch_acc)
    print(f'Epoch {epoch + 1:04d} / {EPOCHS}, loss:{epoch_loss:.4f}, accuracy:{epoch_acc:.4f}')
    
# 모델 평가
model.eval()

with torch.no_grad():
    logits = model(x_tensor)
    loss = criterion(logits, y_tensor).item()
    pred_class = torch.argmax(logits, dim=1)
    acc = (pred_class == y_tensor).float().mean().item()

print('모델 평가 결과 : ', [loss, acc])

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 4))

ax1.plot(history['loss'])
ax1.set_title('loss')
ax1.set_xlabel('epoch')
ax1.set_ylabel('loss')
ax1.grid(True)

ax2.plot(history['accuracy'])
ax2.set_title('accuracy')
ax2.set_xlabel('epoch')
ax2.set_ylabel('accuracy')
ax2.grid(True)

plt.show()







