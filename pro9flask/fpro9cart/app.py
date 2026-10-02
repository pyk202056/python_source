from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__);

app.secret_key = "abcd1234"
app.permanent_session_lifetime = timedelta(minutes=5)  # 세션 만료 시간 5분

products = [
    {"id":1,"name":"노트북","price":3500000},
    {"id":2,"name":"물티슈","price":3500},
    {"id":3,"name":"종이컵","price":350},
    {"id":4,"name":"볼펜","price":1500},
]

@app.route("/")
def product_list():
    return render_template("products.html", products=products)

@app.route("/cart")
def show_cart():   # cart 목록 보기
    cart = session.get("cart", {})
    total = sum(info["price"] * info["qty"] for info in cart.values())  # 금액 = 단가*수량
    return render_template("cart.html", cart=cart, total=total)

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    # print("product_id : ", product_id)

    # 세션 cart가 없으면 빈 dict 생성
    cart = session.get("cart", {})

    # next(..., None) : 묶음형 자료에서 다음 값 1개를 꺼내는 함수
    # 주문 상품이 product에 기억됨
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return "주문 상품을 찾을 수 없어요", 404

    # 주문 상품이 상품목록에 있으면 장바구니에 추가
    item_name = product["name"]

    if item_name in cart:
        cart[item_name]["qty"] += 1  # 카트에 동일 상품이 있는 경우는 수량만 증가
    else:
        cart[item_name] = {"price":product["price"], "qty":1}
        # 카트에 최초 상품일 경우는 수량 1 (qty 요소(key) 생성)

    session["cart"] = cart  # 변수 cart를 세션 "cart" 키에 값으로 저장
    session.permanent = True  # 5분 만료 적용

    return redirect(url_for("show_cart"))   # cart에 저장 후 장바구니(cart 목록) 보기로 이동

# 장바구니 부분 삭제
@app.route("/remove/<item_name>")
def remove_to_cart(item_name):
    cart = session.get("cart")   # 세션에서 여러 개의 key중 "cart" key값 모두 읽어 변수에 저장

    if item_name in cart:  
        del cart[item_name]   # 변수 cart 목록에서 부분삭제 상품명을 지움

    session["cart"] = cart    # 부분 삭제된 변수 cart를 다시 세션에 "cart" key에 덮어쓰기
    return redirect(url_for("show_cart"))

# 장바구니 비우기
@app.route("/clear")
def clear_cart():
    session.pop("cart", None)  # 세션의 여러 개 키 중에서 "cart"라는 키를 추출 (삭제의 효과)
    return redirect(url_for("show_cart"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);