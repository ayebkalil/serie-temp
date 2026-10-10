import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL
import os

sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

train_df = pd.read_csv("data/crypto_btc_eth_bnb_train.csv", index_col=0, parse_dates=True)
full_df = pd.read_csv("data/crypto_btc_eth_bnb_full.csv", index_col=0, parse_dates=True)

print("==================================================================")
print("SECTION 2: ANALYSE EXPLORATOIRE DES DONNÉES & STATIONNARITÉ (2019-2026)")
print("==================================================================")

# 1. Summary Statistics for 3 Assets (Training Sample 2019-2025)
stats_dict = {}
for coin in ["BTC", "ETH", "BNB"]:
    ret = train_df[f'{coin}_Return']
    stats_dict[f'{coin}_Return'] = [
        ret.mean(),
        ret.std(),
        ret.median(),
        ret.min(),
        ret.max(),
        ret.skew(),
        ret.kurtosis()
    ]

stats_df = pd.DataFrame(stats_dict, index=['Moyenne (%)', 'Écart-type (%)', 'Médiane (%)', 'Minimum (%)', 'Maximum (%)', 'Skewness (Asymétrie)', 'Kurtosis (Excès)'])
print("\n--- Statistiques Descriptives : Log-Rendements (%) ---")
print(stats_df.round(4))
stats_df.to_csv("data/descriptive_statistics.csv")

# 2. Time Series Plot: 3 Assets (Prices & Returns)
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Subplot 1: Normalized Prices (Base 100)
btc_norm = 100 * full_df['BTC_Close'] / full_df['BTC_Close'].iloc[0]
eth_norm = 100 * full_df['ETH_Close'] / full_df['ETH_Close'].iloc[0]
bnb_norm = 100 * full_df['BNB_Close'] / full_df['BNB_Close'].iloc[0]

axes[0, 0].plot(full_df.index, btc_norm, label="Bitcoin (BTC-USD)", color="#f39c12", lw=1.5)
axes[0, 0].plot(full_df.index, eth_norm, label="Ethereum (ETH-USD)", color="#3498db", lw=1.5)
axes[0, 0].plot(full_df.index, bnb_norm, label="Binance Coin (BNB-USD)", color="#e67e22", lw=1.5)
axes[0, 0].set_title("Figure 1A : Évolution des Prix Normalisés (Base 100 = 31 Janvier 2019)", fontsize=11, fontweight='bold')
axes[0, 0].set_ylabel("Indice de Prix (Échelle Log)")
axes[0, 0].set_yscale('log')
axes[0, 0].legend(frameon=True)

# Subplot 2: Log-Prices Co-movement
axes[0, 1].plot(full_df.index, full_df['BTC_LogPrice'], label="ln(BTC)", color="#f39c12", lw=1.2)
axes[0, 1].plot(full_df.index, full_df['ETH_LogPrice'], label="ln(ETH)", color="#3498db", lw=1.2)
axes[0, 1].plot(full_df.index, full_df['BNB_LogPrice'], label="ln(BNB)", color="#e67e22", lw=1.2)
axes[0, 1].set_title("Figure 1B : Trajectoires des Log-Prix [ln(P_t)] (2019–2026)", fontsize=11, fontweight='bold')
axes[0, 1].set_ylabel("Log-Prix")
axes[0, 1].legend(frameon=True)

# Subplot 3: BTC Returns
axes[1, 0].plot(full_df.index, full_df['BTC_Return'], label="Rendement BTC (%)", color="#f39c12", alpha=0.7, lw=0.7)
axes[1, 0].axhline(0, color='black', linestyle='--', lw=0.8)
axes[1, 0].set_title("Figure 1C : Log-Rendements Quotidiens du Bitcoin (%) [Regroupement de Volatilité]", fontsize=11, fontweight='bold')
axes[1, 0].set_ylabel("Rendement (%)")
axes[1, 0].legend(frameon=True)

