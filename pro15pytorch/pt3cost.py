# 비용함수(cost function) : 모델의 예측값과 실제값의 차이(오차)를 수치화하여 모델 성능 평가
# 최적의 w, b를 찾기 위해 역전파(backpropagation)로 계산 (경사 하강법)

# 최소제곱법 (전통적인 ML 모델에서 사용)
# : 예측값과 실제값의 오차 제곱합이 최소가 되도록 모델의 파라미터를 구하는 방법.
# 경사하강법 (DeepLearning 모델에서 사용)
# : 손실 함수의 기울기를 계산하여 파라미터를 반복적으로 갱신하는 최적화 알고리즘.

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'   # OpenMP 런타임 중복 우회

# 1. 비용 구하기 - numpy + math 사용
import math
import numpy as np

real = np.array([10, 9, 3, 2, 11])   # 실제값, 정답값
# pred = np.array([11, 5, 2, 4, 3])  # 모델 예측값,실제값과 차이가 큰 경우 (w, b 신뢰도 낮을 때)
pred = np.array([10, 8, 3, 4, 10])   # 모델 예측값,실제값과 차이가 작은 경우 (w, b 신뢰도 높을 때)

cost = 0

for i in range(len(real)):   # MSE(평균제곱오차) 직접 계산
    cost += math.pow(pred[i] - real[i], 2)
    print(cost)

print('cost : ', cost / len(real))

print('\n최적의 W(weightr, 가중치) 얻기 이해')
import torch
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 선형회귀 모델 수식 : hypothesis = w * x + b
# 여기서는 w를 자동으로 학습시키는 것이 아니라 직접 변경하며 각 w에서 cost의 변화 확인
x = torch.tensor([1,2,3,4,5], dtype=torch.float32)   # feature
y = torch.tensor([1,2,3,4,5], dtype=torch.float32)   # label
b = 0   # bias는 편의상 0으로 고정

w_val = []
cost_val = []

for i in range(-30, 50):
    feed_w = i * 0.1    # 0.1은 Learningrate(학습율)
    hypothesis = feed_w * x + b   # hypothesis = w * x + b
    cost = torch.mean(torch.square(hypothesis - y))  # MSE (비용함수 계산)

    cost_val.append(cost.item())
    w_val.append(feed_w)
    print(f'{i}: cost:{cost.item()}, weight:{feed_w}')

# w에 따른 cost 변화 시각화
plt.plot(w_val, cost_val, marker='o')
plt.xlabel('w(가중치)')
plt.ylabel('cost(손실, 비용)')
plt.title('가중치 w변화에 대한 비용함수 cost')
plt.grid()
plt.show()