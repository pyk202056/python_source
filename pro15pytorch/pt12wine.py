# 와인의 등급, 맛, 산도 등의 정보로 레드와인/화이트와인 분류 - 조기종료, 모델저장
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

np.random.seed(42)
torch.manual_seed(42)

# 데이처 읽기 - 6497 행
wdf = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/wine.csv", header=None)
print(wdf.head(2))
print(wdf.info())   # 마지막 열이 label(class)
print(wdf.iloc[:, 12].unique())       # [1(레드)   0(화이트)] 
print(len(wdf[wdf.iloc[:,12] == 0]))  # 4898
print(len(wdf[wdf.iloc[:,12] == 1]))  # 1599    클래스가 불균형함

# feature / label 분리  
dataset = wdf.values
x = dataset[:, 0:12].astype(np.float32)
y = dataset[:, -1].astype(np.float32)
print(x[:2])
print(y[:2])

# train / test split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, stratify=y, shuffle=True, random_state=12
)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)  # (4547, 12) (1950, 12) (4547,) (1950,)

# 스케일링 (표준화)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train).astype(np.float32)
x_test_scaled = scaler.fit_transform(x_test).astype(np.float32)

# train data를 train / validation으로 분리
x_train_part, x_val, y_train_part, y_val = train_test_split(
    x_train_scaled, y_train, test_size=0.2, stratify=y_train, random_state=12
)
print('train : ', x_train_part.shape, y_train_part.shape)  # (3637, 12) (3637,)
print('val : ', x_val.shape, y_val.shape)                  # (910, 12) (910,)
print('test : ', x_test_scaled.shape, y_test.shape)        # (1950, 12) (1950,)

print()
# ndarray -> tensor
x_train_tensor = torch.tensor(x_train_part, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train_part.reshape(-1, 1), dtype=torch.float32)
# y_train_tensor = torch.tensor(y_train_part, dtype=torch.float32).view(-1, 1)  상동

x_val_tensor = torch.tensor(x_val, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val.reshape(-1, 1), dtype=torch.float32)

x_test_tensor = torch.tensor(x_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.reshape(-1, 1), dtype=torch.float32)

train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# 모델 정의
class WineClassifier(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(12, 32),
            nn.ReLU(),

            nn.Linear(32, 24),
            nn.ReLU(),

            nn.Linear(24, 8),
            nn.ReLU(),

            nn.Linear(8, 1)
            # nn.Sigmoid()   손실함수를 BCEWithLogitsLoss()를 쓸 경우 생략
        )

    def forward(self, x):
        return self.net(x)

# cuda는 gpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("사용장치 : ", device)

model = WineClassifier().to(device=device)
print(model)

# criterion = nn.BCELoss()
criterion = nn.BCEWithLogitsLoss()  # 내부적으로 Sigmoid + BinaryCrossEntropy를 한 꺼번에 처리
optimizer = optim.Adam(model.parameters(), lr=0.001)

def evaluate_modelFunc(model, x_data, y_data):
    model.eval()
    x_data = x_data.to(device)
    y_data = y_data.to(device)

    with torch.no_grad():
        logits = model(x_data)   # pred
        loss = criterion(logits, y_data).item()

        # logits -> sigmoid(확률) -> 0, 1
        prob = torch.sigmoid(logits)
        pred = (prob >= 0.5).float()     # True:1, False:0
        acc = (pred == y_data).float().mean().item()

    return loss, acc

# 참고로 훈현되지 않은 모델의 정확도를 먼저 확인
train_loss_before, train_acc_before = evaluate_modelFunc(
    model, x_train_tensor, y_train_tensor
)
print(f'훈련되지 않은 모델의 정확도 : {train_acc_before * 100:.2f}%')  # 75.39%

# 조기종료 + 모델 저장 준비
patience = 5
best_val_loss = np.inf
patience_count = 0

MODEL_DIR = './winemodel/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

modelpath = './winemodel/winemodel_torch.pth'

