# 딥러닝 모델 학습의 기본은
# - 입력 데이터를 모델에 전달해 예측 결과를 얻고
# - 지속적으로 그 결과와 실제값 간에 오차를 줄이기 위한 
#   모델의 파라미터(w, b)를 갱신하는 과정이다.

# 택시 요금 예측 모델 : y = 2x + 5  기본요금:5000원 + 거리당 2000 증가
def taxi_fare_model(distance):    # distance : 이동거리
    weight = 2   # 1km당 2천원
    bias = 5     # 기본요금:5000원
    fare = weight * distance + bias
    return fare

distance = 5   # 5km
predicted_fare = taxi_fare_model(distance)
print(f'{distance}km 이동 시 예상 택시 요금 : {predicted_fare},000원')
# 5km 이동 시 예상 택시 요금 : 15,000원

print('--------------') 
# '실제 택시 요금은 13,000이었다'라고 했을 때 모델이 예측한 값과 2000원 차이 남.
# 모델 오차 보정이 필요. 가중치 수정이 필요.

print("1) 직접 수식으로 구현")
actual_fare = 13
predicted_fare = 15
cost_error = predicted_fare - actual_fare
print(f'오차 : {cost_error}천원 (너무 비싸게 예측)')

print('역전파 작업 : 파라미터 갱신(가중치와 편향)')
# 기존 모델 파라미터
weight = 2; bias = 5; distance = 5
learning_rate = 0.01  # 학습률 : 1회 학습할 때 w, b를 얼마나 수정할 지 결정하는 값

weight = weight - learning_rate * cost_error * distance # 2 - 0.01 * 2 * 5 = 1.9
bias = bias - learning_rate * cost_error
print(f'새로운 weight : {weight:.2f}')   #  1.90
print(f'새로운 bias : {bias:.2f}')       #  4.98
# 새로운 가중치와 편향으로 다시 예측
new_predicted_fare = weight * distance + bias
print(f'새로운 예상 택시요금 : {new_predicted_fare:.2f}천원')  # 14.48천원

print('\n택시요금 모델 반복 학습 ( cost를 줄이익 위한 노력 )')
actual_fare = 13
weight = 2
bias = 5

for i in range(10):
    predicted_fare = weight * distance + bias # 현재 모델로 예측
    error = predicted_fare - actual_fare  # 실제값과의 오차
    print(f'{i + 1}회 학습 전 -> 예측: {predicted_fare:.2f}천원, 오차:{error:.2f}')
    
    # 오차를 이용해 w, b 갱신 (역전파를 통한 갱신)
    weight = weight - learning_rate * error * distance
    bias = bias - learning_rate * error

print('\n반복 완료')
print(f'최종 weight:{weight:.4f}, 최종 bias : {bias:.4f}')
# 최종 갱신된 w, b로 예측
final_fare = weight * distance + bias
print(f'반복 완료 후 최종 예상 택시 요금 : {final_fare:.2f}천원')

print("\n2) PyTorch lib를 사용")
import torch

# 택시 요금 모델   y = weight * distance + bias
distance = torch.tensor(5.0)    # 입력값 : 이동 거리 5km
actual_fare = torch.tensor(13.0)  # 실제 택시요금
# 학습해야할 값(w, b) : 미분을 사용
weight = torch.tensor(2.0, requires_grad=True)   # autograd
bias = torch.tensor(5.0, requires_grad=True)     # autograd
# Autograd는 신경망 학습을 위한 자동 미분 엔진으로, 
# requires_grad=True인 텐서의 연산을 추적하여 
# 동적 계산 그래프(DAG)를 만들고 .backward() 호출 시 연쇄 법칙으로 기울기를 자동 계산. 
learning_rate = 0.01    # 학습률

