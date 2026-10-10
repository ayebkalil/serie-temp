# ==============================================================================
# SCRIPT 05 : CORRÉLATION DYNAMIQUE TRIVARIÉE ET MULTI-HORIZONS (2019-2026)
# ==============================================================================

suppressPackageStartupMessages({
  library(zoo)
  library(Metrics)
})

full_df <- read.csv("data/crypto_btc_eth_bnb_full.csv", stringsAsFactors = FALSE)
full_df$Date <- as.Date(full_df$Date)

# Corrélation glissante sur 60 jours
roll_btc_eth <- rollapply(zoo(full_df[, c("BTC_Return", "ETH_Return")], order.by = full_df$Date),
                          width = 60, function(x) cor(x[, 1], x[, 2]), by.column = FALSE, align = "right")
roll_btc_bnb <- rollapply(zoo(full_df[, c("BTC_Return", "BNB_Return")], order.by = full_df$Date),
                          width = 60, function(x) cor(x[, 1], x[, 2]), by.column = FALSE, align = "right")
roll_eth_bnb <- rollapply(zoo(full_df[, c("ETH_Return", "BNB_Return")], order.by = full_df$Date),
                          width = 60, function(x) cor(x[, 1], x[, 2]), by.column = FALSE, align = "right")

cat("==================================================================\n")
cat("1. MATRICE DE CORRÉLATION STATIQUE VS DYNAMIQUE (2019-2026)\n")
cat("==================================================================\n")
cat("Corrélation statique BTC-ETH :", round(cor(full_df$BTC_Return, full_df$ETH_Return), 4), "\n")
cat("Corrélation statique BTC-BNB :", round(cor(full_df$BTC_Return, full_df$BNB_Return), 4), "\n")
cat("Corrélation statique ETH-BNB :", round(cor(full_df$ETH_Return, full_df$BNB_Return), 4), "\n")

test_df <- read.csv("data/crypto_btc_eth_bnb_test.csv", stringsAsFactors = FALSE)
actual <- test_df$BTC_Close

horizons <- c(1, 5, 7, 10)
cat("\n==================================================================\n")
cat("2. PRÉVISIONS MULTI-HORIZONS EN R (TEST SET 2026 : 281 JOURS)\n")
cat("==================================================================\n")

for (h in horizons) {
  preds <- c(rep(actual[1], h), actual[1:(length(actual) - h)])
  val_rmse <- rmse(actual[-(1:h)], preds[-(1:h)])
  val_mae  <- mae(actual[-(1:h)],  preds[-(1:h)])
  val_mape <- mape(actual[-(1:h)], preds[-(1:h)]) * 100
  cat(sprintf("Horizon h = %2d jours : RMSE = %8.2f $ | MAE = %8.2f $ | MAPE = %5.2f %%\n",
              h, val_rmse, val_mae, val_mape))
}

cat("\nScript 05 (R) exécuté avec succès !\n")