# 모델 학습
EPOCHS = 5000
history = {
    'loss':[], 'accuracy':[], 'val_loss':[], 'val_accuracy':[]
}

for epoch in range(EPOCHS):
    model.train()
    train_loss_sum = 0
    train_correct = 0
    train_total = 0

    for batch_x, batch_y in train_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        logits = model(batch_x)  # 예측값 계산
        loss = criterion(logits, batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss_sum += loss.item() * batch_x.size(0)

        prob = torch.sigmoid(logits)  # accuracy 계산
        pred = (prob >= 0.5).float()

        train_correct += (pred == batch_y).sum().item()
        train_total += batch_y.size(0)

    # epoch 단위 train loss / accuracy 계산
    train_loss = train_loss_sum / train_total
    train_acc = train_correct / train_total

    # validation 평가
    val_loss, val_acc = evaluate_modelFunc(model, x_val_tensor, y_val_tensor)

    history['loss'].append(train_loss)
    history['accuracy'].append(train_acc)
    history['val_loss'].append(val_loss)
    history['val_accuracy'].append(val_acc)

    print(
        f'Epoch [{epoch + 1} / {EPOCHS}]'
        f'loss:{train_loss:.4f} '
        f'accuracy:{train_acc:.4f} '
        f'val_loss:{val_loss:.4f} '
        f'val_accuracy:{val_acc:.4f}'
    )

    # 최고의 모델 저장
    if val_loss < best_val_loss:  # 검증 손실이 개선된 경우
        best_val_loss = val_loss
        patience_count = 0

        # 최적 모델의 파라미터 저장
        torch.save(model.state_dict(), modelpath)
        print(f'최적 모델 저장 : {epoch + 1}, val_loss:{best_val_loss:.5f}')
    else:
        patience_count += 1

    # 조기 종료 : patience 횟수만큼 val_loss 가 개선되지 않으면 조기 종료
    if patience_count >= patience:
        print(f'조기 종료 발생 : {epoch + 1} 번에서 학습 중단')
        break

print('\n학습 완료 ---')
print('전체 학습 횟수 : ', len(history['loss']))
print('최적 학습 횟수 : ', np.argmin(history['loss']) + 1)
print('최소 검증 손실 : ', best_val_loss)

# 저장된 최적의 모델 읽기 ~~~~~~~
best_model = WineClassifier().to(device=device)
best_model.load_state_dict(torch.load(modelpath, map_location=device))

best_model.eval()
# test data로 평가
test_loss, test_acc = evaluate_modelFunc(best_model, x_test_tensor, y_test_tensor)
print(f'훈련된 모델의 정확도 : {test_acc * 100:.2f}%')  # 99.38%
print(f'test 손실(loss) : {test_loss:.4f}')   

# 시각화 - loss
epoch_len = np.arange(len(history['loss']))

plt.figure(figsize=(8, 5))
plt.plot(epoch_len, history['val_loss'], c='red', label='val_loss')
plt.plot(epoch_len, history['loss'], c='blue', label='loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.grid()
plt.show()

# 시각화 - accuracy
plt.figure(figsize=(8, 5))
plt.plot(epoch_len, history['val_accuracy'], c='red', label='val_accuracy')
plt.plot(epoch_len, history['accuracy'], c='blue', label='accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.grid()
plt.show()

# 저장된 모델로 예측
new_data = x_test[:5, :]
print('원본 데이터 : ', new_data)

# 스케일링 -> 텐서화
new_data_scaled = scaler.fit_transform(new_data).astype(np.float32)
new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32).to(device)

with torch.no_grad():
    logits = best_model(new_data_tensor)
    new_prob = torch.sigmoid(logits)  # logits를 확률로 변환 (0 ~ 1 사이의 실수)
    new_pred = (new_prob >= 0.5).int()

print('예측 확률 : ', new_prob.cpu().numpy().ravel())
print('예측 결과 : ', new_pred.cpu().numpy().ravel())
print('실제 정답 : ', y_test[:5].astype(int))