for i in range(10):
    # 1. 순전파(forward) : 현재 weight와 bias를 이용해 요금 예측
    predicted_fare = weight * distance + bias
    error = predicted_fare - actual_fare  # 오차
    loss = 0.5 * error ** 2   # 손실함수. 학습의 방향을 결정하기 위한 함수

    print(f'{i + 1}회 학습 전 -> 예측:{predicted_fare.item():.2f}천원, 오차:{error.item():.2f}, 손실:{loss.item():.4f}')
    # error: 예측값과 실제값의 단순한 차이
    # loss : 그 차이를 모델 학습에 사용할 수 있도록 수치화한 학습목표
    # 경사하강법은 error 자체가 아니라 loss가 최소가 되도록 w,b를 갱신

    # 2. 역전파(Backpropargation) : loss를 기준으로 w, b의 기울기를 자동 계산 (미분 사용)
    # 미분은 w, b를 조금 변화 시켰을 때 loss가 얼마나 변하는지를 알기 위해 사용한다.
    loss.backward()   # loss로 부터 거꾸로 계산하며 각 학습파라미터의 미분값을 자동으로 구해준다.
    print('weight의 기울기 : ', weight.grad.item()) # 기울기 > 0 우측으로 갈수록 loss 증가, 그럴때는 좌로 이동해야 loss 감소
    print('bias의 기울기 : ', bias.grad.item())

    # 가중치와 편향 수정 : gradient 계산 과정은 기록하지 않도록 no_grad 사용
    with torch.no_grad():  # with 블록 안에서 실행되는 계산은 자동미분 기록에서 제외하자
        weight -= learning_rate * weight.grad   # 가중치 수정
        bias -= learning_rate * bias.grad

    # 이전 gradient 초기화 : 왜냐하면 backward()를 실행할 때 gradient를 누적하기 때문
    weight.grad.zero_()
    bias.grad.zero_()

    print('학습 완료')
    print(f'최종 weight : {weight.item():.4f}')
    print(f'최종 bias : {bias.item():.4f}')

# 학습된 weight와 bias로 다시 요금 예측
final_fare = weight * distance + bias
print(f'최종 예상 택시 요금 : {final_fare.item():.2f}천원')

print("\n3) PyTorch 학습 코드 사용하여 모델을 생성")
import torch.nn as nn
import torch.optim as optim

# 택시 요금 모델 : w = weight * distance + bias
distance = torch.tensor([[5.0]])   # 입력값(이동거리), 2차원 형태 (nn.Linear가 입력을 2차원 형태를 원함)
actual_fare = torch.tensor([[13.0]])

# 모델 생성
model = nn.Linear(1, 1)   # 입력 1개, 출력 1개, 은닉층 없음
# 편의상 기존 예제와 동일하게 초기값 설정 : weight=2, bias=5
# 지금은 학습계산이 아니라 초기값을 직접 설정하는 작업이라 자동미분 기록 없다.
with torch.no_grad():
    model.weight.fill_(2.0)
    model.bias.fill_(5.0)

loss_fn = nn.MSELoss()   # 손실함수

# 옵티마이저 : weight, bias를 자동으로 수정
optimizer = optim.SGD(model.parameters(), lr=0.01)

for i in range(10):
    # 순전파
    predicted_fare = model(distance)
    error = predicted_fare.item() - actual_fare.item()  # 현재 예측 오차
    # 손실 계산
    loss = 0.5 * loss_fn(predicted_fare, actual_fare)
    print(f'{i + 1}회 학습 전 -> 예측:{predicted_fare.item():.2f}천원,'
        f'오차:{error:.2f}, 손실:{loss.item():.4f}')
    
    optimizer.zero_grad()  # 이전 gradient 초기화
    loss.backward()   # 역전파
    optimizer.step()  # weight, bias 실제 수정

print('학습 완료')
print(f'최종 weight : {model.weight.item():.4f}')
print(f'최종 bias : {model.bias.item():.4f}')

# 학습된 모델로 요금 예측
final_fare = model(distance)
print(f'최종 예상 택시 요금 : {final_fare.item():.2f}천원')