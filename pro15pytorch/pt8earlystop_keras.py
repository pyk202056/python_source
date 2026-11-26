# Keras 3 + PyTorch Backend 방식으로 코드 작성
# Keras 3를 사용하면 TensorFlow/Keras의 개발 편의성과 PyTorch의 연산 엔진을 함께 활용할 수 있다.
# 하지만 아직은 Keras 3와 PyTorch를 결합하는 방식까지 보편적이지 않다.

# python -m pip install -U keras

# 딥러닝으로 다중 비선형회귀 - autompg dataset
# Keras 3 + PyTorch Backend
# 조기 종료(Early Stopping) : 검증 손실이 개선되지 않을 때 학습을 중단
# 불필요한 학습을 줄이고, Overfitting을 방지하기 위한 방법 중 하나

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['KERAS_BACKEND'] = 'torch'  # 반드시 keras import 전에 설정

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.metrics import r2_score

import torch
from torch.utils.data import TensorDataset, DataLoader, random_split

import keras
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

# Backend 확인
print('Keras version :', keras.__version__)
print('Backend :', keras.backend.backend())  # torch

# 재현성 설정
keras.utils.set_random_seed(123)

# data loading 
datas = pd.read_csv(
    "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/auto-mpg.csv",
    na_values='?'
)

print(datas.head(2))
del datas['car name']

# 결측치 확인 및 제거
print(datas[datas.isna().any(axis=1)])
datas = datas.dropna()
print(datas.isna().sum())

# 편의상 일부 칼럼 제거
datas.drop(
    ['cylinders', 'displacement', 'acceleration', 'model year', 'origin'],
    axis='columns', inplace=True
)
print(datas.head(1))

# train / test split : 샘플링으로 처리 
train_dataset = datas.sample(frac=0.7, random_state=123)
test_dataset = datas.drop(train_dataset.index)

print(train_dataset.shape)  # (274, 3)
print(test_dataset.shape)   # (118, 3)

# 표준화 계산 : (요소값 - 평균) / 표준편차
train_stat = train_dataset.describe()
train_stat.pop('mpg')  # 종속변수는 빼고 ...
train_stat = train_stat.transpose()
print(train_stat)

def stdscale_func(x):
    return (x - train_stat['mean']) / train_stat['std']

# label 분리
train_label = train_dataset.pop('mpg')
test_label = test_dataset.pop('mpg')

# train / test 데이터 표준화
st_train_data = stdscale_func(train_dataset)
st_test_data = stdscale_func(test_dataset)

print(st_train_data[:3])
print(st_test_data[:3])

# tensor로 변환 
x_data = torch.tensor(st_train_data.values, dtype=torch.float32)
y_data = torch.tensor(train_label.values, dtype=torch.float32).view(-1, 1)

x_test = torch.tensor(st_test_data.values, dtype=torch.float32)
y_test = torch.tensor(test_label.values, dtype=torch.float32).view(-1, 1)

# TensorDataset : feature와 label을 한 쌍으로 구성
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
batch_size = 32  # 미니배치 크기

