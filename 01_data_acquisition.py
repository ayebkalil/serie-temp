import yfinance as yf
import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

print("--- 1. Fetching historical data (BTC, ETH, BNB) 2019 to October 2026 ---")
tickers = ["BTC-USD", "ETH-USD", "BNB-USD"]
# Start: 2019-01-01, End: 2026-10-03 (Live current date)
raw_data = yf.download(tickers, start="2019-01-01", end="2026-10-04", interval="1d", auto_adjust=False)

df_close = raw_data['Close'].copy()
df_volume = raw_data['Volume'].copy()

df = pd.DataFrame(index=df_close.index)
for t, name in [("BTC-USD", "BTC"), ("ETH-USD", "ETH"), ("BNB-USD", "BNB")]:
    df[f'{name}_Close'] = df_close[t]
    df[f'{name}_Volume'] = df_volume[t]

# Drop any initial rows if an asset started later
df = df.dropna()

print(f"Data shape: {df.shape}")
print(f"Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")

# Compute derived indicators:
for name in ["BTC", "ETH", "BNB"]:
    # 1. Log-Prices
    df[f'{name}_LogPrice'] = np.log(df[f'{name}_Close'])
    # 2. Log-Returns (%): r_t = 100 * (ln(P_t) - ln(P_{t-1}))
    df[f'{name}_Return'] = 100 * (df[f'{name}_LogPrice'] - df[f'{name}_LogPrice'].shift(1))
    # 3. 30-day Realized Volatility (annualized)
    df[f'{name}_Vol30'] = df[f'{name}_Return'].rolling(window=30).std() * np.sqrt(365)
    # 4. 30-day Simple Moving Average (SMA)
    df[f'{name}_SMA30'] = df[f'{name}_Close'].rolling(window=30).mean()

# Drop initial NaNs from differencing/rolling
df_clean = df.dropna().copy()
print(f"Cleaned dataset shape: {df_clean.shape}")

# Strict chronological split: 90% Train / 10% Test
n_total = len(df_clean)
n_train = int(n_total * 0.90)
n_test = n_total - n_train

train_df = df_clean.iloc[:n_train].copy()
test_df = df_clean.iloc[n_train:].copy()

print(f"Train size (90%): {len(train_df)} days ({train_df.index.min().strftime('%Y-%m-%d')} to {train_df.index.max().strftime('%Y-%m-%d')})")
print(f"Test size (10%): {len(test_df)} days ({test_df.index.min().strftime('%Y-%m-%d')} to {test_df.index.max().strftime('%Y-%m-%d')})")

df_clean.to_csv("data/crypto_btc_eth_bnb_full.csv")
train_df.to_csv("data/crypto_btc_eth_bnb_train.csv")
test_df.to_csv("data/crypto_btc_eth_bnb_test.csv")

print("3-Asset Dataset (2019-2026) saved successfully in data/ directory!")