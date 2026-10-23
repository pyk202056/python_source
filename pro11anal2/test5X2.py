# 이원카이제곱(Chi-Square Test of Independence)-교차분할표 이용
#  : 두 개 이상의 변인(집단 또는 범주)을 대상으로 검정을 수행한다.
# 분석 대상의 집단 수에 의해서 독립성 검정과 동질성 검정으로 나뉜다.
# 독립성(관련성)검정- 동일 집단의 두 변인(학력수준과 대학 진학 여부)을 대상으로 관련성이 있는가없는가?- 독립성검정은두변수사이의연관성을검정한다.

# 실습: 교육수준과 흡연율 간의 관련성 분석 : smoke.csv

# 귀무 : 교육수준과 흡연율 간에 관계가 없다. (독립이다. 연관성이 없다)
# 대립 : 교육수준과 흡연율 간에 관계가 있다. (독립이 아니다. 연관성이 있다)

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/smoke.csv")
print(data.head(3))
print(data.tail(3))
print(data['education'].unique())   # [1 2 3]
print(data['smoking'].unique())     # [1 2 3]

# 학력수준별 흡연 빈도 수 : 교차표 작성
ctab = pd.crosstab(index=data['education'], columns=data['smoking'])  # 빈도 수
# ctab = pd.crosstab(index=data['education'], columns=data['smoking'], normalize=True)  # 비율로 출력
ctab.index = ['대학원졸','대졸','고졸']
ctab.columns = ['과흡연','보통','노담']
print(ctab)

# 이원카이제곱(독립성) 검정 시작
# chi_result = [ctab.loc['대학원졸'], ctab.loc['대졸'], ctab.loc['고졸']]
chi_result = ctab
chi2, pv, dof, expected = stats.chi2_contingency(chi_result)

print(f"chi2:{chi2:.7f}, pv:{pv:.7f}, dof:{dof}")
print(f"expected:\n{expected}")

# 판정1 : 유의수준:0.05 < p:0.000818 이므로 귀무 기각.
# 교육수준과 흡연율 간에 관계가 있다. smoke.csv(수집 자료)는 우연히 발생된 자료가 아니다.

# 판정2 : chi2:18.9109157, dof:4, cv:9.49
# chi2값이 임계치 우측에 있으므로(귀무 기각역) 귀무 기각. 대립 가설이 채택

print("\n\n독립성 검정 2---------------")
# 남성과 여성의 스포츠 음료 선호도 검정

# 귀무 : 성별과 음료 선호는 서로 관련이 없다.
# 대립 : 성별과 음료 선호는 서로 관련이 있다.

# 교차표 생성
data = pd.DataFrame({
    "포카리스웨트":[30, 20],
    "칠성사이다":[20, 30],
    "비타오백":[10, 30]
}, index=["남성", "여성"])

print(data)

chi2, pv, dof, expected = stats.chi2_contingency(data)
print("p-value : ", pv)  # 0.0033880
print("chi2 : ", chi2)   # 11.375
print("dof : ", dof)     # 2
print("expected : ", expected)

# 판정 : 유의수준 0.05 > p-value  0.0033880 이므로 귀무 기각
# 성별과 음료 선호는 서로 관련이 있다.

# 히트맵 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
sns.heatmap(data=data, annot=True, fmt='d', cmap="Blues")
plt.title("성별에 따른 음료 선호 분석")
plt.xlabel("음료 종류")
plt.ylabel("성별")
plt.show()
