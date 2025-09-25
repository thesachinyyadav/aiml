import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

np.random.seed(42)
n_samples = 500

feature1 = np.random.randint(0, 2, n_samples)
feature2 = np.random.randint(0, 2, n_samples)
outcome = np.random.randint(0, 2, n_samples)

df = pd.DataFrame({
    "Feature1": feature1,
    "Feature2": feature2,
    "Outcome": outcome
})

X = df[["Feature1", "Feature2"]]
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1
)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

st.title("Coin Toss Predictor (ML Simulation)")
st.write("This app simulates coin toss prediction using Logistic Regression.")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Model Performance")
st.write("Accuracy:", acc)
st.write("Confusion Matrix:")
st.write(cm)

st.subheader("Try Your Own Toss")
f1 = st.selectbox("Choose Feature1", [0, 1])
f2 = st.selectbox("Choose Feature2", [0, 1])

if st.button("Predict Toss"):
    new_data = pd.DataFrame({"Feature1": [f1], "Feature2": [f2]})
    prediction = model.predict(new_data)[0]
    result = "Heads" if prediction == 1 else "Tails"
    st.success("Predicted Toss: " + result)
