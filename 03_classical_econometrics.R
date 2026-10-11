# ==============================================================================
# SCRIPT 03 : MODÈLES ÉCONOMÉTRIQUES CLASSIQUES EN R (BTC, ETH, BNB 2019-2026)
# Justification : Estimation R du socle classique (Section 3 du barème)
# ==============================================================================

suppressPackageStartupMessages({
  library(tseries)
  library(forecast)
  library(vars)
  library(urca)
  library(fGarch)
})

cat("--- Chargement des données d'apprentissage (2019-2025) ---\n")
train_df <- read.csv("C:/Users/ayebk/OneDrive/Desktop/serie temp/data/crypto_btc_eth_bnb_train.csv", stringsAsFactors = FALSE)
train_df$Date <- as.Date(train_df$Date)

btc_ret <- train_df$BTC_Return
eth_ret <- train_df$ETH_Return
bnb_ret <- train_df$BNB_Return

# 3.1 Modélisation ARIMA sur les rendements de Bitcoin
cat("\n==================================================================\n")
cat("3.1 MODÉLISATION ARIMA SUR LES RENDEMENTS BTC (auto.arima)\n")
cat("==================================================================\n")
arima_r <- auto.arima(btc_ret, seasonal = FALSE, stepwise = TRUE, ic = "aic")
print(summary(arima_r))

cat("\nDiagnostics des résidus ARIMA :\n")
print(checkresiduals(arima_r))
print(jarque.bera.test(residuals(arima_r)))

# 3.2 Modélisation Multivariée : VAR(3 Actifs) & Causalité de Granger
cat("\n==================================================================\n")
cat("3.2 SYSTÈME VAR TRIVARIÉ ET RÉSEAU DE CAUSALITÉ DE GRANGER\n")
cat("==================================================================\n")
var_data <- data.frame(BTC = btc_ret, ETH = eth_ret, BNB = bnb_ret)
var_select <- VARselect(var_data, lag.max = 10, type = "const")
print(var_select$selection)

p_opt <- var_select$selection["AIC(n)"]
var_fit <- VAR(var_data, p = p_opt, type = "const")
cat("VAR trivarié ajusté avec p =", p_opt, "\n")

cat("\nCausalité au sens de Granger :\n")
cat("ETH -> BTC :\n"); print(causality(var_fit, cause = "ETH")$Granger)
cat("BTC -> ETH :\n"); print(causality(var_fit, cause = "BTC")$Granger)
cat("ETH -> BNB :\n"); print(causality(var_fit, cause = "ETH")$Granger)

# 3.3 Test de Cointégration de Johansen (3 Actifs)
cat("\n==================================================================\n")
cat("3.3 TEST DE COINTÉGRATION DE JOHANSEN TRIVARIÉ (urca)\n")
cat("==================================================================\n")
price_data <- data.frame(BTC_Log = train_df$BTC_LogPrice, ETH_Log = train_df$ETH_LogPrice, BNB_Log = train_df$BNB_LogPrice)
coint_test <- ca.jo(price_data, type = "trace", ecdet = "const", K = p_opt)
print(summary(coint_test))

# 3.4 Modélisation GARCH(1,1) avec loi de Student
cat("\n==================================================================\n")
cat("3.4 VOLATILITÉ CONDITIONNELLE GARCH(1,1) - LOI DE STUDENT (fGarch)\n")
cat("==================================================================\n")
garch_r <- garchFit(~ arma(1,0) + garch(1,1), data = btc_ret, cond.dist = "std", trace = FALSE)
print(summary(garch_r))

cat("\nScript 03 (R) 3-Actifs exécuté avec succès !\n")

