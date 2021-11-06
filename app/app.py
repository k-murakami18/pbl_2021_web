# Flaskとrender_template（HTMLを表示させるための関数）をインポート
# test 
from flask import Flask, render_template, request
from models import scraping
 
import matplotlib.pyplot as plt
import numpy as np

import base64
from io import BytesIO

# Flaskオブジェクトの生成
app = Flask(__name__)


# 「/」へアクセスがあった場合の処理
@app.route("/")
# 「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/next.html', methods=["POST"])
def post():
    user_id = request.form["name"]
    df_user = scraping.scraping(user_id)
    
    #追加
    fig = plt.figure(figsize=None, facecolor='white')
    plt.rcParams['font.family'] = "MS Gothic"
    ax = fig.add_subplot(111)

    data = df_user['rating']
    ax.hist(data, bins=10, rwidth=0.9)

    ax.set_title('自分の視聴映画の評価の分布')
    ax.set_xlabel('評価')
    ax.set_ylabel('度数')
    ax.set_xticks([x-0.5 for x in range(1, 6)], minor=True)
    ax.set_xticks(range(0,6), minor=False)
    ax.set_xticklabels([x-0.5 for x in range(1, 6)], color='gray', minor=True)
    ax.set_xticklabels(range(0,6), fontsize=12, minor=False)

    ax.grid()

    io = BytesIO()
    fig.savefig(io, format="png")
    # base64 形式に変換する。
    io.seek(0)
    img = base64.b64encode(io.read()).decode()
    #ここまで

    df_values = df_user.values.tolist()
    return render_template('/next.html', user_id=user_id, df_values=df_values, ax=ax, img=img)


if __name__ == "__main__":
    app.run(debug=True)