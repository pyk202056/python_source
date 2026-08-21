# 문제 1 ---------------------------------
from datetime import datetime

# 직원 데이터 입력
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas


# 급여 처리
def processfunc(datas):
    # 현재 연도 자동으로 가져오기
    current_year = datetime.now().year
    # current_year = 2026

    # 직원별 급여 계산
    for data in datas:
        emp_no, name, base_pay, hire_year = data

        # 근무 연수 계산
        work_years = current_year - hire_year

        # 근속 수당 계산
        if work_years <= 3:
            bonus = 150000
        elif work_years <= 8:
            bonus = 450000
        else:
            bonus = 1000000

        # 총 급여
        salary = base_pay + bonus

        # 공제율 결정
        if salary >= 3000000:
            tax_rate = 0.5
        elif salary >= 2000000:
            tax_rate = 0.3
        else:
            tax_rate = 0.15

        # 공제액
        tax = int(salary * tax_rate)

        # 실수령액
        net_pay = salary - tax

        # 계산 결과 추가
        data.extend([
            work_years,
            bonus,
            tax,
            net_pay
        ])

    # 결과 출력
    print("사번  이름    기본급    근무년수  근속수당  공제액    수령액")
    print("-" * 70)

    for data in datas:
        print(
            f"{data[0]:<4} "
            f"{data[1]:<6} "
            f"{data[2]:<8} "
            f"{data[4]:<8} "
            f"{data[5]:<8} "
            f"{data[6]:<8} "
            f"{data[7]}"
        )

    print("-" * 70)
    print(f"처리 건수 : {len(datas)}건")


# 프로그램 실행
datas = inputfunc()
processfunc(datas)
