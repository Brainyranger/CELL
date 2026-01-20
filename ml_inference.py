import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# ML libraries
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from statsmodels.tsa.arima.model import ARIMA

# --- Load your data ---
# File should contain only throughput values, one per line
df = pd.read_csv('dataset.csv', header=None, names=['throughput'])
data = df['throughput'].values

# Split train/test
train_size = int(len(data) * 0.8)
train, test = data[:train_size], data[train_size:]

# --- ARIMA Model ---
start_time = time.time()
arima_model = ARIMA(train, order=(5,1,0))  # You can tune order
arima_model_fit = arima_model.fit()
arima_pred = arima_model_fit.forecast(steps=len(test))
arima_time = time.time() - start_time
arima_mae = mean_absolute_error(test, arima_pred)

print(f"ARIMA inference time: {arima_time:.4f} seconds, MAE: {arima_mae:.4f}")

# --- LSTM Model ---
# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data.reshape(-1, 1))

# Prepare sequences for LSTM
def create_sequences(data, seq_length=5):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 5
X, y = create_sequences(data_scaled, seq_length)
X_train, X_test = X[:train_size-seq_length], X[train_size-seq_length:]
y_train, y_test = y[:train_size-seq_length], y[train_size-seq_length:]

# Build LSTM
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(seq_length,1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Fit LSTM
start_time = time.time()
model.fit(X_train, y_train, epochs=20, batch_size=16, verbose=0)
lstm_time = time.time() - start_time

# Predict and inverse scale
lstm_pred_scaled = model.predict(X_test, verbose=0)
lstm_pred = scaler.inverse_transform(lstm_pred_scaled)
y_test_inv = scaler.inverse_transform(y_test)

lstm_mae = mean_absolute_error(y_test_inv, lstm_pred)
print(f"LSTM inference time: {lstm_time:.4f} seconds, MAE: {lstm_mae:.4f}")

# --- Compare ---
if arima_mae < lstm_mae:
    print("ARIMA is more accurate on this dataset (lower MAE).")
else:
    print("LSTM is more accurate on this dataset (lower MAE).")

# --- Plot results ---
plt.figure(figsize=(12,6))
plt.plot(range(len(test)), test, label='Actual Throughput', color='black')
plt.plot(range(len(test)), arima_pred, label='ARIMA Prediction', color='red')
plt.plot(range(len(y_test_inv)), lstm_pred, label='LSTM Prediction', color='blue')
plt.xlabel('Time Steps')
plt.ylabel('Throughput')
plt.title('Throughput Prediction Comparison')
plt.legend()
plt.show()
