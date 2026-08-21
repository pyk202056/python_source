# 문제 3 ---------------------------------
products = { "노트북": 1500000, "모니터": 350000, "키보드": 80000, "마우스": 50000 } 

# 할인 함수 
discount10 = lambda price: int(price * 0.9) 
discount20 = lambda price: int(price * 0.8) 

def order(product, count, discount_func=None): 
    price = products[product] 
    total = price * count 
    if discount_func is not None: 
        total = discount_func(total) 

    return total 

print(order("노트북", 1)) 
print(order("키보드", 2, discount10)) 
print(order("모니터", 2, discount20))

orders = [ ("노트북", 1), ("키보드", 3), ("모니터", 2), ("마우스", 5) ]

result = sorted(orders, key=lambda x: products[x[0]] * x[1], reverse=True ) 
print(result)