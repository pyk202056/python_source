"""
* 카이제곱 검정
카이제곱 문제1) 부모학력 수준이 자녀의 진학여부와 관련이 있는가?를 가설검정하시오
칼럼 중 level - 부모의 학력수준, pass - 자녀의 대학 진학여부
조건 :  level, pass에 대해 NA가 있는 행은 제외한다.
"""
import pandas as pd
import scipy.stats as stats

#귀무: 부모 학력이 자녀 진학과 관련이 없다
#대립: 부모 학력이 자녀 진학과 관련이 있다 

data=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/cleanDescriptive.csv")
# print(data.head())

ctab=pd.crosstab(index=data['level'],columns=data['pass'])
# pd.crosstab은 두 범주형 열의 조합별 개수를 세어서 2차원 표로 만들어 주는 함수
# crosstab은 기본적으로 NA인 행을 집계에서 빼
# 한 변수의 분포만 보는 경우 (적합도 검정)	불필요	value_counts()로 충분
print("범주형 표(ctab)",ctab,'\n')

#result=stats.chisquare(data)
result=stats.chi2_contingency(ctab)
print("독립검정 카이제곱",result,'\n')
#statistic=2.7669512025, pvalue=0.2507056840, dof=2,

# 판정: 유의수준 0.05 < p 0.2507 이므로 유의수준을 크게 상회함. 
# 통계적으로 유의미하지 않음. 귀무 채택
# 부모 학력이 자녀 진학과 관련이 없다
