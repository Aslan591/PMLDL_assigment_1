import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

TRAIN_PATH = os.path.join("data", "processed", "train.csv")
TEST_PATH = os.path.join("data", "processed", "test.csv")
MODEL_PATH = os.path.join("models", "model.joblib")

TARGET = "Survived"
CATEGORICAL_FEATURES = ["Sex", "Embarked", "Pclass"]
NUMERIC_FEATURES = ["Age", "SibSp", "Parch", "Fare"]


def build_pipeline():
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ],
        remainder="passthrough",
    )
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def train():
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    features = CATEGORICAL_FEATURES + NUMERIC_FEATURES
    X_train, y_train = train_df[features], train_df[TARGET]
    X_test, y_test = test_df[features], test_df[TARGET]

    mlflow.set_experiment("titanic-survival")

    with mlflow.start_run():
        pipeline = build_pipeline()
        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds),
            "recall": recall_score(y_test, preds),
            "f1": f1_score(y_test, preds),
        }

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(pipeline, "model")

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)

        print("Metrics:", metrics)
        print(f"Model saved to {MODEL_PATH}")

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(pipeline, "model")

        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)

if __name__ == "__main__":
    train()