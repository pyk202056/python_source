# Computer Vision(opencv:Open Source Computer Vision 라이브러리 사용)

# pip install opencv-python
# conda install opencv-python

import cv2
print(cv2.__version__)   # 5.0.0

img1 = cv2.imread('test18ani.jpeg')
print(type(img1))  # <class 'numpy.ndarray'>

cv2.imshow('image test', img1)
cv2.waitKey()
cv2.destroyAllWindows()
# print('end')

# 다른 이름으로 저장
cv2.imwrite('test18ani2.jpg', img1)
cv2.imwrite('test18ani3.jpg', img1, [cv2.IMWRITE_JPEG_QUALITY, 10])  # 10 압축품질
# 100 → 화질 높음 / 파일 용량 큼
# 50  → 중간
# 10  → 화질 낮음 / 파일 용량 작음

# 이미지 크기 조정
img2 = cv2.resize(img1, (300, 100), interpolation=cv2.INTER_AREA)
cv2.imwrite('test18ani4.jpg', img2)

# 밝기, 상하좌우 회전, 자르기 .... 지원



