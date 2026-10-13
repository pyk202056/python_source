# 통계량 : 데이터의 특징을 하나의 숫자로 요약한 것
# 표본 데이터를 추출해 표본 통계량을 구한 후 이를 근거로 전체(모집단), 미래의 경험하지 못한 데이터를 짐작 가능.
# 평균, 분산, 표준편차 등을 사용

grades = [1, 3, -2, 4]   # 표본 데이터. 변량

def show_grades(grades):
    for g in grades:
        print(g, end = " ")

show_grades(grades)
print()

def grades_sum(grades):
    tot = 0
    for g in grades:
        tot += g
    return tot

print('합은 ', grades_sum(grades))

def grades_ave(grades):
    ave = grades_sum(grades) / len(grades)
    return ave

print('평균은 ', grades_ave(grades))

# 분산(편차 제곱의 평균) : 평균값 기준으로 다른 값들의 흩어진 정도
def grades_variance(grades):
    ave = grades_ave(grades)
    vari = 0
    for su in grades:
        vari += (su - ave) ** 2

    return vari / len(grades)
    # return vari / (len(grades) -1)

print('분산은 ', grades_variance(grades))

# 표준편차 : 분산에 루트를 씌운 값
def grades_std(grades):
    return grades_variance(grades) ** 0.5

print('표준 편차는 ', grades_std(grades))

print('\n넘파이 모듈이 지원하는 함수 사용')
import numpy
print('합은 ', numpy.sum(grades))
print('평균은 ', numpy.mean(grades))
print('분산은 ', numpy.var(grades))
print('표준 편차는 ', numpy.std(grades))
