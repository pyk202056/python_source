# 동물의 타입 분류
# zoo.csv -------------
# Attribute Information: (name of attribute and type of value domain)

# animal_name: Unique for each instance
# hair Boolean
# feathers Boolean
# eggs Boolean
# milk Boolean
# airborne Boolean
# aquatic Boolean
# predator Boolean
# toothed Boolean
# backbone Boolean
# breathes Boolean
# venomous Boolean
# fins Boolean
# legs Numeric (set of values: {0,2,4,5,6,8})
# tail Boolean
# domestic Boolean
# catsize Boolean
# class_type Numeric (integer values in range [1,7])

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

# 데이터 읽기
datas = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/zoo.csv")
print(datas.head(3))
print(datas.info())

# feature / label 분리
x_data = datas.iloc[:, :-1].astype('float32').values
y_data = datas.iloc[:, -1].astype('int64').values
print('feature 첫번째 : ', x_data[0], x_data.shape)    # (101, 16)
print('label 첫번째 : ', y_data[0], y_data.shape)      # 0 (101,)
print('label의 종류 : ', sorted(set(map(int, y_data)))) # [0, 1, 2, 3, 4, 5, 6]

np.random.seed(42)
torch.manual_seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('사용장치 : ', device)

original_labels = sorted(set(y_data))
label_to_index = {label:idx for idx, label in enumerate(original_labels)}
index_to_label = {idx:label for label, idx in label_to_index.items()}
y_data_index = np.array([label_to_index[label] for label in y_data], dtype=np.int64)
print('원본 라벨 목록:', original_labels)
print('라벨 -> 인덱스 매핑 : ', label_to_index)
print('인덱스 - > 라벨 매핑 : ', index_to_label)
nb_classes = len(original_labels)
print('클래스 갯수 : ', nb_classes)
print('y_data_index : ', y_data_index)

# train / test split
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data_index, test_size=0.2, random_state=42, stratify=y_data_index
)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)  # (80, 16) (21, 16) (80,) (21,)

# ndarray를 tensor화
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# 배치 처리 준비
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 모델
class ZooModel(nn.Module):
    def __init__(self, input_dim, nb_classes):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            # 드롭아웃은 딥러닝 모델의 과적합을 막기 위해 학습 과정에서 일부 뉴런을 무작위로 비활성화하는 기법

            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(p=0.3),

            nn.Linear(16, nb_classes)
        )

    def forward(self, x):
        return self.net(x)

model = ZooModel(input_dim=x_train.shape[1], nb_classes=nb_classes).to(device=device)
print(model)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


# 학습
epochs = 100
train_loss_history = []
train_acc_history = []

for epoch in range(epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch_x, batch_y in train_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * batch_x.size(0)

        pred = torch.argmax(outputs, dim=1)
        correct += (pred == batch_y).sum().item()
        total += batch_y.size(0)

    avg_loss = total_loss / total
    avg_acc = correct / total
    train_loss_history.append(avg_loss)
    train_acc_history.append(avg_acc)
    print(f'Epoch [{epoch + 1:03d} / {epochs}], loss:{avg_loss:.4f}, acc:{avg_acc:.4f}')

# 모델 평가
model.eval()

with torch.no_grad():
    x_test_device = x_test_tensor.to(device)
    y_test_device = y_test_tensor.to(device)

    test_outputs = model(x_test_device)
    test_loss = criterion(test_outputs, y_test_device)
    test_pred = torch.argmax(test_outputs, dim=1)
    test_acc = (test_pred == y_test_device).float().mean()

print(f'\nloss:{test_loss.item():.4f}, acc:{test_acc.item():.4f}')  # loss:0.3791, acc:0.8095

# 시각화
plt.plot(train_loss_history, label='train loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()
plt.show()

plt.plot(train_acc_history, label='train accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend()
plt.show()

# 혼동행렬 및 분류 리포트
y_pred_index = test_pred.cpu().numpy()
y_true_index = y_test_tensor.numpy()
# 학습용 라벨 index를 원래 라벨로 복원
y_pred_original = np.array([index_to_label[idx] for idx in y_pred_index])
y_true_original = np.array([index_to_label[idx] for idx in y_true_index])
print('분류 리포트 : \n')
print(classification_report(y_true_original, y_pred_original))
print()
cm = confusion_matrix(y_true_original, y_pred_original, 
                    labels=original_labels)
print(cm)

# heatmap
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
            xticklabels=original_labels, yticklabels=original_labels)
plt.xlabel('predicted')
plt.ylabel('true')
plt.show()

print('\n새로운 값으로 예측 ---')
new_data = np.array(
    [[0.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]], dtype='float32'
)
new_tensor = torch.tensor(new_data, dtype=torch.float32).to(device=device)
model.eval()
with torch.no_grad():
    logits = model(new_tensor)
    probs = torch.softmax(logits, dim=1)
    pred_index = torch.argmax(probs, dim=1).item()
    pred_label = index_to_label[pred_index]

print('분류 예측 확률:', probs.cpu().numpy().ravel())
print('분류 예측 index : ', pred_index)
print('분류 예측 label : ', pred_label)