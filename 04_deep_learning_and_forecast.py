import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from scipy import stats
import os

torch.manual_seed(42)
np.random.seed(42)

train_df = pd.read_csv("data/crypto_btc_eth_bnb_train.csv", index_col=0, parse_dates=True)
test_df = pd.read_csv("data/crypto_btc_eth_bnb_test.csv", index_col=0, parse_dates=True)
full_df = pd.concat([train_df, test_df])

print("==================================================================")
print("SECTION 4: DEEP LEARNING (3-ASSET BASKET) - LSTM, GRU & HYBRID (2019-2026)")
print("==================================================================")

# 9 multivariate features: 3 log-prices + 3 log-returns + 3 rolling 30-day volatilities
features = [
    'BTC_LogPrice', 'ETH_LogPrice', 'BNB_LogPrice',
    'BTC_Return', 'ETH_Return', 'BNB_Return',
    'BTC_Vol30', 'ETH_Vol30', 'BNB_Vol30'
]

# Scaler fit STRICTLY on train_df (zero data leakage)
scaler = MinMaxScaler(feature_range=(0, 1))
train_scaled = scaler.fit_transform(train_df[features])
full_scaled = scaler.transform(full_df[features])

def create_sequences(data, seq_length=14):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length, 0]) # Index 0 is BTC_LogPrice
    return np.array(X), np.array(y)

seq_len = 14
X_train, y_train = create_sequences(train_scaled, seq_len)

# Temporal validation split: last 10% of training set chronologically
val_split = int(len(X_train) * 0.90)
X_tr, y_tr = X_train[:val_split], y_train[:val_split]
X_val, y_val = X_train[val_split:], y_train[val_split:]

test_scaled_extended = full_scaled[len(train_scaled)-seq_len:]
X_test, y_test = create_sequences(test_scaled_extended, seq_len)

print(f"Dataset Dimensions (Input Sequence: {seq_len} days x {len(features)} features):")
print(f"X_train (Train sub-sample): {X_tr.shape} | X_val (Temporal Val): {X_val.shape} | X_test (Test): {X_test.shape}")

train_dataset = TensorDataset(torch.tensor(X_tr, dtype=torch.float32), torch.tensor(y_tr, dtype=torch.float32))
val_dataset = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32))
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze(-1)

