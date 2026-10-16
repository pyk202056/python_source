# DataFrame의 재구조화 (열을 행으로, 행을 열로 ...)
import numpy as np
import pandas as pd

df = pd.DataFrame(1000 + np.arange(6).reshape(2, 3), 
            index=['대전','서울'], columns=['2023','2024','2025'])
print(df)

print()
# stack, unstack
df_row = df.stack()  # 열을 아래로 내려서 행 인덱스 쪽으로 쌓기 (가로로 펼쳐진 열을 세로로 쌓기)
print(df_row)
print()
df_col = df_row.unstack()  # 행 인덱스를 다시 열쪽으로 펼치기 (세로로 쌓인 인덱스를 다시 가로로 펼치기 )
print(df_col)

print('\n범주화 -----------')
price = [10.3, 5.5, 7.8, 3.6]
cut = [3, 7, 9 , 11]   # 구간 기준 값 (3개) - (3, 7], (7, 9], (9, 11]    (a, b] => a < x <= b
result_cut = pd.cut(price, cut)   # 연속형 -> 범주형 (구간별 그룹으로 분류)
print(result_cut)  # [(9, 11], (3, 7], (7, 9], (3, 7]]     (3, 7]은 3초과 7이하

result_cut = pd.cut(price, bins=cut, labels=['저가','중가','고가'])
print(result_cut)
print(pd.Series(result_cut).value_counts())

# pd.qcut() : 데이터 개수가 비슷하도록 문위수 기분 자동 분할

print('----')
datas = pd.Series(np.arange(1, 1001))
# print(datas)
print(datas[:5])
print(datas.head())   # 상동
print(datas.head(2))

print(datas[-2:])
print(datas.tail(2))  # 상동

print('\nagg 함수 : 범주의 그룹별 연산')
datas = pd.DataFrame({
    '부서':['개발','개발','영업','영업','인사','개발'],
    '이름':['길동','철수','영희','민수','유리','찬우'],
    '연봉':[4500, 4200, 4000, 4500, 3500, 3900],
    '성과점수':[90,85,70,75,88,95]
})
print(datas)
print()
print(datas.groupby('부서')['연봉'].mean())  # 부서별 연봉 평균
print(datas.groupby('부서')['이름'].count()) # 부서별 건수
print(datas.groupby('부서')[['연봉','성과점수']].mean()) # 부서별 연봉,성과점수 평균

pd.set_option('display.max_columns', None)
print(datas.groupby('부서')['연봉'].agg(['sum','mean','count']))  # 여러 집계함수 한 번에 처리

print()
# agg 대신 사용자 함수를 작성
data = pd.DataFrame({
    '연봉':[4500, 4200, 4000, 4500, 3500, 3900],
    '성과점수':[90,85,70,75,88,95]
})

def summaryFunc(gr):
    return {
        'count':gr.count(),
        'mean':gr.mean(),
        'std':gr.std(),
        'min':gr.min(),
    }

print(data.apply(summaryFunc))  # apply : 함수 실행용 함수

print('\nmerge : DataFrame 객체 병합 - 공통칼럼 기준 - RDBMS의 join 처럼')
df1 = pd.DataFrame({'data1':range(7), 'key':['b','b','a','c','a','a','b']})
print(df1)
df2 = pd.DataFrame({'key':['a','b','d'], 'data2':range(3)})
print(df2)
print()
print(pd.merge(df1, df2, on='key'))  # 교집합 (inner join)
print()
print(pd.merge(df1, df2, on='key', how='inner'))  # 교집합 (inner join)
print()
print(pd.merge(df1, df2, on='key', how='outer'))  # full outer join
print()
print(pd.merge(df1, df2, on='key', how='left'))  # left outer join
print()
print(pd.merge(df1, df2, on='key', how='right'))  # right outer join

print()
df3 = pd.DataFrame({'key2':['a','b','d'], 'data2':range(3)})
print(df3)
print(df1)
print(pd.merge(df1, df3, left_on='key', right_on='key2'))

print('--- concat : 상하 또는 좌우로 이어 붙이기 ---')
print(pd.concat([df1, df3], axis=0))  # 행단위
print()
print(pd.concat([df1, df3], axis=1))  # 열단위

print('\nPIVOT 연산 : pivot과 groupby 명령의 중간적 성격')
# pivot : 데이터 열 중에서 두 개의 열(key)을 사용해 데이터의 행열을 재구성
data = {'city':['강남','강북','강남','강북'],
        'year':[2000, 2001, 2002, 2002],
        'pop':[3.3, 2.5, 3.0, 2.0]
        }
df = pd.DataFrame(data)
print(df)
print(df['pop'].describe())
print()
print(df.pivot_table(index=['city']))
print(df.pivot_table(index=['city'], aggfunc='mean'))  # 상동
print(df.pivot_table(index=['city','year'], aggfunc=[len,'sum']))
print()
print(df.pivot_table(index=['city'], values='pop'))
print(df.pivot_table(index=['city'], values='pop', aggfunc='mean'))
print(df.pivot_table(index=['city'], values='pop', aggfunc=len))
print()
# 구조 재구성 ==> year:행, city:열, pop:계산값
print(df.pivot_table(index=['year'], values='pop', columns=['city']))
print(df.pivot_table(index=['year'], values='pop', columns=['city'], margins=True))
print(df.pivot_table(index=['year'], values='pop', columns=['city'], margins=True, fill_value=0))

print()
hap = df.groupby(['city'])
print(hap)
print(hap.sum())
print(df.groupby(['city']).sum())
print(df.groupby(['city']).mean())
