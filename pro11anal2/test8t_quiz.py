import numpy as np
import pandas as pd
import scipy.stats as stats

# [one-sample t 검정 : 문제1]  
# 영사기( 프로젝터 )에 사용되는 구형 백열전구의 수명은 250 시간이라고 알려졌다. 
# 한국 연구소에서 수명이 50 시간 더 긴 새로운 백열전구를 개발하였다고 발표하였다. 
# 연구소의 발표결과가 맞는지 새로 개발된 백열전구를 임의로 수집하여 수명 시간 관련 자료를 얻었다. 
# 한국 연구소의 발표가 맞는지 새로운 백열전구의 수명을 분석하라.
# 수집된 자료 :  305 280 296 313 287 240 259 266 318 280 325 295 315 278

# 문제 : 새로 개발된 백열전구의 수명은 300 시간인지 검정
# 귀무 : 한국 연구소에서 개발한 백열전구의 평균 수명은 300시간이다.
# 대립 : 한국 연구소에서 개발한 백열전구의 평균 수명은 300시간이 아니다.

data = [305, 280, 296, 313, 287, 240, 259, 266, 318, 280, 325, 295, 315, 278]
print("표본 평균 수명 : ", np.mean(data))   # 289.7857
print("표본 크기 : ", len(data))   # 14

# 정규성 검정
result = stats.shapiro(data)
print("shapiro result : ", result)  # pvalue=0.8208613 > 0.05 이므로 만족

t_result = stats.ttest_1samp(data, popmean=300)
print("t_result : ", t_result)  # statistic=-1.55643565, pvalue=0.1436062
# 해석 : pvalue=0.143606 > 0.05 귀무 채택
# 한국 연구소에서 개발한 백열전구의 평균 수명은 300시간이다

print("----------------")
# [one-sample t 검정 : 문제2] 
# 국내에서 생산된 대다수의 노트북 평균 사용 시간이 5.2 시간으로 파악되었다. 
# A회사에서 생산된 노트북 평균시간과 차이가 있는지를 검정하기 위해서 
# A회사 노트북 150대를 랜덤하게 선정하여 검정을 실시한다.  
# 실습 파일 : one_sample.csv
# 참고 : time에 공백을 제거할 땐 ***.time.replace("     ", ""),
#         null인 관찰값은 제거.

# 문제 : 국내 노트북 평균 사용 시간인 5.2 시간과 A회사 노트북 평균 사용 시간에 차이가 있는지 검정
# 귀무 : A회사 노트북 평균 사용은 5.2시간이다. (차이가 없다)
# 대립 : A회사 노트북 평균 사용은 5.2시간이 아니다. (차이가 있다)

data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/one_sample.csv")
print(data2.head(3))

# 전처리
print(data2.info())
data2['time'] = data2['time'].replace("     ", "").str.strip()  # 공백 제거
data2['time'] = pd.to_numeric(data2['time'], errors='coerce')   # str을 숫자로 변환
data2 = data2.dropna(subset=['time'])

print("표본 평균 사용 시간 : ", data2['time'].mean())  # 5.556880
print("표본 크기 : ", len(data2))   #  109

# 정규성 검정
result2 = stats.shapiro(data2['time'])
print("time에 대한 shapiro result : ", result2)  # pvalue=0.72423 > 0.05이므로 만족

# One sample t-test
t_result2 = stats.ttest_1samp(data2['time'], popmean=5.2)
print("t_result2 : ", t_result2) # statistic=3.946059566, pvalue=0.000141
# 해석 : pvalue=0.000141 < 0.05 귀무 기각
# A회사 노트북 평균 사용은 5.2시간이 아니다. 


print("----------------")
# [one-sample t 검정 : 문제3] 
# https://www.price.go.kr/tprice/portal/main/main.do 에서 
# 메뉴 중  가격동향 -> 개인서비스요금 -> 조회유형:지역별, 품목:미용 자료(엑셀)를 파일로 받아 미용 요금을 얻도록 하자. 
# 정부에서는 전국 평균 미용 요금이 15000원이라고 발표하였다. 이 발표가 맞는지 검정하시오. (월별)

# 문제 : 정부의 전국 평균 미용 요금이 15000원이라고 발표했는데 실제 데이터와 비교 검정
# 귀무 : 전국 평균 미용 요금은 15000원이다. (발표가 맞다)
# 대립 : 전국 평균 미용 요금은 15000원이 아니다. (발표가 틀리다)
# pip install xlrd

data3 = pd.read_excel('개인서비스지역별_동향.xls')
print(data3.head(3))
data4 = data3.iloc[0, 2:]    # 지역 데이터만 추출
data4 = pd.to_numeric(data4, errors='coerce')
data4 = data4.dropna()

print('표본 평균 미용 요금 :', data4.mean())  # 20232.5625
print('표본 크기 :', len(data4))  # 16

# 정규성 검정
result3 = stats.shapiro(data4)
print(result3)   # 0.3746942    정규성 만족

# one-sample t-test
t_result3 = stats.ttest_1samp(data4, popmean=15000)
print(t_result3)  # pvalue 1.8990407726371975e-06 < 0.05이므로 귀무 기각
# 전국 평균 미용 요금은 15000원보다 높다. 정부의 발표가 틀리다.