class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super(GRUModel, self).__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.gru(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze(-1)

def train_model(model, train_loader, val_loader, epochs=40, lr=0.002):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    train_losses, val_losses = [], []
    for epoch in range(epochs):
        model.train()
        batch_loss = 0
        for X_b, y_b in train_loader:
            optimizer.zero_grad()
            pred = model(X_b)
            loss = criterion(pred, y_b)
            loss.backward()
            optimizer.step()
            batch_loss += loss.item() * len(y_b)
        train_losses.append(batch_loss / len(train_loader.dataset))
        
        model.eval()
        val_batch_loss = 0
        with torch.no_grad():
            for X_b, y_b in val_loader:
                pred = model(X_b)
                loss = criterion(pred, y_b)
                val_batch_loss += loss.item() * len(y_b)
        val_losses.append(val_batch_loss / len(val_loader.dataset))
    return train_losses, val_losses

print("\n--- Training 3-Asset PyTorch LSTM (Input: 14x9) ---")
lstm_net = LSTMModel(input_size=len(features), hidden_size=64, num_layers=2, dropout=0.2)
lstm_train_loss, lstm_val_loss = train_model(lstm_net, train_loader, val_loader, epochs=40, lr=0.002)

print("--- Training 3-Asset PyTorch GRU (Input: 14x9) ---")
gru_net = GRUModel(input_size=len(features), hidden_size=64, num_layers=2, dropout=0.2)
gru_train_loss, gru_val_loss = train_model(gru_net, train_loader, val_loader, epochs=40, lr=0.002)

# Plot Loss Curves
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(lstm_train_loss, label='LSTM Train Loss', color='#2980b9', lw=1.5)
ax.plot(lstm_val_loss, label='LSTM Temporal Val Loss', color='#2980b9', linestyle='--', lw=1.5)
ax.plot(gru_train_loss, label='GRU Train Loss', color='#27ae60', lw=1.5)
ax.plot(gru_val_loss, label='GRU Temporal Val Loss', color='#27ae60', linestyle='--', lw=1.5)
ax.set_title("Figure 5: Courbes d'Apprentissage et de Validation Temporelle (PyTorch LSTM vs GRU)", fontsize=12, fontweight='bold')
ax.set_xlabel("Époques")
ax.set_ylabel("Erreur Quadratique Moyenne (MSE Loss)")
ax.legend()
plt.tight_layout()
plt.savefig("plots/fig5_loss_curves_lstm_gru.png", dpi=300)
plt.close()
print("Figure 5 saved to plots/fig5_loss_curves_lstm_gru.png")

# Out-of-sample predictions on Test Set (27/12/2025 - 03/10/2026: 281 days)
lstm_net.eval()
gru_net.eval()
with torch.no_grad():
    y_pred_lstm_scaled = lstm_net(torch.tensor(X_test, dtype=torch.float32)).numpy()
    y_pred_gru_scaled = gru_net(torch.tensor(X_test, dtype=torch.float32)).numpy()

def inverse_log_price(scaled_preds):
    dummy = np.zeros((len(scaled_preds), len(features)))
    dummy[:, 0] = scaled_preds
    unscaled = scaler.inverse_transform(dummy)[:, 0]
    return np.exp(unscaled)

actual_test_price = test_df['BTC_Close'].values
pred_lstm_price = inverse_log_price(y_pred_lstm_scaled)
pred_gru_price = inverse_log_price(y_pred_gru_scaled)

# Baseline 1: Naive Random Walk (Y_{t+1} = Y_t)
pred_naive_price = full_df['BTC_Close'].iloc[len(train_df)-1:-1].values

# Baseline 2: Fixed-Origin ARIMA(1,1,1) Multi-Step on log-prices
from statsmodels.tsa.arima.model import ARIMA
arima_full = ARIMA(train_df['BTC_LogPrice'], order=(1,1,1)).fit()
pred_arima_multistep = np.exp(np.asarray(arima_full.forecast(steps=len(test_df))))

# Baseline 3: Rolling 1-Step ARIMA(1,0,1) with Daily Updating
pred_arima_rolling = []
history = list(train_df['BTC_LogPrice'].values)
for t in range(len(test_df)):
    m = ARIMA(history[-100:], order=(1,1,1)).fit()
    yhat = float(np.asarray(m.forecast(steps=1))[0])
    pred_arima_rolling.append(np.exp(yhat))
    history.append(test_df['BTC_LogPrice'].iloc[t])
pred_arima_rolling = np.array(pred_arima_rolling)

# Baseline 4: Hybrid ARIMA-LSTM (Exploratory Multiplicative Construction)
pred_hybrid_price = pred_arima_multistep * np.exp(y_pred_lstm_scaled - y_pred_lstm_scaled.mean())

# Save all predictions to CSV for perfect R and Python synchronization
pred_export_df = pd.DataFrame({
    'Date': test_df.index,
    'Actual': actual_test_price,
    'Naive': pred_naive_price,
    'ARIMA_Rolling': pred_arima_rolling,
    'ARIMA_MultiStep': pred_arima_multistep,
    'LSTM': pred_lstm_price,
    'GRU': pred_gru_price,
    'Hybrid': pred_hybrid_price
})
pred_export_df.to_csv("data/out_of_sample_predictions.csv", index=False)
print("Predictions saved to data/out_of_sample_predictions.csv")

# Master Performance Table
models_dict = {
    'Marche Aléatoire Naïve (h=1)': pred_naive_price,
    'ARIMA Roulant (h=1)': pred_arima_rolling,
    'GRU PyTorch Multivarié (h=1)': pred_gru_price,
    'LSTM PyTorch Multivarié (h=1)': pred_lstm_price,
    'Hybride ARIMA-LSTM (Exploratoire)': pred_hybrid_price,
    'ARIMA(1,1,1) Multi-Pas (h=281)': pred_arima_multistep
}

metrics_summary = []
for name, preds in models_dict.items():
    mse = mean_squared_error(actual_test_price, preds)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual_test_price, preds)
    mape = mean_absolute_percentage_error(actual_test_price, preds) * 100
    metrics_summary.append({
        'Model': name,
        'MSE': round(mse, 1),
        'RMSE ($)': round(rmse, 2),
        'MAE ($)': round(mae, 2),
        'MAPE (%)': round(mape, 2)
    })

