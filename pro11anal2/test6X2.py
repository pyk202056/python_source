# 이원카이제곱
# 동질성 검정 - 두 집단의 분포가 동일한가? 다른 분포인가? 를 검증하는 방법이다. 분포 비율 차이 검정
# 두 집단 이상에서 각 범주(집단) 간의 비율이 서로 동일한가를 검정하게 된다.
# 두 개 이상의 범주형 자료가 동일한 분포를 갖는 모집단에서 추출된 것인지 검정하는 방법이다.

# 동질성 검정 실습1)
# 교육 방법에 따른 교육생들의 만족도 분석-동질성 검정 survey_method.csv

# 귀무 : 교육 방법에 따른 교육생들의 만족도에 차이가 없다.
# 대립 : 교육 방법에 따른 교육생들의 만족도에 차이가 있다.

import pandas as pd
import scipy.stats as stats

# 만족도에 대한 설문조사 수집 자료
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/survey_method.csv")
print(data.head(3))
print(data['method'].unique())  # [1 2 3]
print(data['survey'].unique())  # [1 2 3 4 5]

ctab = pd.crosstab(index=data['method'], columns=data['survey'])
ctab.index = ["방법1","방법2","방법3"]
ctab.columns = ["매우만족","만족","보통","불만족","매우불만족"]
print(ctab)

chi2, pv, dof, expected = stats.chi2_contingency(ctab)
print(f"chi2:{chi2}, pv:{pv}, dof:{dof}")
print("expected : \n", expected)   # 예측 비율

# 해석 : 유의수준 0.05 < pv 0.58645743 이므로 귀무채택. survey_method.csv는 우연히 발생한 자료라고 할 수 있다.

print("-------------")
# 동질성 검정실습2) 연령대별 sns 이용률의 동질성 검정
# 20대에서 40대까지 연령대별로 서로 조금씩 그 특성이 다른 SNS 서비스들에 대해
# 이용현황을 조사한 자료를 바탕으로 연령대 별로 홍보전략을 세우고자 한다.
# 연령대 별로 이용현황이 서로 동일한지 검정해 보도록 하자

# 귀무 : 연령대별 sns 서비스별 이용률 현황은 동일하다(동질이다).
# 대립 : 연령대별 sns 서비스별 이용률 현황은 동일하지 않다.
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/snsbyage.csv")
print(data2.head(3))

print(data2['age'].unique())      # [1 2 3] ==>  20, 30, 40
print(data2['service'].unique())  # ['F', 'T', 'K', 'C', 'E']

ctab2 = pd.crosstab(index=data2['age'], columns=data2['service'])
ctab2.index = ["20대","30대","40대"]
ctab2.columns = ['F', 'T', 'K', 'C', 'E']
print(ctab2)

chi2, pv, dof, expected = stats.chi2_contingency(ctab2)
print(f"chi2:{chi2}, pv:{pv}, dof:{dof}")
# chi2:102.75202494484225, pv:1.1679064204212775e-18

# 판정 : pv:1.1679064204212775e-18 < 0.05 이므로 귀무 기각
# "연령대별 sns 서비스별 이용률 현황은 동일하지 않다."는 의견을 인정함.

print("\n위 자료는 샘플 자료이지만 모집단 자료라 가정하고 샘플링 후 검정하기 ---")
# 전체자료와 샘플자료로 가설검정을 한 결과에 차리를 확인하기
print("전체 건수 : ", len(data2))      # 1439

samp_data = data2.sample(n=500, replace=True, random_state=1) \
            .reset_index(drop=True)   # 인덱스를 새로 부여
print("샘플 건수 : ", len(samp_data))  # 500

ctab3 = pd.crosstab(index=samp_data['age'], columns=samp_data['service'])
ctab3.index = ["20대","30대","40대"]
ctab3.columns = ['F', 'T', 'K', 'C', 'E']
print(ctab3)

chi2, pv, dof, expected = stats.chi2_contingency(ctab3)
print(f"chi2:{chi2}, pv:{pv}, dof:{dof}")
# chi2:36.20748437710444, pv:1.6088950709449814e-05   해석 결과는 동일
