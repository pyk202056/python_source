# MNIST 손글씨 숫자 이미지 분류 모델 작성
# 주요 기능
# 손으로 쓴 숫자 이미지가 학습용 60,000개, 테스트용 10,000개로 총 70,000개 있다.
# 모든 이미지는 하나의 숫자를 담은 28x28 그레이스케일 이미지이며, 
# 크기가 정규화되고 앤티앨리어싱 처리되어 20x20 상자에 맞게 조정된 후 28x28 프레임의 중앙에 배치.
# 10개 클래스는 숫자 0–9로 구성되며, 클래스마다 이미지 수가 대체로 균형을 이룬다.
# 사전 정의된 학습/테스트 분할을 제공하므로 수동 또는 자동 분할이 필요하지 않다.
# MNIST는 이미지 분류 및 딥러닝 연구에서 표준 벤치마크로 사용된다.

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.datasets import fetch_openml

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

np.random.seed(42)
torch.manual_seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('사용장치 : ', device)

# MNIST 읽기
mnist = fetch_openml('mnist_784', version=1, as_frame=False)
x = mnist.data.astype('float32')
y = mnist.target.astype('int64')
print(x.shape, y.shape)  # (70000, 784) (70000,)
# print(x[0])
# print(y[0])

# train / test split
x_train = x[:60000]
y_train = y[:60000]
x_test = x[60000:]
y_test = y[60000:]
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape) # (60000, 784) (60000,) (10000, 784) (10000,)

# 시각화
"""
img = x_train[0].reshape(28, 28)
plt.imshow(img, cmap='gray')
plt.title(f'label={y_train[0]}')
plt.axis('off')
plt.show()
"""

# 정규화
x_train = x_train / 255.0
x_test = x_test / 255.0
print(x_train[0], x_train.shape)  # (60000, 784)

print(set(map(int, y_test)))  # {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# validation data 구성
# train : 60000개 중 뒤쪽 10000개를 validation data로 사용
x_val = x_train[50000:60000]
y_val = y_train[50000:60000]
x_train = x_train[0:50000]
y_train = y_train[0:50000]
print(x_val.shape, x_train.shape)  # (10000, 784) (50000, 784)

print()
# tensor화
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)

x_val_tensor = torch.tensor(x_val, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val, dtype=torch.long)

x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# 배치 처리
batch_size = 128

train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
val_dataset = TensorDataset(x_val_tensor, y_val_tensor)
test_dataset = TensorDataset(x_test_tensor, y_test_tensor)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 모델 정의
class MNISTModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(784, 64),
            nn.ReLU(),
            nn.Dropout(p=0.2),

            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(p=0.2),

            nn.Linear(32, 10)
        )

    def forward(self, x):
        return self.net(x)

model = MNISTModel().to(device=device)
print(model)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습
epochs = 30
history = {'loss':[], 'accuracy':[], 'val_loss':[], 'val_accuracy':[]}

for epoch in range(epochs):
    model.train()

    train_total_loss = 0.0
    train_correct = 0
    train_total = 0
    for batch_x, batch_y in train_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_total_loss += loss.item() * batch_x.size(0)  # 학습 손실 누적. size(0)은 크기를 정수로 반환:ex) [128]->128

        pred = torch.argmax(outputs, dim=1)
        train_correct += (pred == batch_y).sum().item()   # 학습 정답 갯수 누적
        train_total += batch_y.size(0)    # 학습 데이터 갯수 누적
        
    train_avg_loss = train_total_loss / train_total
    train_avg_acc = train_correct / train_total

    # 검증 모드 (validation data) : Dropout이 비활성된다.
    model.eval()

    val_total_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for batch_x, batch_y in val_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            # 검증이므로 역전파 X

            val_total_loss += loss.item() * batch_x.size(0)  # 학습 손실 누적. size(0)은 크기를 정수로 반환:ex) [128]->128
            
            pred = torch.argmax(outputs, dim=1)
            val_correct += (pred == batch_y).sum().item()   # 학습 정답 갯수 누적
            val_total += batch_y.size(0)

        val_avg_loss = val_total_loss / val_total
        val_avg_acc = val_correct / val_total

        history['loss'].append(train_avg_loss)
        history['accuracy'].append(train_avg_acc)
        history['val_loss'].append(val_avg_loss)
        history['val_accuracy'].append(val_avg_acc)

        print(
            f'Epoch [{epoch + 1:02d} / {epochs}]'
            f'loss : {train_avg_loss:.4f} '
            f'val_loss : {val_avg_loss:.4f} '
            f'val_accuracy : {val_avg_acc:.4f}'
        )

# 모델이 완성되었으므로 test data로 모델 검증
model.eval()

test_total_loss = 0.0
test_correct = 0
test_total = 0

with torch.no_grad():
    for batch_x, batch_y in test_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        # 검증이므로 역전파 X

        test_total_loss += loss.item() * batch_x.size(0) 
        
        pred = torch.argmax(outputs, dim=1)
        test_correct += (pred == batch_y).sum().item() 
        test_total += batch_y.size(0)

test_loss = test_total_loss / test_total
test_acc = test_correct / test_total
print(f'test loss:{test_loss:.4f}, accuracy:{test_acc:.4f}')

# 학습 결과 시각화
plt.plot(history['loss'], label='train loss')
plt.plot(history['val_loss'], label='validation loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

plt.plot(history['accuracy'], label='train accuracy')
plt.plot(history['val_accuracy'], label='validation accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()

# 모델 저장
torch.save(model.state_dict(), 'mnist_model.pth')
print('모델 저장 완료 : mnist_model.pth')
# ---데이터 분석(과학자)가 할 일 끝----------------------------------

# 모델 불러오기 - 모델이 필요한 누구던지
mymodel = MNISTModel().to(device=device)
mymodel.load_state_dict(torch.load('mnist_model.pth', map_location=device))
mymodel.eval()
print('모델 읽기 성공')

# 기존 테스트 데이터로 예측
with torch.no_grad():
    sample_x = x_test_tensor[1:2].to(device=device)
    logits = mymodel(sample_x)
    pred_prob = torch.softmax(logits, dim=1)
    pred_label = torch.argmax(pred_prob, dim=1).item()

print('pred : ', pred_prob.cpu().numpy())
print('예측값 : ', pred_label)
print('실제값 : ', y_test_tensor[1].item())

# 예측을 위해 사용된 이미지 시각화
plt.imshow(x_test_tensor[1].reshape(28, 28), cmap='gray')
plt.title(f'pred:{pred_label}, true:{y_test_tensor[1].item()}')
plt.show()
