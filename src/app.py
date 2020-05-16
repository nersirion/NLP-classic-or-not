import joblib
from flask import Flask, render_template, url_for, request
import pandas as pd
from utils import clean_text, check_len_tokens, final_check

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
def predict():

    tfidf = joblib.load("TfIdf.joblib")
    lr = joblib.load("TfIdf-LogReg.joblib")
    if request.method == "POST":
        message = request.form["message"]
        text = [message]
        text = clean_text(text)
        if not check_len_tokens(text) and final_check(text):
            matrix = tfidf.transform([text])
            my_prediction = lr.predict(matrix)
        else:
            my_prediction = 2
    return render_template("result.html", prediction=my_prediction)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
