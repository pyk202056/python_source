from flask import Flask, render_template, request

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/get_form")
def get_form():
    return render_template("get_form.html");

@app.route("/get_result")
def get_result():
    name = request.args.get("username")  # get방식 요청 자료 받기
    age = request.args.get("age")     # '23' 문자 타입으로만 받기
    age = age + "살"
    return render_template("get_result.html", name=name, age=age)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);