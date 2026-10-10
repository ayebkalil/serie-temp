# Mini-Projet : Séries Temporelles pour Data Science & IA (TEK-UP 2026)

**Enseignant :** M. Ahmed Dhouibi  
**Date limite de rendu :** 12 Octobre 2026 à 23h55  
**Auteurs (Équipe de 4 membres) :** Rawen Bejie, Khawla Hawari, Amine Benfadhel, Khalil Ayeb  
**Sujet :** *Joint Dynamics, Cointegration, and Volatility Modeling of a 3-Crypto Basket: Bitcoin (BTC-USD), Ethereum (ETH-USD), and Binance Coin (BNB-USD) [2019–2026]*

---

## 1. Vue d'Ensemble du Projet

Ce projet implémente un pipeline complet de modélisation économétrique et d'apprentissage profond sur les trois principales cryptomonnaies mondiales (BTC, ETH, BNB) cotées en continu 24/7 sur **2 803 jours** (du 31 janvier 2019 au 3 octobre 2026).

### Source et Partition Chronologique Stricte (Zero Data Leakage) :
- **Source :** Yahoo Finance via Python `yfinance` et R `quantmod`. Tickers : `BTC-USD`, `ETH-USD`, `BNB-USD` (clôture Close à 00:00 UTC).
- **Date d'origine :** 31 janvier 2019 (première date d'historique continu commun sur Yahoo Finance après fenêtre glissante 30j).
- **Ensemble d'entraînement (90%) :** 2 522 jours (31 janvier 2019 au 26 décembre 2025).
- **Ensemble de test hors échantillon (10%) :** 281 jours (27 décembre 2025 au 3 octobre 2026).

---

## 2. Structure des Fichiers

```
serie temp/
│
├── Rapport_MiniProjet_Series_Temporelles_BTC_ETH_BNB.pdf   # Rapport scientifique master (PDF 17 pages)
├── Rapport_MiniProjet_Series_Temporelles_BTC_ETH_BNB.docx  # Rapport scientifique éditable (Word)
├── Time_Series_MiniProject_BTC_ETH_BNB.ipynb              # Notebook Jupyter interactif 100% exécuté en direct
├── Time_Series_MiniProject_BTC_ETH_BNB.Rmd                # Notebook RMarkdown économétrique (R)
├── Plan_Detaille_Par_Role_Equipe_TEKUP.pdf               # Plan de projet par rôle pour 4 membres (PDF)
├── Plan_Detaille_Par_Role_Equipe_TEKUP.docx              # Plan de projet par rôle pour 4 membres (Word)
├── README.md                                              # Synthèse du projet et guide d'exécution
│
├── data/                                                  # Données CSV et tables de résultats
│   ├── crypto_btc_eth_bnb_full.csv                        # Base historique 2019–2026 (2 803 observations)
│   ├── crypto_btc_eth_bnb_train.csv                       # Échantillon d'apprentissage (2 522 obs)
│   ├── crypto_btc_eth_bnb_test.csv                        # Échantillon de test (281 obs)
│   ├── out_of_sample_predictions.csv                      # Prévisions synchronisées de tous les modèles
│   ├── descriptive_statistics.csv                         # Moments d'ordre 1 à 4 & Jarque-Bera
│   ├── stationarity_tests_results.csv                     # Double test conjoint ADF vs KPSS
│   ├── granger_causality_matrix_3assets.csv               # Matrice de causalité croisée 3x3
│   ├── forecast_metrics_master_table.csv                  # Tableau comparatif des prévisions (Test 281j)
│   └── llm_audit_section5.json                            # Audit critique des hallucinations LLM
│
├── plots/                                                 # Figures scientifiques haute résolution (300 DPI)
│   ├── fig1_prices_and_returns.png                        # Prix normalisés, log-prix et rendements (2019-2026)
│   ├── fig2_acf_pacf.png                                  # Fonctions ACF/PACF (Train 2019-2025)
│   ├── fig3_stl_decomposition.png                         # Décomposition STL hebdomadaire s=7 (2019-2025)
│   ├── fig4_garch_volatility_events.png                   # Volatilité conditionnelle vs événements (2019-2025)
│   ├── fig5_loss_curves_lstm_gru.png                      # Courbes de perte d'entraînement & validation temporelle
│   ├── fig6_forecast_comparison.png                       # Trajectoires prédictives hors échantillon (Test 281j)
│   └── fig7_dynamic_correlation.png                       # Corrélations dynamiques glissantes 60 jours
│
├── Scripts Python :
│   ├── 01_data_acquisition.py                            # Téléchargement et ingénierie des features
│   ├── 02_eda_stationarity.py                             # Statistiques descriptives, STL et tests ADF/KPSS
│   ├── 03_classical_econometrics.py                       # ARMA/ARIMA, VAR(5), Johansen, GARCH et GJR-GARCH
│   ├── 04_deep_learning_and_forecast.py                  # PyTorch LSTM, GRU, Hybride & Diebold-Mariano
│   ├── 05_llm_experiments.py                             # Protocole de test et audit des LLMs (Section 5)
│   └── 06_advanced_extensions.py                         # Multi-horizons et corrélations dynamiques
│
└── Scripts R :
    ├── 01_data_acquisition.R                             # Ingestion des données en R
    ├── 02_eda_stationarity.R                              # Décomposition STL et double test en R
    ├── 03_classical_econometrics.R                        # auto.arima, vars, ca.jo, fGarch en R
    ├── 04_advanced_models_forecast.R                     # Évaluation prédictive et Diebold-Mariano synchronisés
    └── 05_extensions_dcc_multihorizon.R                  # Extensions économétriques multivariées en R
```

