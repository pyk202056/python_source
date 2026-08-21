# 문제 2 ---------------------------------
def inputfunc():
    datas = [
        "새우깡,15",
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas


def solution_func():
    # 상품별 단가
    price_by_name = {
        "새우깡": 450,
        "감자깡": 300,
        "양파깡": 450
    }

    # 주문 데이터
    arr_items = inputfunc()

    # 상품별 총 수량 : {key표현식: value표현식 for 변수 in 반복가능객체}
    count_by_name = {name: 0 for name in price_by_name}

    # 상품별 총 금액
    amount_by_name = {name: 0 for name in price_by_name}

    # 주문별 결과를 저장할 리스트
    order_table = []

    # 주문 데이터 처리
    for item in arr_items:
        # "새우깡,15" → "새우깡", "15"
        name, count = item.split(",")

        count = int(count)
        price = price_by_name[name]
        amount = count * price

        # 상품별 누적 수량
        count_by_name[name] += count

        # 상품별 누적 금액
        amount_by_name[name] += amount
        # 주문별 결과 저장
        order_table.append([name,count,price,amount])

    # 주문 내역 출력
    print("출력 형태:")
    print(f"{'상품명':<6} {'수량':>6} {'단가':>6} {'금액':>8}")
    print("-" * 35)

    for item in order_table:
        print(
            f"{item[0]:<6} "
            f"{item[1]:>6} "
            f"{item[2]:>6} "
            f"{item[3]:>8}"
        )

    # 상품별 소계
    print("\n소계")
    total_count = 0
    total_amount = 0

    for name in price_by_name:
        print(
            f"{name} : "
            f"{count_by_name[name]}개   "
            f"소계액 : {amount_by_name[name]}원"
        )

        total_count += count_by_name[name]
        total_amount += amount_by_name[name]

    # 전체 총계
    print("\n총계")
    print(f"총 수량 : {total_count}")
    print(f"총 액   : {total_amount}")

solution_func()
