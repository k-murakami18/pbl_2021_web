# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
from models import scraping

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

    df_values = df_user.values.tolist()
    return render_template('/next.html', user_id=user_id, df_values=df_values)


if __name__ == "__main__":
    app.run(debug=True)