---

## 3. Résultats Clés et Conclusions Économétriques

| Dimension Analysée | Méthode & Test | Résultat Obtenu | Interprétation Économique / Statistique |
| :--- | :--- | :--- | :--- |
| **Ordre d'intégration** | Double test conjoint ADF & KPSS | Log-Prix: $I(1)$ ($p_{\text{ADF}} > 0.26, p_{\text{KPSS}} = 0.01$)<br>Rendements: $I(0)$ ($p_{\text{ADF}} < 0.0001, p_{\text{KPSS}} > 0.10$) | Tous les actifs possèdent une racine unitaire stochastique en niveau ; les log-rendements sont stationnaires. |
| **Spécification Univariée** | ARMA(1,1) / ARIMA(1,0,1) | $\phi_1 = -0.050, \mu = 0.0892\%$ ($p=0.0304$)<br>Ljung-Box $p = 0.198$, ARCH-LM $p < 10^{-16}$ | Modèle estimé sur log-rendements (équivalent à ARIMA(1,1,1) avec dérive sur log-prix). Hétéroscédasticité massive justifiant le GARCH. |
| **Cointégration Trivariée** | Test de la Trace de Johansen ($k\_ar\_diff=4$) | Python : $25.53 < 29.80$<br>R `urca` : $30.27 < 34.91$ $\implies r = 0$ | **$r = 0$ : Absence de cointégration.** Une corrélation élevée n'implique pas de cointégration. Justification théorique du modèle VAR sur rendements plutôt qu'un VECM. |
| **Transmission d'Information** | VAR(5) sur Log-Rendements & Granger | BTC $\leftrightarrow$ ETH ($p < 0.05$) ; ETH $\rightarrow$ BNB ($p=0.0090$) ; BNB $\nrightarrow$ BTC/ETH | Précédence temporelle d'information (et non causalité physique). BNB n'apporte pas d'information prédictive marginale. |
| **Dynamique de Volatilité** | GARCH(1,1) avec loi de Student | $\alpha_1=0.0697, \beta_1=0.9303 \implies \alpha_1+\beta_1=1.0000$, $\nu=2.98$ | Frontière du cas IGARCH(1,1) (persistance extrême des chocs) et queues lourdes. Test ARCH-LM post-GARCH $p = 0.8889$ (effets résiduels éliminés). |
| **Effet de Levier** | Modèle GJR-GARCH Asymétrique | $\gamma = -0.0029$ ($p = 0.895$, non significatif) | Absence d'effet de levier : la volatilité des cryptomonnaies réagit de manière symétrique aux chocs haussiers et baissiers. |
| **Compétition Prédictive** | Test (281 jours, 27/12/2025 au 03/10/2026) | Naïf ($1\,725\$$) $\approx$ ARIMA Roulant ($1\,769\$$) < GRU ($2\,468\$$) < LSTM ($3\,776\$$) | **Puzzle de Meese-Rogoff (1983) :** La marche aléatoire naïve domine tous les modèles neuronaux et égale l'ARIMA roulant 1-pas. |
| **Test de Diebold-Mariano (HAC)** | Tests Like-for-Like ($h=1$) | Naïf vs ARIMA Roulant : $DM = -1.243$ ($p = 0.214$)<br>Naïf vs GRU : $DM = -5.001$ ($p < 10^{-6}$)<br>Naïf vs LSTM : $DM = -13.149$ ($p < 10^{-16}$) | Supériorité statistique confirmée du benchmark naïf face aux modèles complexes, égalité statistique face à l'ARIMA roulant. |
| **Audit IA Générative (Sec. 5)** | Grille d'évaluation LLM | 3 failles réfutées avec prompts verbatim | Réfutation de l'arbitrage sans risque (Johansen $r=0$), de la confusion Granger/causalité physique, et du mirage de prédictibilité sans fuite de données. |

---

## 4. Instructions d'Exécution

### Option A : Pipeline Python Complet
```bash
# 1. Installer les dépendances
pip install yfinance pandas numpy matplotlib seaborn statsmodels arch torch scikit-learn scipy python-docx

# 2. Exécuter les scripts
python 01_data_acquisition.py
python 02_eda_stationarity.py
python 03_classical_econometrics.py
python 04_deep_learning_and_forecast.py
python 05_llm_experiments.py
python 06_advanced_extensions.py

# 3. Lancer le notebook Jupyter
jupyter notebook Time_Series_MiniProject_BTC_ETH_BNB.ipynb
```

### Option B : Pipeline R
```r
# 1. Packages requis
install.packages(c("tseries", "forecast", "vars", "urca", "fGarch", "zoo", "Metrics", "rmarkdown"))

# 2. Exécuter
source("01_data_acquisition.R")
source("02_eda_stationarity.R")
source("03_classical_econometrics.R")
source("04_advanced_models_forecast.R")
```
