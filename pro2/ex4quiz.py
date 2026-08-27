try:
    with open('sales.txt', mode='r', encoding='utf-8') as obj:
        employee_sales = {}  # 직원별 판매금액 담을 딕셔너리
        total_sales = 0      # 전체 판매금액

        print("날짜      이름    상품명   갯수    판매금액")

        for line in obj:
            line = line.strip()  # 줄바꿈 문자 제거

            if line:
                data = line.split(',') # 데이터 콤마(,) 단위로 쪼개기.

                date = data[0]
                name = data[1]
                product = data[2]
                quantity = int(data[3])
                price = int(data[4])
                amount = quantity * price # 각 판매금액

                print(f"{date} {name} {product} {quantity}개 {amount}원")
                
                if name in employee_sales:
                    employee_sales[name] += amount
                    # 이름이 같을 경우 판매금액을 더함
                else:
                    employee_sales[name] = amount  # 이름이 다를 경우 새로 추가

                total_sales = total_sales + amount # 전체 판매금액

    top_employee = max(employee_sales, key=employee_sales.get) # get을 이용하여 키를 통해 value값을 확인하여 가장 많이 판매한 사람을 찾음.
    top_amount = employee_sales[top_employee]  # 위 에서 찾은 판매왕의 키를 이용해 벨류 값 가져옴

    print(f"전체 판매 금액 : {total_sales}원")
    print(f"판매왕 : {top_employee}")

    # 파일 저장
    with open('sales_report.txt', mode='w', encoding='utf-8') as writes:
        writes.write("직원별 판매 실적\n\n")

        for name, amount in employee_sales.items():
            writes.write(f"{name} : {amount}원\n")

        writes.write(f'\n전체 판매 금액 : {total_sales:,}원\n')
        writes.write(f'판매왕 : {top_employee} ({top_amount:,}원)\n')

    print()

except Exception as e:
    print("error : ", e)