import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pickle
import os
import json

load_dotenv()

app = Flask(__name__)
silpi = pickle.load(open("silpi.pkl", "rb"))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#db.create_all()

class DataPrediksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    tempat_lahir = db.Column(db.String(15), nullable=False)
    pendidikan = db.Column(db.String(4), nullable=False)
    no_hp = db.Column(db.Integer, nullable=False)
    jabatan = db.Column(db.String(20), nullable=False)
    penempatan = db.Column(db.String(20), nullable=False)
    lama_kerja = db.Column(db.String(20), nullable=False)
    kehadiran = db.Column(db.Integer, nullable=False)
    sikap = db.Column(db.Integer, nullable=False)
    tanggung_jawab = db.Column(db.Integer, nullable=False)
    pencapaian = db.Column(db.Integer, nullable=False)


@app.route("/")
def home():
    print("Konek teu nya ", db.session.execute('SELECT 1'))
    return render_template('prediksi.html')
    
@app.route("/table")
def table():
    data = DataPrediksi.query.all()
    return render_template('table.html', data=data)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.get
    fitur = [np.array([
        int(data("kehadiran")),
        int(data("sikap")),
        int(data("tanggung_jawab")),
        int(data("pencapaian"))
    
    ])]
    prediction = silpi.predict(fitur)
    populate_data = DataPrediksi(
        nama=data("nama"),
        jenis_kelamin=data("jenis_kelamin"),
        tempat_lahir=data("tempat_lahir"),
        pendidikan=data("pendidikan"),
        no_hp=data("no_hp"),
        jabatan=data("jabatan"),
        penempatan=data("penempatan"),
        lama_kerja=data("lama_kerja"),
        kehadiran=data("kehadiran"),
        sikap=data("sikap"),
        tanggung_jawab=data("tanggung_jawab"),
        pencapaian=data("pencapaian"),
        keputusan=prediction
    )

    db.session.add(populate_data)
    db.session.commit()
    return redirect("/table")

if __name__ == "__main__":
    app.run(debug=True)