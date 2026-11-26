# 딥러닝으로 다중선형회귀 - autompg dataset
# 조기 종료 (Early Stopping) : loss에 성능이 어느 순간 개선되지 않을 때 학습을 중단
# 불필요한 학습을 줄이고, Overfitting을 방지하기 위한 방법 중 하나

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import r2_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
import copy

# 재현성 설정
torch.manual_seed(123)
np.random.seed(123)

# data loading
datas = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/auto-mpg.csv", na_values='?')
print(datas.head(2))
del datas['car name']
print(datas[datas.isna().any(axis=1)])
datas = datas.dropna()
print(datas.isna().sum())

# 편의상 일부 칼럼 제거
datas.drop(
    ['cylinders','displacement','acceleration','model year','origin'],
    axis='columns', inplace=True
)
print(datas.head(1))
#     mpg  horsepower  weight
# 0  18.0       130.0    3504

# train / test split : 샘플링으로 처리
train_dataset = datas.sample(frac=0.7, random_state=123)
test_dataset = datas.drop(train_dataset.index)
print(train_dataset[:1], train_dataset.shape)  # (274, 3)
print(test_dataset[:1], test_dataset.shape)    # (118, 3)

# 표준화 계산 : (요소값 - 평균) / 표준편차
train_stat = train_dataset.describe()
train_stat.pop('mpg')  # 종속변수는 빼고 ...
print(train_stat)
train_stat = train_stat.transpose()
print(train_stat)

def stdscale_func(x):
    return (x - train_stat['mean']) / train_stat['std']

# train 데이터 표준화
st_train_data = stdscale_func(train_dataset)
st_train_data = st_train_data.drop(['mpg'], axis='columns')
print(st_train_data[:3])

# test 데이터 표준화
st_test_data = stdscale_func(test_dataset)
st_test_data = st_test_data.drop(['mpg'], axis='columns')
print(st_test_data[:3])

# label 분리
train_label = train_dataset.pop('mpg')
print(train_label[:3])
test_label = test_dataset.pop('mpg')
print(test_label[:3])

# tensor로 변환
x_data = torch.tensor(st_train_data.values, dtype=torch.float32)
y_data = torch.tensor(train_label.values, dtype=torch.float32).view(-1, 1)  # 2차원 텐서화

x_test = torch.tensor(st_test_data.values, dtype=torch.float32)
y_test = torch.tensor(test_label.values, dtype=torch.float32).view(-1, 1)  # 2차원 텐서화

# train -> train / validation 으로 분리
dataset = TensorDataset(x_data, y_data)

# train / validation split 
dataset_size = len(dataset)
vali_size = int(dataset_size * 0.2)
train_size = dataset_size - vali_size

train_subset, vali_subset = random_split(
    dataset, [train_size, vali_size],
    generator=torch.Generator().manual_seed(123)
)
print(len(dataset), len(train_subset), len(vali_subset))  # 274 220 54

# DataLoader 생성
batch_size = 32   # 미니배치 크기

