import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

data = pd.read_csv("movie_data.csv")

print("First 5 rows of dataset:")
print(data.head())

plt.figure(figsize=(8,6))
sns.heatmap(data.select_dtypes(include=[np.number]).corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

target = "popularity"  
numeric_data = data.select_dtypes(include=[np.number])
correlations = numeric_data.corr()[target].drop(target)
best_var = correlations.abs().idxmax()

print("\nBest predictor variable for Y:", best_var)
print("Correlation value:", correlations[best_var])

X = data[[best_var]].values.reshape(-1,1)
y = data[target].values

model = LinearRegression()
model.fit(X, y)

intercept = model.intercept_
slope = model.coef_[0]

y_pred = model.predict(X)

mse = mean_squared_error(y, y_pred)
rms = np.sqrt(mse)

print("\nIntercept (b0):", intercept)
print("Slope (b1):", slope)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Square (RMS):", rms)
