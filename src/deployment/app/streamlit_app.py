import os
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("Titanic Survival Predictor")

sex = st.selectbox("Sex", ["male", "female"])
embarked = st.selectbox("Port of Embarkation", ["S", "C", "Q"])
pclass = st.selectbox("Passenger Class", [1, 2, 3])
age = st.number_input("Age", min_value=0.0, max_value=100.0, value=30.0)
sibsp = st.number_input("Siblings/Spouses Aboard", min_value=0, value=0)
parch = st.number_input("Parents/Children Aboard", min_value=0, value=0)
fare = st.number_input("Fare", min_value=0.0, value=30.0)

if st.button("Predict"):
    payload = {
        "Sex": sex,
        "Embarked": embarked,
        "Pclass": pclass,
        "Age": age,
        "SibSp": sibsp,
        "Parch": parch,
        "Fare": fare,
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result["survived"]:
                st.success(f"Survived! Probability: {result['probability']:.2%}")
            else:
                st.error(f"Did not survive. Survival probability: {result['probability']:.2%}")
        else:
            st.error(f"API error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not reach API at {API_URL}. Make sure the API is running.")