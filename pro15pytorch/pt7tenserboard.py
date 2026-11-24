# 텐서보드는 머신러닝 실험에 필요한 시각화 및 도구를 제공합니다.
# 손실 및 정확도와 같은 측정항목 추적 및 시각화
# 모델 그래프(작업 및 레이어) 시각화
# 시간의 경과에 따라 달라지는 가중치, 편향, 기타 텐서의 히스토그램 확인
# 저차원 공간에 임베딩 투영
# 이미지, 텍스트, 오디오 데이터 표시
# 그 외 다양한 도구 제공

# python -m pip install tensorboard

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

from sklearn.datasets import load_diabetes
from torch.utils.tensorboard import SummaryWriter
import datetime
import os

# data load
diabetes = load_diabetes()
xdata = diabetes.data
ydata = diabetes.target.reshape(-1, 1)
print(xdata[:2], ' ', xdata.shape)  # [[ 0.03807591  0.05068012 ...  (442, 10)
print(ydata[:2], ' ', ydata.shape)  # [[151.] [ 75.]]  (442, 1)
print('feature names : ', diabetes.feature_names)  
# ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']


