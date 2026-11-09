# [로지스틱 분류분석 문제2] 
# 게임, TV 시청 데이터로 안경 착용 유무를 분류하시오.
# 안경 : 값0(착용X), 값1(착용O)
# 예제 파일 : https://github.com/pykwon  ==>  bodycheck.csv
# 새로운 데이터(키보드로 입력)로 분류 확인. 스케일링X
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/fa236a226b6cf7ff7f61850d14f087ade1c437be/testdata_utf8/bodycheck.csv")

print(data.head(3))
#    번호  게임   신장  체중  TV시청  안경유무
# 0     1    2    146    34      2     0
# 1     2    6    169    57      3     1
# 2     3    9    160    48      3     1

# train/test set 분리
x = data[['게임','TV시청']]
y = data['안경유무']
# print(x[:3])
# print(y[:3])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
# print(x_train[:3], '\n', x_test[:3], '\n', y_train[:3], '\n', y_test[:3])
# -- x
#     게임  TV시청
# 11   5     3
# 3    1     2
# 18   1     1
#      게임  TV시청
# 0    2     2
# 17   8     2
# 15   5     3
# -- y
#  11    1
# 3     0
# 18    0
# Name: 안경유무, dtype: int64
#  0     0
# 17    1
# 15    1
# Name: 안경유무, dtype: int64

# 모델 생성
model = LogisticRegression(C=0.06, solver='lbfgs', random_state=1)
model.fit(x_train, y_train)

# 분류
y_pred = model.predict(x_test)
print("예측값: ", y_pred)
# 예측값:  [0 1 1 1 1 0]
print("실제값: \n", y_test)
# 실제값:  
# 0     0
# 17    1
# 15    1
# 1     1
# 8     1
# 5     0
# Name: 안경유무, dtype: int64

print(f"총 갯수: {len(y_test)}, 오류 수:{(y_test != y_pred).sum()}")
# 총 갯수: 6, 오류 수:0
print("--- 분류 정확도 확인 ---")
print(f"{accuracy_score(y_test, y_pred)}")

# 모델 저장 후 읽기
import joblib                           
joblib.dump(model, 'glasses.pkl')
del model
read_model = joblib.load('glasses.pkl')

# 입력
game = float(input("게임 시간 입력: "))
tv = float(input("TV 시청 시간 입력: "))

new_data = pd.DataFrame([[game, tv]], columns=['게임', 'TV시청'])
new_pred = read_model.predict(new_data)
print("안경 착용 여부: ", "착용" if new_pred[0] == 1 else "미착용")
print()           
print(f"안경 착용 확률: {read_model.predict_proba(new_data)[0][1]*100:.2f}%") 