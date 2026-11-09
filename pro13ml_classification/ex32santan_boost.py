# 산탄데르 은행 관련 데이터로 고객만족 여부 분류
# label(class, y)명은 TARGET이고 0:만족, 1:불만족

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from xgboost import XGBClassifier
from xgboost import plot_importance

df = pd.read_csv('train_bank.csv', encoding='latin-1')
print(df.head(2))
print(df.shape)    # (76020, 371)
print(df.info())   # dtypes: float64(111), int64(260)

# 전체 데이터에서 만족과 불만족의 비율
print(df['TARGET'].value_counts())
unsatisfied_cnt = df[df['TARGET'] == 1].TARGET.count()
total_cnt = df['TARGET'].count()
print(f'불만족의 비율은 {unsatisfied_cnt / total_cnt}')  # 0.0395685

# pd.set_option('display.max_columns', None)
print(df['var3'].describe())   # min -999999.000000 이상치
df['var3'] = df['var3'].replace(-999999, 2)  # 현재 중앙값으로 대체
print(df['var3'].describe())
df.drop('ID', axis=1, inplace=True)   # ID는 식별자이므로 제거
print(df.describe())
print(df.shape)   # (76020, 370)

# feature / label 분리
x_features = df.iloc[:, :-1]
y_label = df.iloc[:, -1]

# train / test split
x_train,x_test,y_train,y_test = train_test_split(x_features, y_label, test_size=0.2, random_state=0)
print(x_train.shape, x_test.shape)  # (60816, 369) (15204, 369)
train_cnt = y_train.count()
test_cnt = y_test.count()
print('학습데이터 레이블값 분포 비율:', y_train.value_counts() / train_cnt)
# 0  0.960964, 1  0.039036
print('검증데이터 레이블값 분포 비율:', y_test.value_counts() / test_cnt)
# 0  0.9583,   1  0.0417

print()
# 모델
xgb_clf = XGBClassifier(n_estimators=50, random_state=12, eval_metric='auc')
xgb_clf.fit(x_train, y_train, eval_set=[(x_test, y_test)], verbose=True)  
# eval_set=[] 학습진행 중 성능 평가용 매개변수 지정 - validation 역할
# 학습은 x_train, y_train로 진행하고, 학습 도중 x_test, y_test로 성능 확인
xgb_roc_score = roc_auc_score(y_test, xgb_clf.predict_proba(x_test)[:, 1])
print(f'xgb_roc_score : {xgb_roc_score:.5f}')   #  0.83019
# 클래스 불균형이 심한 경우에는 roc_auc_score()가 효과적이다.
print()
pred = xgb_clf.predict(x_test)
print('예측값 : ', pred[:5])
print('실제값 : ', y_test[:5].values)
print('분류 정확도 : ', accuracy_score(y_test, pred))   # 0.9580373
# roc_auc : 만족과 불만족을 얼마나 잘 구분하는가?
# accuracy : 전체 고객중 얼마나 맞혔는가?
# recall : 실제 불만족 고객을 얼마나 찾아냈는가?
# precision : 불만족이라고 예측한 고객 중 실제 불만족 비율은?
# 불만족 고객을 놓치지 않는 것이 중요하다면 recall도 살펴보는 것을 권장


print('\nGridSearchCV로 최적의 파라미터 찾기 ---')
from sklearn.model_selection import GridSearchCV

xgb_clf2 = XGBClassifier(n_estimators = 10)
# max_depth:트리 깊이, min_child_weight:관측치 가중치합 최소, colsample_bytree:피처 비율
params = {
    'max_depth':[5, 7], 
    'min_child_weight':[1, 3], 
    'colsample_bytree':[0.5, 0.75]
}
gridcv = GridSearchCV(xgb_clf2, param_grid=params)
gridcv.fit(x_train, y_train, eval_set=[(x_test, y_test)])
print('gridcv 최적 파라미터:', gridcv.best_params_)
# {'colsample_bytree': 0.75, 'max_depth': 5, 'min_child_weight': 1}

print()
best_clf = XGBClassifier(n_estimators = 10, random_state=12,
    colsample_bytree=0.75, max_depth=5, min_child_weight=1)
best_clf.fit(x_train, y_train)

xgb_roc_score2 = roc_auc_score(y_test, 
                    best_clf.predict_proba(x_test)[:, 1])
print(f'xgb_roc_score2 : {xgb_roc_score2:.5f}')  # 0.84268

pred2 = best_clf.predict(x_test)
print('예측값 : ', pred2[:5])
print('실제값 : ', y_test[:5].values)
print('분류 정확도 : ', accuracy_score(y_test, pred2))  # 0.9584319

from sklearn.metrics import recall_score
recall = recall_score(y_test, pred2)
print('recall(재현율) : ', recall)
# 0.004731 : 실제 불만족 고객 중 약 0.47%만 불만족으로 예측했다는 의미

# 참고 ---
# 지금처럼 불만족 고객이 약 4%인 데이터에서는 Accuracy, ROC-AUC, Recall을 
# 함께 확인하는 것이 좋다. 
# 특히 실제 불만족 고객을 얼마나 놓치지 않고 찾아내는지가 중요하다면 
# Recall에 주목하자.