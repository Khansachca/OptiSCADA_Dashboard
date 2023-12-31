# -*- coding: utf-8 -*-
"""arthemisgrove.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19WCMFM9Iv_zZuabIghKX5oeHvwEuaTdZ

##library
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

"""## eksplorasi & visualisasi"""

url = "https://drive.google.com/uc?id=1tHVr4CLC-gk6SBodROXrNSWl_QgfSmTf"
df = pd.read_csv(url)
df.head()

plt.figure(figsize=(12, 6))
plt.scatter(df["Wind Speed (m/s)"], df["LV ActivePower (kW)"], alpha=0.5)
plt.xlabel('Kecepatan Angin (Wind Speed)')
plt.ylabel('LV ActivePower (kW)')
plt.title('Daya Aktif vs. Kecepatan Angin (Sebelum dilatih)')
plt.grid(True)
plt.show()

# Plot data sebelum dilatih
plt.figure(figsize=(12, 6))
plt.scatter(df['Wind Speed (m/s)'], df['Wind Direction (°)'], c=df['LV ActivePower (kW)'], s=10)
plt.title('Wind Speed vs Wind Direction (Sebelum Dilatih)')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Wind Direction (°)')
plt.colorbar()

# Memilih fitur dan target
features = ["Wind Speed (m/s)", "Wind Direction (°)"]
target = ["LV ActivePower (kW)"]
X = df[features].values
y = df[target].values

# Normalisasi data
scaler_x = StandardScaler()
scaler_y = StandardScaler()
scaler_x.fit(X)
scaler_y.fit(y)
X = scaler_x.transform(X)
y = scaler_y.transform(y)

# KFold cross validation
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
mse_scores = []

# Data setelah dilatih
df_after = df.copy()
# Tambahkan data dari dataset lain
df_after = pd.concat([df_after, pd.read_csv("https://drive.google.com/uc?id=19gfneVlgVQK3kFihdlHjCMo1mmvZuYRl&export")])
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Reshape input data to have three dimensions
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])



"""##modeling"""

# Membangun model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
model.add(LSTM(100, activation='relu'))
model.add(Dropout(0.2))  # Tambahkan dropout layer
model.add(Dense(100, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Melatih model
 model.fit(X_train, y_train, epochs=50, batch_size=64)

# Evaluasi model
mse_score = model.evaluate(X_test, y_test)
mse_scores.append(mse_score)

# Bentuk ulang data masukan menjadi tiga dimensi
df_after_transformed = scaler_x.transform(df_after[features])
df_after_transformed = df_after_transformed.reshape(df_after_transformed.shape[0], 1, df_after_transformed.shape[1])

# Prediksi pada data setelah dilatih
df_after['LV ActivePower (kW)'] = model.predict(df_after_transformed)

# Mean Squared Error (MSE) rata-rata
mse_mean = np.mean(mse_scores)
print(f"Mean Squared Error (MSE) rata-rata: {mse_mean}")

# Evaluasi model pada data pelatihan
loss_train = model.evaluate(X_train, y_train)
print(f"Mean Squared Error (MSE) pada data pelatihan: {loss_train}")

# Evaluasi model pada data pengujian
loss_test = model.evaluate(X_test, y_test)
print(f"Mean Squared Error (MSE) pada data pengujian: {loss_test}")

"""##prediksi"""

# Input dari pengguna
wind_speed = float(input('Masukkan kecepatan angin (m/s): '))
wind_direction = float(input('Masukkan arah angin (°): '))
input_array = np.array([[wind_speed, wind_direction]])
input_array = scaler_x.transform(input_array)
input_array = input_array.reshape((1, input_array.shape[0], input_array.shape[1]))
# Prediksi
predictions = model.predict(input_array)
predictions_denorm = scaler_y.inverse_transform(predictions)
print(f"Prediksi LV ActivePower (kW): {predictions_denorm[0][0]}")

# Reshape input data to have three dimensions
df_after_transformed = scaler_x.transform(df_after[features])
df_after_transformed = df_after_transformed.reshape(df_after_transformed.shape[0], 1, df_after_transformed.shape[1])
df_after['LV ActivePower (kW)'] = model.predict(df_after_transformed)
mse_mean = np.mean(mse_scores)
print(f"Mean Squared Error (MSE) rata-rata: {mse_mean}")

# Membuat grafik wind speed vs lv active power
plt.figure(figsize=(10, 6))
plt.scatter(df_after['Wind Speed (m/s)'], df_after['LV ActivePower (kW)'])
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('LV ActivePower (kW)')
plt.title('Wind Speed vs LV ActivePower')
plt.show()

# Plot data setelah dilatih
df_after_transformed = scaler_x.transform(df_after[features])
df_after_transformed = df_after_transformed.reshape(df_after_transformed.shape[0], 1, df_after_transformed.shape[1])
df_after['LV ActivePower (kW)'] = model.predict(df_after_transformed)
mse_mean = np.mean(mse_scores)
print(f"Mean Squared Error (MSE) rata-rata: {mse_mean}")

plt.figure(figsize=(10, 6))
plt.scatter(df_after['Wind Speed (m/s)'], df_after['Wind Direction (°)'], c=df_after['LV ActivePower (kW)'], s=10)
plt.title('Data Setelah Dilatih')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Wind Direction (°)')
plt.colorbar()

plt.show()