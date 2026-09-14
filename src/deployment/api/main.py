import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.path.join("models", "model.joblib")

app = FastAPI(title="Titanic Survival API")
model = joblib.load(MODEL_PATH)


class PassengerData(BaseModel):
    Sex: str
    Embarked: str
    Pclass: int
    Age: float
    SibSp: int
    Parch: int
    Fare: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: PassengerData):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    return {
        "survived": bool(prediction),
        "probability": float(probability),
    }