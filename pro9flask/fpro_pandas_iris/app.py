from flask import Flask, render_template, request
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib 
import matplotlib
matplotlib.use('Agg') # Anti Grain Geometric : 이미지 저장시 오류 방지용(차트 출력없이 저장 시 사용)

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent  # 현재 파일의 경로
STATIC_DIR = BASE_DIR / 'static' / 'images'
STATIC_DIR.mkdir(parents=True, exist_ok=True)

df = sns.load_dataset("iris")  # 1회만 실행

@app.get("/")
def main():
    return render_template("main.html")

@app.get("/showdata")
def showdata():
    # print(df.head())
    irisdata = df.to_html()

    # pie chart 생성 및 저장(서버에서 자체 출력 X)
    counts = df['species'].value_counts().sort_index()

    plt.figure()
    counts.plot.pie(autopct='%1.1f%%', startangle=90, ylabel='')
    plt.tight_layout()

    img_path = STATIC_DIR / 'fpro_pandas.png'
    plt.savefig(img_path, dpi=130)   # 해상도
    plt.close()  # 메모리 자원 해제

    return render_template("show.html", 
                        irisdata=irisdata,
                        piechart = 'images/fpro_pandas.png'
    )

@app.get("/showdata2")
def showdata2():
    irisdata = df.to_html()
    counts = df['species'].value_counts().sort_index()

    # chart.js에 전달할 데이터
    labels = counts.index.to_list()  # js에서 읽기 위함
    values = counts.tolist()

    return render_template("show2.html", 
                        irisdata=irisdata,
                        labels = labels,
                        values = values
    )

if __name__ == '__main__':
    app.run(debug=True)