# 다중선형회귀 : tv,radio,newspaper가 sales에 얼마나 영향을 주는지 파악

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
from sklearn.preprocessing import minmax_scale
import numpy as np
import pandas as pd

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head(2))
del data['no']
print(data.head(2))

fdata = data[['tv','radio','newspaper']]
# ldata = data[['sales']]
ldata = data.iloc[:, [3]]
print(fdata.head(2))
print(ldata[:2])

# feature 간 단위의 차이가 클 경우 정규화/표준화 작업이 모델 성능에 도움
# 정규화
fedata = minmax_scale(fdata, axis=0, copy=True)  # 행기준, 원본자료 보존
print(fedata[:3])

# train / test 분리
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(fedata, ldata, \
        shuffle=True, test_size=0.3, random_state=123)  # stratify는 회귀에서는 안줌
print(x_train[:2], x_train.shape)  # (140, 3)
print(x_test[:2], x_test.shape)    # (60, 3)

print()
# 전처리가 모두 끝난 경우 모델 설계 및 실행
model = Sequential()
model.add(Input(shape=(3, )))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='linear')) # activation 생략 가능
print(model.summary())

model.compile(
    optimizer=optimizers.Adam(learning_rate=0.01),
    loss='mse', 
    metrics=['mse']
)

history = model.fit(x_train, y_train, epochs=100, \
    batch_size=32, verbose=2,
    validation_split=0.2  # train data중 20%를 학습 중 검증용 사용
)

ev_loss = model.evaluate(x_test, y_test, verbose=0)
print('ev_loss : ', ev_loss)

# history 값 확인
# print('history : ', history.history)
# print('history val_loss : ', history.history['val_loss']) # validation_split이 있는 경우
# print('history val_mse : ', history.history['val_mse'])
# print('history loss : ', history.history['loss'])
# print('history mse : ', history.history['mse'])

# loss 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['val_loss'], label='val_loss')
plt.plot(history.history['loss'], label='loss')
plt.legend()
plt.show()

from sklearn.metrics import r2_score
print('설명력:', r2_score(y_test, model.predict(x_test))) # 0.78905

# predict
pred = model.predict(x_test[:5])
print('예측값 : ', pred.ravel())  
print('실제값 : ', y_test[:5].values.ravel())
# 예측값 :  [11.568753  8.204429 17.498812 12.249282 13.518066]
# 실제값 :  [11.4  8.8 14.7 10.1 14.6]
