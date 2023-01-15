import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataprediksi.db'

db = SQLAlchemy(app)

class DataPrediksi(db.Model):
    id = db.Column(db.integer, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    jenis_pmks = db.Column(db.Integer(1), nullable=False)
    hubungan_dlm_keluarga = db.Column(db.Integer(1), nullable=False)
    jml_tanggungan_kepala_keluarga = db.Colum


@app.route("/")
def home():
    return render_template('prediksi.html')

@app.route("/predict", methods=["POST"])
def predict():
    int_features = [int(x) for x in request.form.values()]
    fitur = [np.array(int_features)]
    prediction = model.predict(fitur)
    return render_template("prediksi.html", prediction_text = "{}".format(prediction))

if __name__ == "__main__":
    app.run(debug=True)