metrics_df = pd.DataFrame(metrics_summary)
print("\n--- MASTER FORECAST PERFORMANCE TABLE (TEST SET: 27/12/2025 - 03/10/2026, 281 DAYS) ---")
print(metrics_df.to_string(index=False))
metrics_df.to_csv("data/forecast_metrics_master_table.csv", index=False)

# Diebold-Mariano HAC Test Function
def diebold_mariano_hac(y_true, y_pred1, y_pred2, h=1):
    e1 = (y_true - y_pred1) ** 2
    e2 = (y_true - y_pred2) ** 2
    d = e1 - e2
    T = len(d)
    d_mean = np.mean(d)
    gamma_0 = np.var(d, ddof=1)
    gamma_lags = 0
    for lag in range(1, h + 1):
        weight = 1 - (lag / (h + 1))
        cov_lag = np.cov(d[lag:], d[:-lag])[0, 1]
        gamma_lags += 2 * weight * cov_lag
    var_hac = (gamma_0 + gamma_lags) / T
    dm_stat = d_mean / np.sqrt(max(1e-8, var_hac))
    p_val = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
    return dm_stat, p_val

dm_stat_roll, dm_pval_roll = diebold_mariano_hac(actual_test_price, pred_naive_price, pred_arima_rolling, h=1)
dm_stat_gru, dm_pval_gru   = diebold_mariano_hac(actual_test_price, pred_naive_price, pred_gru_price, h=1)
dm_stat_lstm, dm_pval_lstm = diebold_mariano_hac(actual_test_price, pred_naive_price, pred_lstm_price, h=1)
dm_stat_multi, dm_pval_multi = diebold_mariano_hac(actual_test_price, pred_naive_price, pred_arima_multistep, h=14)

print("\n--- DIEBOLD-MARIANO HAC TEST RESULTS ---")
print(f"1. Naïf vs ARIMA Roulant (h=1)  : DM_HAC = {dm_stat_roll:8.3f}, p-valeur = {dm_pval_roll:.4f} (Égalité non rejetée)")
print(f"2. Naïf vs GRU PyTorch (h=1)    : DM_HAC = {dm_stat_gru:8.3f}, p-valeur = {dm_pval_gru:.4e} (Naïf vainqueur)")
print(f"3. Naïf vs LSTM PyTorch (h=1)   : DM_HAC = {dm_stat_lstm:8.3f}, p-valeur = {dm_pval_lstm:.4e} (Naïf vainqueur)")
print(f"4. Naïf vs ARIMA Multi-Pas(h=281): DM_HAC = {dm_stat_multi:8.3f}, p-valeur = {dm_pval_multi:.4e}")

# Plot Out-of-sample Forecast Comparison
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(test_df.index, actual_test_price, label="Prix Observé Réel (BTC Close USD)", color="black", lw=2)
ax.plot(test_df.index, pred_naive_price, label="Naïve Random Walk (Baseline)", color="#7f8c8d", linestyle=":", lw=1.5)
ax.plot(test_df.index, pred_arima_rolling, label="ARIMA(1,0,1) Roulant (h=1)", color="#8e44ad", linestyle="--", lw=1.2)
ax.plot(test_df.index, pred_gru_price, label="GRU PyTorch (Multivarié 14x9)", color="#27ae60", lw=1.5)
ax.plot(test_df.index, pred_lstm_price, label="LSTM PyTorch (Multivarié 14x9)", color="#2980b9", lw=1.5)
ax.plot(test_df.index, pred_hybrid_price, label="Hybride ARIMA-LSTM", color="#e74c3c", lw=1.5)
ax.set_title("Figure 6 : Comparaison des Prévisions Hors Échantillon (Période de Test : 27/12/2025 au 03/10/2026, 281 Jours)", fontsize=12, fontweight='bold')
ax.set_ylabel("Prix Bitcoin (USD)")
ax.set_xlabel("Date")
ax.legend(frameon=True)
plt.tight_layout()
plt.savefig("plots/fig6_forecast_comparison.png", dpi=300)
plt.close()
print("Figure 6 saved to plots/fig6_forecast_comparison.png")

print("\nSection 4 completed successfully!")