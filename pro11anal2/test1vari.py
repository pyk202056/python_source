# 표준 편차, 분산의 중요성
# 두 반의 시험성적이 있을 때 "평균이 같다고 성적 분포가 동일한가?"
# 실제로 표준편차의 대소에 따라 성적 편차가 다를 수 있다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(42)

# 목표 평균
target_mean = 60
std_dev_small = 10
std_dev_large = 20

# 데이터 생성
class1_raw = np.random.normal(loc=target_mean, scale=std_dev_small, size=100)
class2_raw = np.random.normal(loc=target_mean, scale=std_dev_large, size=100)
print(class1_raw[:5])
print(class2_raw[:5])

# 평균 보정
class1_adj = class1_raw - np.mean(class1_raw) + target_mean
class2_adj = class2_raw - np.mean(class2_raw) + target_mean

print()
# 정수화 및 범위 제한  np.clip(배열, 최소값, 최대값)
class1 = np.clip(np.round(class1_adj), 10, 100).astype(int)
class2 = np.clip(np.round(class2_adj), 10, 100).astype(int)
print(class1)
print(class2)

# 통계 계산
mean1, mean2 = np.mean(class1), np.mean(class2)
std1, std2 = np.std(class1), np.std(class2)
var1, var2 = np.var(class1), np.var(class2)

print("1반 (성적 편차 적음)")
print(f"평균:{mean1}, 표준편차:{std1}, 분산:{var1}")
print("2반 (성적 편차 큼)")
print(f"평균:{mean2}, 표준편차:{std2}, 분산:{var2}")

# 자료를 파일로 저장
df = pd.DataFrame({
    'class':['1반'] * 100 + ['2반'] * 100,
    'score':np.concatenate([class1, class2])
})
print(df.head(3))
print(df.tail(3))
df.to_csv("test1.csv", index=False, encoding="utf-8-sig")

print("시각화 -------")
x1 = np.random.normal(1, 0.05, size=100)
x2 = np.random.normal(2, 0.05, size=100)

plt.figure(figsize=(10, 6))
plt.scatter(x1, class1, alpha=0.8, label=f"1반(평균={mean1:2f},표준편차={std1:2f})")
plt.scatter(x2, class2, alpha=0.8, label=f"2반(평균={mean2:2f},표준편차={std2:2f})")
plt.hlines(target_mean, 0.5, 2.5, colors='red', 
        linestyles='dashed', label=f"공통평균={target_mean}")
plt.xticks([1, 2], ["1반", "2반"])
plt.ylabel("시험 점수")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.boxplot([class1, class2], label=["1반", "2반"])
plt.grid(True)
plt.show()

# 국어 선생님 입장에서 말하기를
# 전통적 주장(귀무 가설) : 내가 가르치는 학생들의 점수는 매년 두 반의 국어 점수 평균(편차)에 차이가 없다.
# 누군가가 실험을 통해 데이터를 수집 후 두 반의 평균(편차) 점수에 차이가 있다. 라는 새로운 의견 제시
# 대립 가설 : 두 반의 국어 점수의 평균(편차)은 차이가 있다.
# 위 주장에 대해 누가 맞는지 가설검정을 통해 판정을 내릴 수 있다. 
# (t-test, anova를 사용)

from scipy import stats

# 독립표본 t검정
t_stat, p_value_t = stats.ttest_ind(class1, class2, equal_var=False)  # Welchi's test
print(f't-통계값 : {t_stat:.4f}')
print(f'p값 : {p_value_t:.4f}')

if p_value_t < 0.05:
    print("유의확률(p)가 유의수준(α, 95%신뢰구간에서 0.05) 보다 작으므로 두 반의 평균은 차이가 있다. 유의하다.")
else:
    print("유의확률(p)가 유의수준(α, 95%신뢰구간에서 0.05) 보다 크므로 두 반의 평균은 차이가 없다. 유의하지 않다.")




기술 통계 -------------------
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 1. Iris 데이터 불러오기
iris = sns.load_dataset('iris')

print("\n1. 데이터 확인 ---")
print(iris.head())
print("\n데이터 크기:", iris.shape)
print("\n자료형:", iris.dtypes)

data = iris.select_dtypes(include='number')   # 수치형 데이터만 추출

# 2. 기본 기술통계량
print("\n2. 기본 기술통계 ---")
print(data.describe())
print("\n평균: ", data.mean())
print("\n중앙값 : ", data.median())
print("\n최빈값 : ", data.mode().iloc[0])

# 3. 산포도 : 분산, 표준편차, 범위
print("\n3. 산포도 ---")
print("표본 분산:", data.var(ddof=1))
print("표본 표준편차:", data.std(ddof=1))
print("범위(최댓값 - 최솟값):", data.max() - data.min())

# 5. 왜도와 첨도 - 분포 형태
print("왜도:", data.skew())
print("첨도:", data.kurt())

# 6. 품종별 기술통계
print("\n6. 품종별 평균 : ", iris.groupby('species')[data.columns].mean())
print("\n품종별 표준편차 : ", iris.groupby('species')[data.columns].std())
print("\n품종별 개수 : ", iris['species'].value_counts())

# 7. 도수분포표 : sepal_length를 0.5cm 간격으로 구간화
print("\n7. 도수분포표 ---")
col = 'sepal_length'
bins = np.arange(4.0, 8.5, 0.5)

# 구간별 도수 계산
frequency = pd.cut( iris[col], bins=bins, right=False).value_counts().sort_index()
freq_table = pd.DataFrame({ '도수': frequency})

freq_table['상대도수'] = ( freq_table['도수'] / freq_table['도수'].sum())
freq_table['누적도수'] = freq_table['도수'].cumsum()
freq_table['누적상대도수'] = ( freq_table['상대도수'].cumsum())

print(freq_table)
print("\n도수 합계:", freq_table['도수'].sum())

# 8. 히스토그램
plt.figure(figsize=(9, 5))
plt.hist( iris[col], bins=bins, edgecolor='black',  alpha=0.8)
plt.title('Iris 꽃받침 길이 히스토그램')
plt.xlabel('꽃받침 길이(cm)')
plt.ylabel('도수')
plt.xticks(bins)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 도수분포표 CSV 저장
freq_table.to_csv( 'iris_frequency.csv', encoding='utf-8-sig')


# 평균과 중앙값의 차이: 평균은 극단적인 값에 영향을 받지만, 중앙값은 상대적으로 영향을 덜 받는다.
# 분산과 표준편차의 차이: 둘 다 데이터의 흩어짐을 나타내며, 표준편차는 원래 데이터와 같은 단위를 사용한다.
# 사분위수와 상자그림: Q1, Q2, Q3를 통해 데이터의 중앙 위치와 퍼짐을 이해할 수 있으며, IQR을 이용해 이상치 후보를 찾을 수도 있다.
# 도수분포표와 히스토그램: 표를 통해 구간별 개수를 확인하고, 그래프를 통해 데이터가 어디에 집중되어 있는지 직관적으로 파악할 수 있다.