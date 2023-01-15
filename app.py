import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/dataprediksi"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.create_all()

class DataPrediksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)
    layak = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    jenis_pmks = db.Column(db.Integer, nullable=False)
    hubungan_dlm_keluarga = db.Column(db.Integer, nullable=False)
    jml_tanggungan_kepala_keluarga = db.Column(db.Integer, nullable=False)
    pendapatan_keluarga = db.Column(db.Integer, nullable=False)
    status_rumah = db.Column(db.Integer, nullable=False)
    pekerjaan = db.Column(db.Integer, nullable=False)


@app.route("/")
def home():
    print("Konek teu nya ", db.session.execute('SELECT 1'))
    return render_template('prediksi.html')

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.get
    fitur = [np.array([
        int(data("jenis_pmks")),
        int(data("hubungan_dlm_keluarga")),
        int(data("jml_tanggungan_kepala_keluarga")),
        int(data("pendapatan_keluarga")),
        int(data("status_rumah")),
        int(data("pekerjaan"))
    ])]
    prediction = model.predict(fitur)
    populate_data = DataPrediksi(
        nama=data("nama"),
        alamat=data("alamat"),
        jenis_pmks=data("jenis_pmks"),
        hubungan_dlm_keluarga=data("hubungan_dlm_keluarga"),
        jml_tanggungan_kepala_keluarga=data("jml_tanggungan_kepala_keluarga"),
        pendapatan_keluarga=data("pendapatan_keluarga"),
        status_rumah=data("status_rumah"),
        pekerjaan=data("pekerjaan"),
        layak=prediction
    )

    db.session.add(populate_data)
    db.session.commit()

    return render_template("prediksi.html", prediction_text = "{}".format(prediction))

if __name__ == "__main__":
    app.run(debug=True)