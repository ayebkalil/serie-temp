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
train_df <- read.csv("C:/Users/ayebk/OneDrive/Desktop/serie temp/data/crypto_btc_eth_bnb_train.csv", stringsAsFactors = FALSE)
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
cat("1.BIS VISUALISATION DES DISTRIBUTIONS, ASYMÉTRIE ET QUEUES ÉPAISSES\n")
cat("==================================================================\n")
cat("Génération du graphique des distributions (Histograms + KDE vs Normale + Q-Q Plot)...\n")

# Configuration de la grille 2x2 dans RStudio
par(mfrow = c(2, 2), mar = c(4.5, 4.5, 3, 1))

# 1. Distribution Bitcoin (BTC)
hist(btc_ret, breaks = 60, probability = TRUE, col = rgb(0.95, 0.6, 0.1, 0.5), border = "white",
     xlim = c(-25, 20), main = "BTC: Skew = -1.07 | Kurt = +18.86 (Queues Épaisses)",
     xlab = "Rendement Journalier (%)", ylab = "Densité")
lines(density(btc_ret), col = "#d35400", lwd = 2.5)
curve(dnorm(x, mean = mean(btc_ret), sd = sd(btc_ret)), add = TRUE, col = "black", lty = 2, lwd = 2)
legend("topright", legend = c("Densité Réelle", "Loi Normale"), col = c("#d35400", "black"), 
       lty = c(1, 2), lwd = 2, bty = "n")

# 2. Distribution Ethereum (ETH)
hist(eth_ret, breaks = 60, probability = TRUE, col = rgb(0.2, 0.6, 0.9, 0.5), border = "white",
     xlim = c(-25, 20), main = "ETH: Skew = -0.99 | Kurt = +14.42 (Queues Épaisses)",
     xlab = "Rendement Journalier (%)", ylab = "Densité")
lines(density(eth_ret), col = "#2980b9", lwd = 2.5)
curve(dnorm(x, mean = mean(eth_ret), sd = sd(eth_ret)), add = TRUE, col = "black", lty = 2, lwd = 2)
legend("topright", legend = c("Densité Réelle", "Loi Normale"), col = c("#2980b9", "black"), 
       lty = c(1, 2), lwd = 2, bty = "n")

# 3. Distribution Binance Coin (BNB)
hist(bnb_ret, breaks = 60, probability = TRUE, col = rgb(0.95, 0.77, 0.05, 0.5), border = "white",
     xlim = c(-25, 20), main = "BNB: Skew = -0.17 | Kurt = +24.44 (Queues Épaisses)",
     xlab = "Rendement Journalier (%)", ylab = "Densité")
lines(density(bnb_ret), col = "#d4ac0d", lwd = 2.5)
curve(dnorm(x, mean = mean(bnb_ret), sd = sd(bnb_ret)), add = TRUE, col = "black", lty = 2, lwd = 2)
legend("topright", legend = c("Densité Réelle", "Loi Normale"), col = c("#d4ac0d", "black"), 
       lty = c(1, 2), lwd = 2, bty = "n")

# 4. Q-Q Plot Bitcoin vs Loi Normale (Droite de Henry)
qqnorm(btc_ret, main = "Q-Q Plot BTC vs Loi Normale (Droite de Henry)", 
       col = rgb(0.95, 0.6, 0.1, 0.6), pch = 20,
       xlab = "Quantiles Théoriques (Normale)", ylab = "Quantiles Observés (%)")
qqline(btc_ret, col = "black", lwd = 2, lty = 2)
grid()

# Sauvegarde également en haute résolution dans le dossier plots/
if (!dir.exists("plots")) dir.create("plots")
png("plots/fig1b_distributions_skew_kurtosis.png", width = 1200, height = 800, res = 130)
par(mfrow = c(2, 2), mar = c(4.5, 4.5, 3, 1))
hist(btc_ret, breaks = 60, probability = TRUE, col = rgb(0.95, 0.6, 0.1, 0.5), border = "white",
     xlim = c(-25, 20), main = "BTC: Skew = -1.07 | Kurt = +18.86 (Queues Épaisses)",
     xlab = "Rendement Journalier (%)", ylab = "Densité")
lines(density(btc_ret), col = "#d35400", lwd = 2.5)
curve(dnorm(x, mean = mean(btc_ret), sd = sd(btc_ret)), add = TRUE, col = "black", lty = 2, lwd = 2)
legend("topright", legend = c("Densité Réelle", "Loi Normale"), col = c("#d35400", "black"), lty = c(1, 2), lwd = 2, bty = "n")

hist(eth_ret, breaks = 60, probability = TRUE, col = rgb(0.2, 0.6, 0.9, 0.5), border = "white",
     xlim = c(-25, 20), main = "ETH: Skew = -0.99 | Kurt = +14.42 (Queues Épaisses)",
     xlab = "Rendement Journalier (%)", ylab = "Densité")
lines(density(eth_ret), col = "#2980b9", lwd = 2.5)
curve(dnorm(x, mean = mean(eth_ret), sd = sd(eth_ret)), add = TRUE, col = "black", lty = 2, lwd = 2)
legend("topright", legend = c("Densité Réelle", "Loi Normale"), col = c("#2980b9", "black"), lty = c(1, 2), lwd = 2, bty = "n")

hist(bnb_ret, breaks = 60, probability = TRUE, col = rgb(0.95, 0.77, 0.05, 0.5), border = "white",
     xlim = c(-25, 20), main = "BNB: Skew = -0.17 | Kurt = +24.44 (Queues Épaisses)",
     xlab = "Rendement Journalier (%)", ylab = "Densité")
lines(density(bnb_ret), col = "#d4ac0d", lwd = 2.5)
curve(dnorm(x, mean = mean(bnb_ret), sd = sd(bnb_ret)), add = TRUE, col = "black", lty = 2, lwd = 2)
legend("topright", legend = c("Densité Réelle", "Loi Normale"), col = c("#d4ac0d", "black"), lty = c(1, 2), lwd = 2, bty = "n")

qqnorm(btc_ret, main = "Q-Q Plot BTC vs Loi Normale (Droite de Henry)", col = rgb(0.95, 0.6, 0.1, 0.6), pch = 20,
       xlab = "Quantiles Théoriques (Normale)", ylab = "Quantiles Observés (%)")
qqline(btc_ret, col = "black", lwd = 2, lty = 2)
grid()
dev.off()
cat("-> Graphique enregistré dans plots/fig1b_distributions_skew_kurtosis.png\n")

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
plot(btc_stl, main = "Décomposition STL du Log-Prix BTC (Saisonnalité 7 jours)")

cat("\nScript 02 (R) 3-Actifs exécuté avec succès !\n")
