import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from arch import arch_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import os

sns.set_theme(style="whitegrid")

train_df = pd.read_csv("data/crypto_btc_eth_bnb_train.csv", index_col=0, parse_dates=True)
test_df = pd.read_csv("data/crypto_btc_eth_bnb_test.csv", index_col=0, parse_dates=True)
full_df = pd.concat([train_df, test_df])

print("==================================================================")
print("BONUS EXTENSION 1: TRIVARIATE DYNAMIC ROLLING CORRELATIONS (2019-2026)")
print("==================================================================")

full_df['Corr_BTC_ETH'] = full_df['BTC_Return'].rolling(60).corr(full_df['ETH_Return'])
full_df['Corr_BTC_BNB'] = full_df['BTC_Return'].rolling(60).corr(full_df['BNB_Return'])
full_df['Corr_ETH_BNB'] = full_df['ETH_Return'].rolling(60).corr(full_df['BNB_Return'])

fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(full_df.index, full_df['Corr_BTC_ETH'], label='BTC vs ETH (60-day Rolling Corr)', color='#3498db', lw=1.5)
ax.plot(full_df.index, full_df['Corr_BTC_BNB'], label='BTC vs BNB (60-day Rolling Corr)', color='#e67e22', lw=1.2, linestyle='--')
ax.plot(full_df.index, full_df['Corr_ETH_BNB'], label='ETH vs BNB (60-day Rolling Corr)', color='#27ae60', lw=1.2, linestyle=':')

ax.set_title("Figure 7: Trivariate Dynamic Rolling Correlations Between BTC, ETH, and BNB (2019–2026)", fontsize=12, fontweight='bold')
ax.set_ylabel("Pearson Correlation Coefficient")
ax.set_ylim(0.2, 1.0)

ax.annotate('COVID Liquidity Panic\n(All correlations > 0.90)', xy=(pd.to_datetime('2020-03-12'), 0.93),
            xytext=(pd.to_datetime('2019-06-01'), 0.95),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1), fontsize=9, fontweight='bold')

ax.annotate('Ethereum "The Merge" Decoupling\n(Proof of Stake transition)', xy=(pd.to_datetime('2022-09-15'), 0.70),
            xytext=(pd.to_datetime('2022-10-01'), 0.35),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1), fontsize=9, fontweight='bold')

ax.legend(loc='lower left')
plt.tight_layout()
plt.savefig("plots/fig7_dynamic_correlation.png", dpi=150)
plt.close()
print("Figure 7 saved to plots/fig7_dynamic_correlation.png")

print("\n==================================================================")
print("BONUS EXTENSION 2: GJR-GARCH ASYMMETRY (LEVERAGE EFFECT 2019-2026)")
print("==================================================================")

gjr_model = arch_model(train_df['BTC_Return'], mean='AR', lags=1, vol='GARCH', p=1, o=1, q=1, dist='StudentsT')
gjr_res = gjr_model.fit(disp='off')
print(gjr_res.summary())

gamma_coef = gjr_res.params.get('gamma[1]', 0.0)
gamma_pval = gjr_res.pvalues.get('gamma[1]', 1.0)
print(f"\nAsymmetry Parameter gamma: {gamma_coef:.4f} (p-value: {gamma_pval:.4f})")

print("\n==================================================================")
print("MULTI-HORIZON FORECASTING ON 2026 TEST SET (h = 1, 5, 7, 10)")
print("==================================================================")

horizons = [1, 5, 7, 10]
multi_results = []
actual_test = test_df['BTC_Close'].values

for h in horizons:
    naive_preds = test_df['BTC_Close'].shift(h).bfill().values
    sma_preds = test_df['BTC_SMA30'].values
    
    rmse_n = np.sqrt(mean_squared_error(actual_test[h:], naive_preds[h:]))
    mae_n = mean_absolute_error(actual_test[h:], naive_preds[h:])
    mape_n = mean_absolute_percentage_error(actual_test[h:], naive_preds[h:]) * 100
    
    rmse_s = np.sqrt(mean_squared_error(actual_test[h:], sma_preds[h:]))
    mae_s = mean_absolute_error(actual_test[h:], sma_preds[h:])
    mape_s = mean_absolute_percentage_error(actual_test[h:], sma_preds[h:]) * 100
    
    multi_results.append({
        'Horizon (h)': f'h = {h} days',
        'Naive RMSE ($)': rmse_n,
        'Naive MAE ($)': mae_n,
        'Naive MAPE (%)': mape_n,
        'SMA30 RMSE ($)': rmse_s,
        'SMA30 MAE ($)': mae_s,
        'SMA30 MAPE (%)': mape_s
    })

multi_df = pd.DataFrame(multi_results)
print(multi_df.to_string(index=False))
multi_df.to_csv("data/multi_horizon_forecast_results.csv", index=False)

print("\nExtensions completed successfully!")