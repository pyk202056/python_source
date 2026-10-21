# 차트 영역 객체 선언시 인터페이스 유형 두 가지
import numpy as np
import matplotlib.pyplot as plt

# 1) 'Matplotlib 스타일' 인터페이스
x = np.arange(10)
plt.figure()
plt.subplot(2, 1, 1)   # row, column, panel_number
plt.plot(x, np.sin(x))
plt.subplot(2, 1, 2)   # row, column, panel_number
plt.plot(x, np.cos(x))
plt.show()

# 2) '객체 지향' 인터페이스 - 2행 1열
fig, ax = plt.subplots(nrows=2, ncols=1)
ax[0].plot(x, np.sin(x))
ax[1].plot(x, np.cos(x))
plt.show()

# 2) '객체 지향' 인터페이스 - 2행 2열
fig, ax = plt.subplots(nrows=2, ncols=2)
ax[0, 0].plot(x, np.sin(x))
ax[0, 1].plot(x, np.cos(x))
ax[1, 0].plot(x, np.tan(x))
ax[1, 1].plot(x, x ** 2)
plt.show()

# 차트(그래프)의 종류 일부 경험하기
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
# Histogram : 연속형 수치 데이터를 일정한 구간으로 나눠, 데이터의 개수(빈도)를 막대로 표현
ax1.hist(np.random.rand(100), bins=10, alpha=0.7)
ax2.plot(np.random.rand(100))
plt.show()

# 막대
data = [5, 8, 10, 9, 7]
plt.bar(range(len(data)), data)   
plt.show()

err = np.random.rand(len(data))
plt.barh(range(len(data)), data, alpha=0.8, xerr=err)   
plt.show()

# 원 : 데이터의 양이 적을 경우
plt.pie(data, colors=['yellow', 'blue', 'red'], explode=(0, 0.2, 0, 0.1, 0))
plt.title('pie chart')
plt.show()

# 박스 플롯 : 전체 데이터의 분ㅍ를 확인 하기에 효과적. 이상치 확인에 도움
data = [1, 50, 80, 100, 90, 70, 300]
plt.boxplot(
    data,
    widths=0.4,  # 상자 너비
    showmeans=True,
    meanline=False,   # 평균을 점으로 표시
    showfliers=True,  # 이상치 표시
    whis=1.5          # 수염 범위(IQR의 1.5배)
)
plt.ylabel('value')
plt.show()

# scatter(bubble chart) : 산점도 차트에 점의 크기를 동적으로 표시
n = 30
np.random.seed(0)
x = np.random.rand(n)
y = np.random.rand(n)
color = np.random.rand(n)
scale = np.pi * (np.random.rand(n) * 15) ** 2
plt.scatter(x, y, c=color, s=scale)
plt.show()

# 시계열 데이터로 선차트
import pandas as pd
fdata = pd.DataFrame(np.random.randn(1000, 4),
            index = pd.date_range('1/1/2000', periods=1000), 
            columns=list('abcd'))
print(fdata.head())
print(fdata.tail())
fdata = fdata.cumsum()
print(fdata.head(3))
plt.plot(fdata)
plt.show()

# pandas의 plot 기능
fdata.plot(kind='bar')  # <== 요거
plt.xlabel("time")
plt.ylabel("data")
plt.show()
