import os
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_PATH = os.path.join("data", "raw", "titanic.csv")
TRAIN_PATH = os.path.join("data", "processed", "train.csv")
TEST_PATH = os.path.join("data", "processed", "test.csv")


def remove_outliers_iqr(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return df[(df[column] >= lower) & (df[column] <= upper)]


def prepare_data():
    df = pd.read_csv(RAW_PATH)

    df = df.drop(columns=["Cabin", "Ticket", "Name", "PassengerId"], errors="ignore")

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    df = remove_outliers_iqr(df, "Fare")
    df = remove_outliers_iqr(df, "Age")

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)
    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)
    print(f"train: {train_df.shape}, test: {test_df.shape}")


if __name__ == "__main__":
    prepare_data()