test_dataset = TensorDataset(x_test, y_test)

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
vali_loader = DataLoader(vali_subset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
print(len(train_loader), len(vali_loader), len(test_loader))  # 7 2 4

# 모델 정의
class MpgModel(nn.Module):
    def __init__(self):
        super().__init__()

        # layer 정의 : Fully Connected Layer
        self.hidden_layer1 = nn.Linear(2, 32)
        self.hidden_layer2 = nn.Linear(32, 16)
        self.output_layer = nn.Linear(16, 1)

        self.relu = nn.ReLU()

        """
        self.net = nn.Sequential(
            nn.Linear(2, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
        """

    def forward(self, inputs):
        # print('forward 실행 ~~~~~ : ', inputs.shape)

        # 데이터 흐름 정의 : 순전파(forward propagation)
        net = self.hidden_layer1(inputs)
        net = self.relu(net)
        net = self.hidden_layer2(net)
        net = self.relu(net)
        outputs = self.output_layer(net)

        return outputs

    """
    def forward(self, inputs):
        return self.net(inputs)
    """

model = MpgModel()
print(model)
print('전체 파라미터 수 : ', 
    sum(p.numel() for p in model.parameters() if p.requires_grad))  # 641

# 손실함수와 옵티마이저 정의
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
mae_metric = nn.L1Loss()  # 절대 평균오차(모델 성능 평가지표로 사용)

# 모델 학습 : epoch 마다 loss, mae를 기록, 조기종료 구현
# patience : 검증 손실이 개선되지 않을 때 기다리는 epoch 수
def train_modelFunc(
    model, train_loader, vali_loader, criterion, optimizer, epochs=5000, patience=10
):
    history = {
        "loss":[], "mae":[], "vali_loss":[], "vali_mae":[]
    }

    # 조기 종료 관련 변수1
    best_vali_loss = float('inf')  # 가장 낮은 검증 손실 저장용
    best_model_state = None        # 최적 모델의 상태 저장  
    best_epoch = 0   
    wait = 0     # 성능이 개선되지 않은 연속 횟수

    for epoch in range(epochs):
        model.train()  # 모델 학습 모드로 전환
        train_loss_sum = 0  # loss 누적
        train_mae_sum = 0   # mae 누적

        # DataLoader에서 데이터를 배치단위로 가져옴
        for x_batch, y_batch in train_loader:
            pred = model(x_batch)  # 예측값 계산(순전파)
            loss = criterion(pred, y_batch)  # 손실값 계산
            optimizer.zero_grad()  # 이전 gradient 초기화
            loss.backward()        # 역전파 
            optimizer.step()       # 파라미터 계산(weight, bias)

            # 배치별 평균 loss에 샘플 수를 곱해 누적. 마지막 배치의 데이터 수가 다를 수 있기 때문
            train_loss_sum += loss.item() * len(x_batch)
            # mae 계산은 평가지표이므로 gradient 계산 x
            with torch.no_grad():
                mae = mae_metric(pred, y_batch)

            train_mae_sum += mae.item() * len(x_batch)

        # 1개의 epoch에서 전체 샘플 기준 평균 loss, mae 계산
        train_loss = train_loss_sum / len(train_loader.dataset)
        train_mae = train_mae_sum / len(train_loader.dataset)

        # 학습 도중 모델 검증 : validation data 사용
        model.eval()  # 검증 / 평가 모드로 전환
        vali_loss_sum = 0
        vali_mae_sum = 0

        # 검증이므로 파라미터 갱신 안함(gradient 계산 x)
        with torch.no_grad():
            for x_vali, y_vali in vali_loader:
                vali_pred = model(x_vali)
                vali_loss = criterion(vali_pred, y_vali)
                vali_mae = mae_metric(vali_pred, y_vali)

                vali_loss_sum += vali_loss.item() * len(x_vali)
                vali_mae_sum += vali_mae.item() * len(x_vali)

        # 1개의 epoch에서 평균 validation loss, mae 계산
        vali_loss = vali_loss_sum / len(vali_loader.dataset)
        vali_mae = vali_mae_sum / len(vali_loader.dataset)

        # history에 학습 결과 기록
        history['loss'].append(train_loss)
        history['mae'].append(train_mae)
        history['vali_loss'].append(vali_loss)
        history['vali_mae'].append(vali_mae)

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1:5d}/{epochs}]'
                f'loss:{train_loss:.5f} '
                f'mae:{train_mae:.5f} '
                f'vali_loss:{vali_loss:.5f} '
                f'vali_mae:{vali_mae:.5f}'
            )

        # 조기 종료 처리 : train loss 보다는 validation loss를 기준으로 판단
        # 학습 중 특정지표가 더 이상 개선된지 않으면 학습을 중단!
        if vali_loss < best_vali_loss:
            best_vali_loss = vali_loss
            best_epoch = epoch + 1

            # state_dict() : 모델의 파라미터 및 등록된 버퍼 정보
            # 가장 좋은 모델의 상태를 복사해 저장 - deepcopy 사용
            best_model_state = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait += 1   # 손실이 개선되지 않았으므로 누적
            if wait >= patience:
                print(f'\n조기종료 발생 ~~~ 학습종료함 : {epoch + 1}')
                break

    # 최적 모델의 파라미터 복원 : 조기 종요와 상관없이 가장 성능이 좋은 모델로 복원
    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    print('\n학습 완료. 전체 학습 횟수:', len(history['loss']))
    print('최적 Epoch : ', best_epoch, ', 최소 validation loss:', best_vali_loss)
    
    return history


# 모델 학습 호출
history = train_modelFunc(
    model, train_loader, vali_loader, criterion, optimizer, 5000, 10
)

# 모델 평가 함수 (test dataset으로)
def evaluate_modelFunc(model, test_loader, criterion):
    model.eval()    # 평가 모드로 전환
    test_loss_sum = 0
    test_mae_sum = 0

    predictions = []  # 배치별 예측값 실제값 저장
    actuals = []

    with torch.no_grad():
        for x_batch, y_batch in test_loader:
            pred = model(x_batch)
            loss = criterion(pred, y_batch)
            mae = mae_metric(pred, y_batch)

            test_loss_sum += loss.item() * len(x_batch)
            test_mae_sum += mae.item() * len(x_batch)

            predictions.append(pred)
            actuals.append(y_batch)

    # 전체 test 데이터에 대한 평균 MSE, MAE
    test_loss = test_loss_sum / len(test_loader.dataset)
    test_mae = test_mae_sum / len(test_loader.dataset)

    # torch.cat() : 여러 텐서를 기존 차원으로 연결 (배치별로 저장된 텐서를 하나의 텐서화)
    # (32, 1), (32, 1), (32, 1), (22, 1) -> (118, 1)
    pred_tensor = torch.cat(predictions, dim=0)
    actual_tensor = torch.cat(actuals, dim=0)

    return test_loss, test_mae, pred_tensor, actual_tensor

