import ta.momentum
import ta.others
import ta.trend
import ta.utils
import ta.volume
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import ta
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sklearn.metrics import mean_squared_error
import torch.optim as optim
import matplotlib.pyplot as plt


# Load data using Alpaca or any CSV file
training_data = pd.read_csv('training_data.csv')

#generate features
training_data['SMA_20'] = ta.trend.sma_indicator(training_data['close'],window=20)
training_data['EMA_20'] = ta.trend.ema_indicator(training_data['close'],window=20)
training_data['RSI'] = ta.momentum.rsi(training_data['close'],window=20)
training_data['MACD'] = ta.trend.macd(training_data['close'])
training_data['MACD_Signal'] = ta.trend.macd_signal(training_data['close'])
bollinger = ta.volatility.BollingerBands(training_data['close'], window=20)
training_data['BB_Upper'] = bollinger.bollinger_hband()
training_data['BB_Lower'] = bollinger.bollinger_lband()
training_data['BB_Width'] = training_data['BB_Upper'] - training_data['BB_Lower']
training_data['Volume_Change'] = training_data['volume'].pct_change()
training_data['Volume_MA_10'] = training_data['volume'].rolling(window=10).mean()
training_data['day_of_week'] = pd.DatetimeIndex(training_data['timestamp']).day
training_data['month'] = pd.DatetimeIndex(training_data['timestamp']).month
for lag in range(1, 4):
    training_data[f'Close_Lag_{lag}'] = training_data['close'].shift(lag)
training_data['Return'] = training_data['close'].pct_change()
training_data = training_data.dropna()
training_data.to_csv('processed_training_data.csv')

# Scale the data
training_features = training_data[['close', 'SMA_20', 'EMA_20', 'RSI', 'MACD', 'MACD_Signal',
                 'BB_Upper', 'BB_Lower', 'BB_Width', 'volume', 'Volume_Change',
                 'Volume_MA_10', 'day_of_week', 'month', 
                 'Close_Lag_1', 'Close_Lag_2', 'Close_Lag_3', 'Return']]
scaler = MinMaxScaler()
scaled_training_features = scaler.fit_transform(training_features)

# Create a DataFrame from scaled data to keep things organized
scaled_training_data = pd.DataFrame(scaled_training_features, index=training_data.index, columns=training_features.columns)

# Create sliding window dataset
def create_dataset(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data.iloc[i:i + seq_length].values)
        y.append(data.iloc[i + seq_length]['close'])  
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

# Create dataset
seq_length = 20
X, y = create_dataset(scaled_training_data, seq_length)

class StockLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(StockLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, 
                            batch_first=True, dropout=0.2)
        self.fc1 = nn.Linear(hidden_size, 64)   # Fully connected layer
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)             # Output layer
        
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.relu(self.fc1(out[:, -1, :]))  # Take last time step output
        out = self.relu(self.fc2(out))
        out = self.fc3(out)
        return out

# Model parameters
input_size = X.shape[2]  # Number of features
hidden_size = 128         # More neurons = better capacity to learn patterns
num_layers = 2            # Stack multiple LSTM layers

model = StockLSTM(input_size, hidden_size, num_layers)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 50
early_stop_patience = 5
best_loss = float('inf')
patience_counter = 0

for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, y.unsqueeze(1))
    
    loss.backward()
    optimizer.step()
    
    # Early stopping
    if loss.item() < best_loss:
        best_loss = loss.item()
        patience_counter = 0
    else:
        patience_counter += 1
    
    if patience_counter >= early_stop_patience:
        print(f"Stopping early at epoch {epoch}")
        break
    
    if (epoch + 1) % 5 == 0:
        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

model.eval()
predictions = model(X).detach().numpy()

# Inverse scale the predictions
predictions = scaler.inverse_transform(
    np.concatenate((np.zeros((predictions.shape[0], input_size - 1)), predictions), axis=1)
)[:, -1]

actual = scaler.inverse_transform(
    np.concatenate((np.zeros((y.shape[0], input_size - 1)), y.numpy().reshape(-1, 1)), axis=1)
)[:, -1]

pred_dates = training_data['timestamp'].iloc[seq_length:].values

# Plot
# plt.figure(figsize=(12, 6))
# plt.plot(pred_dates, actual, label="Actual", color="blue")
# plt.plot(pred_dates, predictions, label="Predicted", color="orange", linestyle="--")
# plt.xticks(pred_dates[::50], rotation=45)
# plt.legend()
# plt.show()


# Load Test Data
test_data = pd.read_csv('test_data.csv')
test_data['SMA_20'] = ta.trend.sma_indicator(test_data['close'],window=20)
test_data['EMA_20'] = ta.trend.ema_indicator(test_data['close'],window=20)
test_data['RSI'] = ta.momentum.rsi(test_data['close'],window=20)
test_data['MACD'] = ta.trend.macd(test_data['close'])
test_data['MACD_Signal'] = ta.trend.macd_signal(test_data['close'])
bollinger = ta.volatility.BollingerBands(test_data['close'], window=20)
test_data['BB_Upper'] = bollinger.bollinger_hband()
test_data['BB_Lower'] = bollinger.bollinger_lband()
test_data['BB_Width'] = test_data['BB_Upper'] - test_data['BB_Lower']
test_data['Volume_Change'] = test_data['volume'].pct_change()
test_data['Volume_MA_10'] = test_data['volume'].rolling(window=10).mean()
test_data['day_of_week'] = pd.DatetimeIndex(test_data['timestamp']).day
test_data['month'] = pd.DatetimeIndex(test_data['timestamp']).month
for lag in range(1, 4):
    test_data[f'Close_Lag_{lag}'] = test_data['close'].shift(lag)
test_data['Return'] = test_data['close'].pct_change()
test_data = test_data.dropna()
test_data.to_csv('processed_test_data.csv')

# Scale the data
test_features = test_data[['close', 'SMA_20', 'EMA_20', 'RSI', 'MACD', 'MACD_Signal',
                 'BB_Upper', 'BB_Lower', 'BB_Width', 'volume', 'Volume_Change',
                 'Volume_MA_10', 'day_of_week', 'month', 
                 'Close_Lag_1', 'Close_Lag_2', 'Close_Lag_3', 'Return']]
scaler = MinMaxScaler()
scaled_test_features = scaler.fit_transform(test_features)

# Create a DataFrame from scaled data to keep things organized
scaled_test_data = pd.DataFrame(scaled_test_features, index=test_data.index, columns=test_features.columns)
x_test, y_test = create_dataset(scaled_test_data,seq_length=seq_length)
test_predictions = model(x_test).detach().numpy()

test_input_size = x_test.shape[2]

# test_predictions = scaler.inverse_transform(
#     np.concatenate((np.zeros((test_predictions.shape[0], test_input_size - 1)), test_predictions), axis=1)
# )[:, -1]

# test_actual = scaler.inverse_transform(
#     np.concatenate((np.zeros((y_test.shape[0], test_input_size - 1)), y_test.numpy().reshape(-1, 1)), axis=1)
# )[:, -1]

test_predictions = scaler.inverse_transform(test_predictions)
test_actual = scaler.inverse_transform(y_test.detach().numpy().reshape(-1, 1))

pred_test_dates = test_data['timestamp'].iloc[seq_length:].values

plt.figure(figsize=(12, 6))
plt.plot(pred_test_dates,test_actual, label='Actual', color='blue')
plt.plot(pred_test_dates,test_predictions, label='Predicted', linestyle='--', color='orange')
plt.xticks(pred_test_dates[::50], rotation=45)
plt.legend()
plt.show()
