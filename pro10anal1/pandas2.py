# 재색인 (순서 재배치)
from pandas import Series, DataFrame

# Series의 재색인
data = Series([1, 3, 2], index=(1, 4, 2))
print(data)
data2 = data.reindex((1, 2, 4))   # 내가 지정한 인덱스 순서대로 재배치
# data2 = data.reindex((2, 1, 4))
print(data2)

print('\n재색인할 때 값 채워넣기')
data3 = data2.reindex([0,1,2,3,4,5])  # 대응된 값이 없으면 NaN
print(data3)

# 대응값이 없는 인덱스에 특정값으로 채우기
data3 = data2.reindex([0,1,2,3,4,5], fill_value=777)
print(data3)

print()
# NaN 앞 값으로 NaN을 채우기
data3 = data2.reindex([0,1,2,3,4,5], method='ffill')  # data2 정렬된 상태여야함
print(data3)
data3 = data2.reindex([0,1,2,3,4,5], method='pad')
print(data3)

print()
# NaN 뒤(다음) 값으로 NaN을 채우기
data3 = data2.reindex([0,1,2,3,4,5], method='bfill')
print(data3)
data3 = data2.reindex([0,1,2,3,4,5], method='backfill')
print(data3)

import numpy as np
print('\nDataFrame : bool 처리')
df = DataFrame(np.arange(12).reshape(4, 3), 
        index=['1월','2월','3월','4월'], columns=['강남','강북','서초'])
print(df)

print(df['강남'])      # 해당 열 출력
print(df['강남'] > 3)  # True, False 출력
print(df[df['강남'] > 3])  # 조건이 참인 행만 출력
print()
print(df < 3)   # 전체자료 대상 bool 값 출력
df[df < 3] = 0  # 3 미만 자료는 0으로 대체
print(df)

print()
# 슬라이싱 관련 메소드
# df.loc['행(열)이름'] : 해당 행(열), df.iloc[행(열)번호] : 위치 기준 행(열)
print(df.loc['3월'])
print(df.loc['3월', :])
print(df.loc[:'2월'])   # 2월 이하 행
print(df.loc[:'2월', ['서초']])   # 2월 이하 행 '서초' 열

print()
print(df.iloc[2])   # 2행
print(df.iloc[2, :]) 
print()
print(df.iloc[:3])     # 3행 미만 행 모든 열
print(df.iloc[:3, 2])  # 3행 미만 행 2열
print(df.iloc[:3, 1:3])   # 3행 미만 행 1,2열
print(df.iloc[1:3, 1:3])  # 1,2행, 1,2열