# 모델 평가 함수 호출
ev_loss, ev_mae,  pred_tensor, actual_tensor = evaluate_modelFunc(
    model, test_loader, criterion
)

pre = pred_tensor.numpy().ravel()
actual = actual_tensor.numpy().ravel()

print('\n모델 평가 결과')
print(f'MSE:{ev_loss}, RMSE:{np.sqrt(ev_loss)}, MAE(평균절대오차):{ev_mae}')
print(f'설명력:{r2_score(actual, pre)}')

# history값을 DataFrame에 저장
histDf = pd.DataFrame(history)
histDf['epoch'] = range(1, len(histDf) + 1)
print(histDf.head(3))
print(histDf.tail(3))
print(histDf.columns)

# 검증 손실이 가장 낮았던 epoch은?
best_epoch = np.argmin(histDf['vali_loss']) + 1
print('최적 학습 횟수 : ', best_epoch)  # 133

# 모델 학습 정보 시각화
def plt_history(histDf):
    best_epoch = histDf.loc[histDf['vali_loss'].idxmin(), 'epoch']
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)   # MAE
    plt.plot(histDf['epoch'], histDf['mae'], label='train mae')
    plt.plot(histDf['epoch'], histDf['vali_mae'], label='validation mae')
    # 최적 모델 시점 표시
    plt.axvline(x=best_epoch, color='red', linestyle='--', 
                label = f'Best Epoch : {best_epoch}')
    plt.xlabel('Epoch')
    plt.ylabel('MAE[mpg]')
    plt.title('평균 절대 오차 (MAE)')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(2, 1, 2)   # MSE
    plt.plot(histDf['epoch'], histDf['loss'], label='train loss')
    plt.plot(histDf['epoch'], histDf['vali_loss'], label='validation loss')
    # 최적 모델 시점 표시
    plt.axvline(x=best_epoch, color='red', linestyle='--', 
                label = f'Best Epoch : {best_epoch}')
    plt.xlabel('Epoch')
    plt.ylabel('MSE[mpg]')
    plt.title('평균 제곱 오차 (MSE)')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

plt_history(histDf)

# 실제값과 예측값 비교 시각화 - 추세선(회귀선)
plt.figure(figsize=(7, 7))
plt.scatter(actual, pre, alpha=0.7)
min_value = min(actual.min(), pre.min())
max_value = max(actual.max(), pre.max())
plt.plot([min_value, max_value], [min_value, max_value], 
        'r--', label='예측값==실제값')
plt.xlabel('실제연비(mpg)')
plt.ylabel('예측연비(mpg)')
plt.axis('equal')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# 잔차(Residual) 분포 시각화
residual = actual - pre
plt.figure(figsize=(8, 4))
sns.histplot(residual, bins=20, kde=True)
plt.axvline(x=0, color='red', linestyle='--')
plt.xlabel('잔차')
plt.ylabel('빈도수')
plt.title('잔차 분포')
plt.grid(alpha=0.3)
plt.show()


# 최적 모델의 파라미터 복원된 상태이므로 모델 저장 후 읽기 -------
model_path = './mpg_bestmodel.pth'
torch.save(model.state_dict(), model_path)
print('최적 모델 저장 완료 : ', model_path)

# 저장된 모델 읽기
loaded_model = MpgModel()  # 저장시 사용한 모델과 동일 구조 객체 생성

loaded_model.load_state_dict(
    torch.load(model_path, weights_only=True, map_location='cpu')
)

# 예측을 위해 평가 모드로 전환
loaded_model.eval()
print('loaded_model : ', loaded_model)

# 기존 데이터로 예측
loaded_model.eval()
with torch.no_grad():
    pred_5 = loaded_model(x_test[:5])

print('예측값 : ', pred_5.numpy().ravel())
print('실제값 : ', y_test[:5].numpy().ravel())

print()
# 새로운 데이터로 예측
new_data = pd.DataFrame({
    'horsepower':[111, 155],
    'weight':[2222, 4444]
})
# 학습시 표준화를 했으므로 새 자료도 표준화
new_st_data = stdscale_func(new_data)
print('표준화 결과 : ', new_st_data)
# 텐서로 변환
new_tensor = torch.tensor(new_st_data.values, dtype=torch.float32)

loaded_model.eval()
with torch.no_grad():
    new_pred = loaded_model(new_tensor)

print('새 값 예측 결과 : ', new_pred.numpy().ravel())

# 새로운 데이터와 예측 결과를 함께 출력
new_data['예측연비(mpg)'] = new_pred.numpy().ravel()
print(new_data)