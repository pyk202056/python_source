# 연산자와 기본 함수 - PyTorch 관련
import torch
import numpy as np

x = torch.tensor(7)
y = torch.tensor(13)

if x > y:
    result1 = torch.add(x, y)
else:
    result1 = torch.subtract(x, y)

print(result1)

if x > 5:
    result2 = "good"
elif x > 9:
    result2 = "nice"
else:
    result2 = "ok"

print(result2)

print('관계 연산 ---')
print(torch.eq(torch.tensor(1), torch.tensor(2)))  # =
print(torch.ne(torch.tensor(1), torch.tensor(2)))  # !=
print(torch.lt(torch.tensor(1), torch.tensor(2)))  # <
print(torch.gt(torch.tensor(1), torch.tensor(2)))  # >
print(torch.ge(torch.tensor(1), torch.tensor(2)))  # >=

print('논리 연산 ---')
print(torch.logical_and(torch.tensor(True), torch.tensor(False))) 
print(torch.logical_or(torch.tensor(True), torch.tensor(False))) 
print(torch.logical_not(torch.tensor(True))) 

print('유일값  ---')
kbs = torch.tensor([1, 2, 2, 3, 2])
val = torch.unique(kbs)
print('val : ', val)
val, idx = torch.unique(kbs, return_inverse=True)  # 인덱스 반환
print('val : ', val)
print('idx : ', idx)

print('reduce  ---')
ar = torch.tensor([[1.,2.],[3.,4.]])
print(torch.mean(ar).item())   # 전체평균 2.5
print(torch.mean(ar, dim=0).numpy())  # 각열 평균
print(torch.mean(ar, dim=1).numpy())  # 각행 평균
print(torch.max(ar).item())

print('reshape  ---')
t =  np.array([[[0,1,2],[3,4,5],[6,7,8],[9,10,11]]])
print(t.shape)   # (1, 4, 3)
t_tensor = torch.tensor(t)
print(t_tensor.shape)  # torch.Size([1, 4, 3])
print(torch.reshape(t_tensor, shape=(12,)))
print(torch.reshape(t_tensor, shape=(2, 6)))
print(torch.reshape(t_tensor, shape=(-1, 6)))  # 행 갯수 자동 결정
print(torch.reshape(t_tensor, shape=(2, -1)))  # 열 갯수 자동 결정

print('squeeze : 차원축소(shape에서 크기가 1인 차원을 제거) ---')
print(torch.squeeze(t_tensor))
print(torch.squeeze(t_tensor).shape)  # torch.Size([4, 3])

print()
t2 = np.array([[[0],[3],[6],[9]]])
t2_tensor = torch.tensor(t2)     # torch.Size([1, 4, 1])
print(t2_tensor.shape)
print(torch.squeeze(t2_tensor))  # tensor([0, 3, 6, 9])
print(torch.squeeze(t2_tensor).shape)  # torch.Size([4])

print('unsqueeze : 차원확대 ---')
tarr = torch.tensor([[1,2,3],[4,5,6]])
print(tarr.shape)   # torch.Size([2, 3])

sbs = torch.unsqueeze(tarr, dim=0)
print(sbs.shape)    # torch.Size([1, 2, 3])
print(sbs.numpy())
print()
sbs = torch.unsqueeze(tarr, dim=1)
print(sbs.shape)    # torch.Size([2, 1, 3])
print(sbs.numpy())
print()
sbs = torch.unsqueeze(tarr, dim=2)
print(sbs.shape)    # torch.Size([2, 3, 1])
print(sbs.numpy())
print()
sbs = torch.unsqueeze(tarr, dim=-1)   # 마지막 위치에 새 차원 추가
print(sbs.shape)    # torch.Size([2, 3, 1])
print(sbs.numpy())

print('type변환 : 자료형 변환')
num = torch.tensor([1,2,3])
print(num, num.dtype)  # tensor([1, 2, 3]) torch.int64
num2 = num.to(torch.float32)
print(num2, num2.dtype)

print('텐서 합치기 : torch.cat - 텐서 이어 붙이기, torch.stack - 텐서 쌓기')
t1 = torch.tensor([1, 2, 3])
t2 = torch.tensor([4, 5, 6])
cat_res = torch.cat((t1, t2), dim=0)
print(cat_res)   
print()   # tensor([1, 2, 3, 4, 5, 6])
stack_res = torch.stack((t1, t2), dim=0)
print(stack_res)
# tensor([[1, 2, 3],
#         [4, 5, 6]])