# Subplot 4: ETH & BNB Returns Overlay
axes[1, 1].plot(full_df.index, full_df['ETH_Return'], label="Rendement ETH (%)", color="#3498db", alpha=0.6, lw=0.7)
axes[1, 1].plot(full_df.index, full_df['BNB_Return'], label="Rendement BNB (%)", color="#e67e22", alpha=0.6, lw=0.7)
axes[1, 1].axhline(0, color='black', linestyle='--', lw=0.8)
axes[1, 1].set_title("Figure 1D : Log-Rendements Quotidiens d'Ethereum et BNB (%)", fontsize=11, fontweight='bold')
axes[1, 1].set_ylabel("Rendement (%)")
axes[1, 1].legend(frameon=True)

plt.tight_layout()
plt.savefig("plots/fig1_prices_and_returns.png", dpi=300)
plt.close()
print("Figure 1 enregistrée dans plots/fig1_prices_and_returns.png (300 DPI).")

# 3. ACF and PACF Plots (Training Sample 2019-2025)
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
plot_acf(train_df['BTC_LogPrice'], lags=30, ax=axes[0, 0], title="Figure 2A : ACF du Log-Prix BTC (Décroissance Lente I(1))")
plot_pacf(train_df['BTC_LogPrice'], lags=30, ax=axes[0, 1], title="Figure 2B : PACF du Log-Prix BTC (Pic Unitaire au Retard 1)")
plot_acf(train_df['BTC_Return'], lags=30, ax=axes[1, 0], title="Figure 2C : ACF des Log-Rendements BTC (Coupure Rapide I(0))")
plot_pacf(train_df['BTC_Return'], lags=30, ax=axes[1, 1], title="Figure 2D : PACF des Log-Rendements BTC")
plt.tight_layout()
plt.savefig("plots/fig2_acf_pacf.png", dpi=300)
plt.close()
print("Figure 2 enregistrée dans plots/fig2_acf_pacf.png (300 DPI).")

# 4. STL Decomposition (BTC - Training Sample 2019-2025, period=7)
stl_btc = STL(train_df['BTC_LogPrice'], period=7, robust=True).fit()
fig = stl_btc.plot()
fig.set_size_inches(12, 8)
fig.suptitle("Figure 3 : Décomposition STL du Log-Prix du Bitcoin (Périodicité Hebdomadaire s=7, 2019–2025)", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig("plots/fig3_stl_decomposition.png", dpi=300)
plt.close()
print("Figure 3 enregistrée dans plots/fig3_stl_decomposition.png (300 DPI).")

# 5. Dual Unit Root Tests (ADF vs KPSS) on All 3 Coins
def run_tests(series, name):
    adf_res = adfuller(series.dropna(), autolag='AIC')
    kpss_res = kpss(series.dropna(), regression='c', nlags='auto')
    return {
        'Série': name,
        'Stat ADF': round(adf_res[0], 4),
        'p-valeur ADF': round(adf_res[1], 4),
        'Verdict ADF': 'Stationnaire' if adf_res[1] < 0.05 else 'Non-Stationnaire (Racine Unitaire)',
        'Stat KPSS': round(kpss_res[0], 4),
        'p-valeur KPSS': round(kpss_res[1], 4),
        'Verdict KPSS': 'Stationnaire' if kpss_res[1] > 0.05 else 'Non-Stationnaire (Rejet H0)',
        'Conclusion Conjointe': 'I(0) Stationnaire' if (adf_res[1] < 0.05 and kpss_res[1] > 0.05) else ('I(1) Racine Unitaire' if (adf_res[1] > 0.05 and kpss_res[1] < 0.05) else 'Inconcluant')
    }

results = []
for coin in ["BTC", "ETH", "BNB"]:
    results.append(run_tests(train_df[f'{coin}_LogPrice'], f"{coin} Log-Prix (Niveau)"))
    results.append(run_tests(train_df[f'{coin}_Return'], f"{coin} Log-Rendement (Différence)"))

test_table = pd.DataFrame(results)
print("\n--- Double Validation Formelle de la Stationnarité (ADF vs KPSS) ---")
print(test_table.to_string(index=False))
test_table.to_csv("data/stationarity_tests_results.csv", index=False)

print("\nScript 02 exécuté avec succès !")