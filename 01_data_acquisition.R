# ==============================================================================
# SCRIPT 01 : ACQUISITION ET PRÉPARATION DES DONNÉES (BTC, ETH, BNB 2019-2026)
# Justification : Collecte continue 24/7 sur 3 cryptomonnaies majeures
# ==============================================================================

suppressPackageStartupMessages({
  library(zoo)
  library(xts)
})
"C:/Users/ayebk/OneDrive/Desktop/serie temp/data/crypto_btc_eth_bnb_full.csv"
df_full <- read.csv("C:/Users/ayebk/OneDrive/Desktop/serie temp/data/crypto_btc_eth_bnb_full.csv"
, stringsAsFactors = FALSE)
df_full$Date <- as.Date(df_full$Date)

cat("Nombre total d'observations journalières (2019-2026) :", nrow(df_full), "\n")
cat("Période couverte : du", as.character(min(df_full$Date)), "au", as.character(max(df_full$Date)), "\n")

n_total <- nrow(df_full)
n_train <- floor(n_total * 0.90)
n_test  <- n_total - n_train

train_df <- df_full[1:n_train, ]
test_df  <- df_full[(n_train + 1):n_total, ]

cat("Taille Train (90%) :", nrow(train_df), "jours\n")
cat("Taille Test  (10%) :", nrow(test_df),  "jours\n")

cat("Script 01 (R) 3-Actifs exécuté avec succès !\n")

