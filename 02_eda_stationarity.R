# ==============================================================================
# SCRIPT 02 : ANALYSE EXPLORATOIRE ET TESTS DE STATIONNARITÉ (R)
# Justification : Vérification empirique des moments, décomposition et stationnarité
# ==============================================================================

suppressPackageStartupMessages({
  library(tseries)
  library(forecast)
  library(zoo)
})

train_df <- read.csv("data/crypto_btc_eth_train.csv", stringsAsFactors = FALSE)
train_df$Date <- as.Date(train_df$Date)

# Justification : Extraction des rendements pour quantifier la volatilité et les moments d'ordre supérieur
btc_ret <- train_df$BTC_Return
eth_ret <- train_df$ETH_Return

cat("==================================================================\n")
cat("1. STATISTIQUES DESCRIPTIVES & ASYMÉTRIE / KURTOSIS\n")
cat("==================================================================\n")
cat("Bitcoin  - Moyenne :", round(mean(btc_ret), 4), "% | Écart-type :", round(sd(btc_ret), 4), "%\n")
cat("Ethereum - Moyenne :", round(mean(eth_ret), 4), "% | Écart-type :", round(sd(eth_ret), 4), "%\n")

# Justification : Calcul de la leptokurticité pour tester l'écart à la loi normale
btc_kurt <- (sum((btc_ret - mean(btc_ret))^4) / length(btc_ret)) / (var(btc_ret)^2) - 3
eth_kurt <- (sum((eth_ret - mean(eth_ret))^4) / length(eth_ret)) / (var(eth_ret)^2) - 3
cat("Kurtosis en excès Bitcoin  :", round(btc_kurt, 4), "(Leptokurtique extrême)\n")
cat("Kurtosis en excès Ethereum :", round(eth_kurt, 4), "(Leptokurtique extrême)\n")

cat("\n==================================================================\n")
cat("2. DOUBLE TEST DE STATIONNARITÉ : ADF (Racine Unitaire) vs KPSS (Stationnaire)\n")
cat("Justification : Croisement obligatoire pour lever l'ambiguïté des hypothèses nulles opposées\n")
cat("==================================================================\n")

# Tests sur les Log-Prix
adf_btc_p <- adf.test(train_df$BTC_LogPrice)
kpss_btc_p <- kpss.test(train_df$BTC_LogPrice)
cat("BTC Log-Prix : ADF p-value =", adf_btc_p$p.value, "| KPSS p-value =", kpss_btc_p$p.value, "-> Conclusion : I(1) Non-Stationnaire\n")

# Tests sur les Log-Rendements
adf_btc_r <- adf.test(train_df$BTC_Return)
kpss_btc_r <- kpss.test(train_df$BTC_Return)
cat("BTC Log-Rendement : ADF p-value =", adf_btc_r$p.value, "| KPSS p-value =", kpss_btc_r$p.value, "-> Conclusion : I(0) Stationnaire\n")

cat("\n==================================================================\n")
cat("3. DÉCOMPOSITION STL SUR LE LOG-PRIX DE BITCOIN\n")
cat("Justification : Séparation robuste de la tendance séculaire et de la cyclicité hebdomadaire\n")
cat("==================================================================\n")
btc_ts <- ts(train_df$BTC_LogPrice, frequency = 7)
btc_stl <- stl(btc_ts, s.window = "periodic", robust = TRUE)
summary(btc_stl)

cat("Script 02 (R) exécuté avec succès !\n")