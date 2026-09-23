from flask import Flask, render_template

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/condition")
def condition():
    score = 85;
    return render_template("condition.html", score=score);

@app.route("/loop")
def loop():
    users = ["김찬우","김민채","제임스"]
    return render_template("loop.html", users=users);

@app.route("/filter")
def filter():
    message = "hello flask jinja2";
    price = 12345;
    return render_template("filter.html", message=message, price=price);

# jinja2에는 기본적으로 천단위 콤마가 없어서 직접 구현하거나 format 사용 가능
@app.template_filter('format')
def format_number(value):
    return format(value, ",")    # 숫자 세자리 마다 , 출력

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);