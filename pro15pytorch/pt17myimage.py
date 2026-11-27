# 손글씨 이미지 읽기
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import torch

im = Image.open("number.png")

# 이미지 크기 변경 및 흑백 전환(반전)
# mnist dataset의 크기가 28 * 28

img = im.resize((28, 28), Image.Resampling.LANCZOS).convert('L')

img_np = np.array(img)
print(img_np.shape)   # (28, 28)
print(img_np)

# 원본 이미지 시각화
plt.imshow(img_np, cmap='Greys')
plt.title('Original image')
plt.show()

# ndarray -> tensor화
img_tensor = torch.tensor(img_np, dtype=torch.float32)
print(img_tensor.shape)  # torch.Size([28, 28])
print(img_tensor)

# 정규화 : 0 ~ 255를 0 ~ 1로 변환
img_tensor = img_tensor / 255.0
print(img_tensor)

# 분류 모델에 넣를 때는 한 줄로 나란히 배치 - Flatten 방식
data = img_tensor.reshape(1, 784)
print(data)
print(data.shape)

# 정규화된 784열 텐서를 28 * 28 형태로 변환 후 다시 시각화
plt.imshow(data.reshape(28, 28), cmap='Greys')
plt.title('Normalized image')
plt.show()