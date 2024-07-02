import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load the dataset
df = pd.read_csv('updated_fashion_data_2018_2022.csv')

# Features and target variable
X = df[['product_name', 'gender', 'category', 'color', 'age_group', 'season', 'price', 'material', 'sales_count', 'brand', 'discount']]
y = df['average_rating']

# One-hot encode categorical variables
X = pd.get_dummies(X, columns=['product_name', 'gender', 'category', 'color', 'age_group', 'season', 'material', 'brand'], drop_first=True)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

# Feature scaling
sc_X = StandardScaler()
sc_y = StandardScaler()

X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
y_train = sc_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()
y_test = sc_y.transform(y_test.values.reshape(-1, 1)).flatten()

# Train SVR model
svr_model = SVR(kernel='linear')
svr_model.fit(X_train, y_train)

# Predict on training data
y_train_pred = svr_model.predict(X_train)

# Predict on testing data
y_test_pred = svr_model.predict(X_test)

# Inverse transform predictions and actual values
y_train_pred = sc_y.inverse_transform(y_train_pred.reshape(-1, 1)).flatten()
y_test_pred = sc_y.inverse_transform(y_test_pred.reshape(-1, 1)).flatten()
y_train = sc_y.inverse_transform(y_train.reshape(-1, 1)).flatten()
y_test = sc_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

# Evaluate model on training data
train_mae = mean_absolute_error(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)

# Evaluate model on testing data
test_mae = mean_absolute_error(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
r2 = r2_score(y_test, y_test_pred)

print(f'Training MAE: {train_mae}')
print(f'Training MSE: {train_mse}')
print(f'Test MAE: {test_mae}')
print(f'Test MSE: {test_mse}')
print(f'R-squared: {r2}')

# Visualize results
plt.scatter(y_test, y_test_pred, color='blue')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linewidth=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('SVR: Actual vs Predicted')
plt.show()


joblib.dump(svr_model,'rating.pkl')