# ==============================================================================
# SCRIPT 01 : ACQUISITION ET PRÉPARATION DES DONNÉES (BTC, ETH, BNB 2019-2026)
# Justification : Collecte continue 24/7 sur 3 cryptomonnaies majeures
# ==============================================================================

suppressPackageStartupMessages({
  library(zoo)
  library(xts)
})

# 1. Chargement du dataset complet (2019 - 2026)
data_path <- "C:/Users/ayebk/OneDrive/Desktop/serie temp/data/crypto_btc_eth_bnb_full.csv"
df_full <- read.csv(data_path, stringsAsFactors = FALSE)
df_full$Date <- as.Date(df_full$Date)

cat("==================================================================\n")
cat("1. RÉCAPITULATIF DES DONNÉES BRUTES (2019 - 2026)\n")
cat("==================================================================\n")
cat("Nombre total d'observations journalières :", nrow(df_full), "jours\n")
cat("Période couverte : du", as.character(min(df_full$Date)), "au", as.character(max(df_full$Date)), "\n")

# 2. Découpage chronologique strict Train (90%) / Test (10%)
n_total <- nrow(df_full)
n_train <- floor(n_total * 0.90)
n_test  <- n_total - n_train

train_df <- df_full[1:n_train, ]
test_df  <- df_full[(n_train + 1):n_total, ]

split_date <- test_df$Date[1]

cat("Taille Train (90%) :", nrow(train_df), "jours (du", as.character(min(train_df$Date)), "au", as.character(max(train_df$Date)), ")\n")
cat("Taille Test  (10%) :", nrow(test_df),  "jours (du", as.character(min(test_df$Date)),  "au", as.character(max(test_df$Date)),  ")\n")
cat("Date frontière Train/Test :", as.character(split_date), "\n")

# ==============================================================================
# 3. VISUALISATION DES SÉRIES TEMPORELLES (LOG-PRIX & RENDEMENTS JOURNALIERS)
# ==============================================================================
cat("\n==================================================================\n")
cat("2. VISUALISATION DES TRAJECTOIRES ET DES CHOCS MAJEURS\n")
cat("==================================================================\n")
cat("Affichage dans la fenêtre graphique RStudio et enregistrement dans plots/...\n")

# Fonction interne pour tracer les deux panneaux
draw_overview_plots <- function() {
  par(mfrow = c(2, 1), mar = c(4, 4.5, 2.5, 1))

  # --- PANNEAU 1 : Trajectoires des Log-Prix & Frontière Train/Test ---
  min_lp <- min(c(df_full$BTC_LogPrice, df_full$ETH_LogPrice, df_full$BNB_LogPrice), na.rm = TRUE)
  max_lp <- max(c(df_full$BTC_LogPrice, df_full$ETH_LogPrice, df_full$BNB_LogPrice), na.rm = TRUE)

  plot(df_full$Date, df_full$BTC_LogPrice, type = "l", col = "#d35400", lwd = 2,
       ylim = c(min_lp - 0.5, max_lp + 1.2),
       main = "Trajectoires des Log-Prix (2019-2026) : BTC, ETH, BNB & Découpage Train/Test (90/10)",
       xlab = "Date", ylab = "Log-Prix (USD)")
  lines(df_full$Date, df_full$ETH_LogPrice, col = "#2980b9", lwd = 2)
  lines(df_full$Date, df_full$BNB_LogPrice, col = "#8e44ad", lwd = 2)
  grid()

  # Ligne verticale de séparation Train / Test
  abline(v = split_date, col = "red", lty = 2, lwd = 2)
  text(split_date + 15, max_lp + 0.8, labels = paste("Test Set (10%)\n281 jours"), 
       col = "red", adj = 0, cex = 0.85, font = 2)

  # Annotations des 3 Chocs Majeurs sur le Log-Prix
  covid_date <- as.Date("2020-03-12")
  china_date <- as.Date("2021-05-19")
  ftx_date   <- as.Date("2022-11-11")

  points(c(covid_date, china_date, ftx_date), 
         c(df_full$BTC_LogPrice[df_full$Date == covid_date], 
           df_full$BTC_LogPrice[df_full$Date == china_date], 
           df_full$BTC_LogPrice[df_full$Date == ftx_date]), 
         col = "red", pch = 19, cex = 1.2)

  text(covid_date, 7.8,  labels = "1. Covid-19 (-40%)", col = "black", cex = 0.78, font = 2)
  text(china_date, 11.4, labels = "2. Chine Ban (-50%)", col = "black", cex = 0.78, font = 2)
  text(ftx_date,   9.2,  labels = "3. Crash FTX",        col = "black", cex = 0.78, font = 2)

  legend("topleft", 
         legend = c("Bitcoin (BTC)", "Ethereum (ETH)", "Binance Coin (BNB)", "Frontière Train/Test (90/10)"),
         col = c("#d35400", "#2980b9", "#8e44ad", "red"), 
         lty = c(1, 1, 1, 2), lwd = 2, bty = "n", cex = 0.85)

  # --- PANNEAU 2 : Rendements Journaliers (%) & Regroupement de Volatilité ---
  plot(df_full$Date, df_full$BTC_Return, type = "l", col = rgb(0.95, 0.6, 0.1, 0.55), lwd = 1,
       ylim = c(-45, 35),
       main = "Rendements Journaliers (%) & Regroupements de Volatilité (Stationnaires I(0))",
       xlab = "Date", ylab = "Rendement Journalier (%)")
  lines(df_full$Date, df_full$ETH_Return, col = rgb(0.16, 0.5, 0.73, 0.45), lwd = 1)
  lines(df_full$Date, df_full$BNB_Return, col = rgb(0.56, 0.27, 0.68, 0.45), lwd = 1)
  abline(h = 0, col = "gray40", lty = 3)
  abline(v = split_date, col = "red", lty = 2, lwd = 2)
  grid()

  legend("topright", 
         legend = c("BTC Rendement", "ETH Rendement", "BNB Rendement"),
         col = c("#d35400", "#2980b9", "#8e44ad"), 
         lty = 1, lwd = 1.5, bty = "n", cex = 0.85)
}

# 1. Tracé interactif dans RStudio (dans l'onglet Plots)
draw_overview_plots()

# 2. Sauvegarde automatique en haute définition dans le dossier plots/
if (!dir.exists("plots")) dir.create("plots")
png("plots/fig1_prices_and_returns.png", width = 1200, height = 800, res = 130)
draw_overview_plots()
dev.off()

cat("-> Graphique interactif affiché dans RStudio (onglet Plots) !\n")
cat("-> Graphique haute résolution sauvegardé dans : plots/fig1_prices_and_returns.png\n")

cat("\nScript 01 (R) 3-Actifs exécuté avec succès !\n")
