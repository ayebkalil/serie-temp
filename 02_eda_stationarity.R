# ==============================================================================
# SCRIPT 02 : ANALYSE EXPLORATOIRE ET TESTS DE STATIONNARITÉ EN R (3 ACTIFS)
# Actifs analysés : Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB) [2019-2026]
# ==============================================================================

suppressPackageStartupMessages({
  library(tseries)
  library(forecast)
  library(zoo)
})

cat("--- Chargement des données d'apprentissage 3-Actifs (2019-2025) ---\n")
train_df <- read.csv("data/crypto_btc_eth_bnb_train.csv", stringsAsFactors = FALSE)
train_df$Date <- as.Date(train_df$Date)

btc_ret <- train_df$BTC_Return
eth_ret <- train_df$ETH_Return
bnb_ret <- train_df$BNB_Return

cat("==================================================================\n")
cat("1. STATISTIQUES DESCRIPTIVES & MOMENTS D'ORDRE SUPÉRIEUR (TRAIN)\n")
cat("==================================================================\n")
cat(sprintf("Bitcoin  (BTC) - Moyenne: %+7.4f %% | Écart-type: %6.4f %%\n", mean(btc_ret), sd(btc_ret)))
cat(sprintf("Ethereum (ETH) - Moyenne: %+7.4f %% | Écart-type: %6.4f %%\n", mean(eth_ret), sd(eth_ret)))
cat(sprintf("Binance  (BNB) - Moyenne: %+7.4f %% | Écart-type: %6.4f %%\n", mean(bnb_ret), sd(bnb_ret)))

# Calcul du kurtosis en excès (Leptokurticité)
calc_kurt <- function(x) {
  (sum((x - mean(x))^4) / length(x)) / (var(x)^2) - 3
}
# Calcul du skewness (Asymétrie)
calc_skew <- function(x) {
  (sum((x - mean(x))^3) / length(x)) / (sd(x)^3)
}

cat("\nAsymétrie (Skewness) :\n")
cat(sprintf("BTC: %+7.4f | ETH: %+7.4f | BNB: %+7.4f (Chocs baissiers plus violents)\n", 
            calc_skew(btc_ret), calc_skew(eth_ret), calc_skew(bnb_ret)))

cat("Kurtosis en excès (Queues Épaisses) :\n")
cat(sprintf("BTC: %+7.4f | ETH: %+7.4f | BNB: %+7.4f (Leptokurticité extrême, non-normalité)\n", 
            calc_kurt(btc_ret), calc_kurt(eth_ret), calc_kurt(bnb_ret)))

# Test de normalité de Jarque-Bera
cat("\nTests de Normalité de Jarque-Bera :\n")
cat("BTC JB p-value :", jarque.bera.test(btc_ret)$p.value, "\n")
cat("ETH JB p-value :", jarque.bera.test(eth_ret)$p.value, "\n")
cat("BNB JB p-value :", jarque.bera.test(bnb_ret)$p.value, "\n")

cat("\n==================================================================\n")
cat("2. DOUBLE TEST DE STATIONNARITÉ (ADF vs KPSS) SUR LES 3 ACTIFS\n")
cat("==================================================================\n")

assets <- c("BTC", "ETH", "BNB")
for (coin in assets) {
  log_p <- train_df[[paste0(coin, "_LogPrice")]]
  ret   <- train_df[[paste0(coin, "_Return")]]
  
  cat(paste0("\n--- Actif : ", coin, " ---\n"))
  adf_p  <- adf.test(log_p)
  kpss_p <- kpss.test(log_p)
  cat(sprintf("  Log-Prix   : ADF p = %.4f | KPSS p = %.4f -> Conclusion : I(1) Non-stationnaire\n", 
              adf_p$p.value, kpss_p$p.value))
  
  adf_r  <- adf.test(ret)
  kpss_r <- kpss.test(ret)
  cat(sprintf("  Log-Rend.  : ADF p = %.4f | KPSS p = %.4f -> Conclusion : I(0) Stationnaire\n", 
              adf_r$p.value, kpss_r$p.value))
}

cat("\n==================================================================\n")
cat("3. DÉCOMPOSITION STL SUR LE LOG-PRIX DE BITCOIN (Fréquence = 7j)\n")
cat("==================================================================\n")
btc_ts <- ts(train_df$BTC_LogPrice, frequency = 7)
btc_stl <- stl(btc_ts, s.window = "periodic", robust = TRUE)
print(summary(btc_stl))

cat("\nScript 02 (R) 3-Actifs exécuté avec succès !\n")