test_dataset = TensorDataset(x_test, y_test)

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
vali_loader = DataLoader(vali_subset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(len(train_loader), len(vali_loader), len(test_loader))  # 7 2 4

# 모델 정의 : Keras API로 신경망을 구성하고 실제 연산은 PyTorch가 수행
model = Sequential([
    Input(shape=(2,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1)  # 회귀 모델이므로 linear activation
])

model.summary()
print('전체 파라미터 수 :', model.count_params())  # 641

# 손실함수와 옵티마이저 정의
model.compile(
    optimizer=Adam(learning_rate=0.001),loss='mse',metrics=['mae']
)

# 조기 종료 설정 
# patience : 검증 손실이 개선되지 않을 때 기다리는 epoch 수
# restore_best_weights : 가장 성능이 좋았던 모델의 파라미터 복원
early_stop = EarlyStopping(
    monitor='val_loss', mode='min', patience=10,
    restore_best_weights=True, verbose=1
)

# 모델 학습 : PyTorch의 DataLoader를 Keras의 fit()에 직접 전달
# 순전파, 역전파, gradient 초기화, 파라미터 갱신 등을 자동 처리
history = model.fit(
    train_loader, validation_data=vali_loader, epochs=5000,
    callbacks=[early_stop], verbose=2
)

# 모델 평가 
ev_loss, ev_mae = model.evaluate(test_loader, verbose=0)

# test 데이터 전체 예측
pre = model.predict(test_loader, verbose=0).ravel()
actual = y_test.numpy().ravel()

print('\n모델 평가 결과')
print(f'MSE : {ev_loss:.5f}')
print(f'RMSE : {np.sqrt(ev_loss):.5f}')
print(f'MAE(평균절대오차) : {ev_mae:.5f}')
print(f'설명력 : {r2_score(actual, pre):.5f}')

# history 값을 DataFrame에 저장 
histDf = pd.DataFrame(history.history)
histDf['epoch'] = range(1, len(histDf) + 1)
print(histDf.head(3))
print(histDf.tail(3))
print(histDf.columns)

# 검증 손실이 가장 낮았던 epoch은?
best_epoch = np.argmin(histDf['val_loss']) + 1
print('전체 학습 횟수 :', len(histDf))
print('최적 학습 횟수 :', best_epoch)
print('최소 validation loss :', histDf['val_loss'].min())

# 모델 학습 정보 시각화 
def plt_history(histDf):
    plt.figure(figsize=(10, 8))

    # MAE, MSE 시각화
    for i, (metric, title, unit) in enumerate([
        ('mae', '평균 절대 오차(MAE)', 'mpg'),
        ('loss', '평균 제곱 오차(MSE)', 'mpg²')
    ], start=1):

        plt.subplot(2, 1, i)
        plt.plot(histDf['epoch'], histDf[metric], label='train')
        plt.plot(histDf['epoch'], histDf['val_' + metric], label='validation')

        # 최적 모델 시점 표시
        plt.axvline(
            x=best_epoch, color='red', linestyle='--',
            label=f'Best Epoch : {best_epoch}'
        )

        plt.xlabel('Epoch')
        plt.ylabel(unit)
        plt.title(title)
        plt.legend()
        plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

plt_history(histDf)

# 실제값과 예측값 비교 시각화 
plt.figure(figsize=(7, 7))
plt.scatter(actual, pre, alpha=0.7)

min_value = min(actual.min(), pre.min())
max_value = max(actual.max(), pre.max())

# 최적 모델 저장 
# EarlyStopping의 restore_best_weights=True에 의해 최적 모델의 파라미터가 복원된 상태
model_path = './mpg_bestmodel.keras'
model.save(model_path)
print('최적 모델 저장 완료 :', model_path)

# 저장된 모델 읽기
loaded_model = keras.models.load_model(model_path)
loaded_model.summary()

# 기존 데이터로 예측 
pred_5 = loaded_model.predict(x_test[:5], verbose=0)

print('\n기존 데이터로 예측')
print('예측값 :', pred_5.ravel())
print('실제값 :', y_test[:5].numpy().ravel())

# 새로운 데이터로 예측 
new_data = pd.DataFrame({
    'horsepower': [111, 155],
    'weight': [2222, 4444]
})

# 학습 시 표준화를 했으므로 새 자료도 표준화
new_st_data = stdscale_func(new_data)
print('표준화 결과 :', new_st_data)

# 텐서로 변환
new_tensor = torch.tensor(new_st_data.values, dtype=torch.float32)

# 새로운 데이터 예측
new_pred = loaded_model.predict(new_tensor, verbose=0)

print('\n새로운 데이터로 예측')
print('새 값 예측 결과 :', new_pred.ravel())

# 새로운 데이터와 예측 결과를 함께 출력
new_data['예측연비(mpg)'] = new_pred.ravel()
print(new_data)