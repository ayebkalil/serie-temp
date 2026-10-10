import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BG = RGBColor(15, 23, 42)       # Slate 900
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_BLUE = RGBColor(37, 99, 235)  # Blue 600
    ACCENT_CYAN = RGBColor(14, 165, 233) # Sky 500
    ACCENT_EMERALD = RGBColor(16, 185, 129) # Emerald 500
    ACCENT_AMBER = RGBColor(245, 158, 11) # Amber 500
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text, speaker_text=None):
        # Header background banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = RGBColor(15, 23, 42)
        header_shape.line.color.rgb = RGBColor(30, 41, 59)

        # Category / Section pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(6), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN
        p_cat.font.name = "Segoe UI"

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT
        p_title.font.name = "Segoe UI"

        # Speaker Badge (if provided)
        if speaker_text:
            badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.8), Inches(0.3), Inches(2.7), Inches(0.45))
            badge.fill.solid()
            badge.fill.fore_color.rgb = RGBColor(30, 41, 59)
            badge.line.color.rgb = ACCENT_BLUE
            tf_badge = badge.text_frame
            p_badge = tf_badge.paragraphs[0]
            p_badge.text = f"Speaker: {speaker_text}"
            p_badge.font.size = Pt(11)
            p_badge.font.bold = True
            p_badge.font.color.rgb = TEXT_LIGHT
            p_badge.alignment = PP_ALIGN.CENTER
            p_badge.font.name = "Segoe UI"

    def set_slide_background(slide, color=DARK_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def create_card(slide, left, top, width, height, title="", border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        if title:
            tbox = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.4))
            tf = tbox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
            p.font.name = "Segoe UI"
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, RGBColor(10, 15, 30))

    # Center hero card
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(0.8), Inches(10.333), Inches(5.9))
    hero.fill.solid()
    hero.fill.fore_color.rgb = CARD_BG
    hero.line.color.rgb = ACCENT_BLUE
    hero.line.width = Pt(2)

    # University header tag
    u_box = s1.shapes.add_textbox(Inches(2.0), Inches(1.2), Inches(9.3), Inches(0.4))
    tf_u = u_box.text_frame
    p_u = tf_u.paragraphs[0]
    p_u.text = "TEK-UP UNIVERSITY • DATA SCIENCE & AI ENGINEERING • 2026"
    p_u.font.size = Pt(13)
    p_u.font.bold = True
    p_u.font.color.rgb = ACCENT_CYAN
    p_u.alignment = PP_ALIGN.CENTER
    p_u.font.name = "Segoe UI"

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(2.0), Inches(1.7), Inches(9.3), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Comparative Econometric Modeling &\nDeep Learning Forecasting of Crypto Assets"
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_LIGHT
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Segoe UI"

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(2.0), Inches(3.6), Inches(9.3), Inches(0.6))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Multi-Asset Empirical Study (BTC, ETH, BNB) with Generative AI Audit"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Segoe UI"

    # Divider line
    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(4.3), Inches(4.3), Inches(0.04))
    div.fill.solid()
    div.fill.fore_color.rgb = ACCENT_BLUE
    div.line.fill.background()

    # Team members grid
    team_box = s1.shapes.add_textbox(Inches(2.0), Inches(4.5), Inches(9.3), Inches(1.2))
    tf_team = team_box.text_frame
    tf_team.word_wrap = True
    
    p_team_title = tf_team.paragraphs[0]
    p_team_title.text = "Presented by Team 4:"
    p_team_title.font.size = Pt(13)
    p_team_title.font.bold = True
    p_team_title.font.color.rgb = ACCENT_EMERALD
    p_team_title.alignment = PP_ALIGN.CENTER

    p_members = tf_team.add_paragraph()
    p_members.text = "Rawen Bejie  •  Khawla Hawari  •  Amine Benfadhel  •  Khalil Ayeb"
    p_members.font.size = Pt(15)
    p_members.font.bold = True
    p_members.font.color.rgb = TEXT_LIGHT
    p_members.alignment = PP_ALIGN.CENTER

    p_sup = tf_team.add_paragraph()
    p_sup.text = "Supervised by: Prof. Ahmed Dhouibi"
    p_sup.font.size = Pt(12)
    p_sup.font.italic = True
    p_sup.font.color.rgb = TEXT_MUTED
    p_sup.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: CONTEXT, PROBLEM & DATA PIPELINE
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Data Engineering Pipeline", "1. Introduction & Data", "Rawen Bejie")

    # Card 1: Problem Formulation
    create_card(s2, 0.8, 1.4, 5.6, 5.5, "🎯 The Core Research Question")
    c1_box = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True
    
    bullets_c1 = [
        ("Central Question:", True, ACCENT_AMBER),
        ("Can non-linear Deep Learning models (LSTM/GRU) outperform classical econometric baselines (ARIMA, VAR) and the Naïve Random Walk in high-frequency crypto price forecasting?", False, TEXT_LIGHT),
        ("Why Crypto Assets? (BTC, ETH, BNB):", True, ACCENT_AMBER),
        ("• Extreme volatility and non-stationary dynamics ($I(1)$).\n• 24/7/365 uninterrupted trading (no weekend seasonality).\n• Complex interconnectedness and regime shifts.", False, TEXT_MUTED),
        ("Key Econometric Rule:", True, ACCENT_AMBER),
        ("Every model must be statistically diagnosed. A sophisticated model without residual validation will be scientifically rejected.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c1):
        p = tf_c1.paragraphs[0] if i == 0 else tf_c1.add_paragraph()
        p.text = txt
        p.font.size = Pt(12)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # Card 2: Data Pipeline & Split
    create_card(s2, 6.8, 1.4, 5.7, 5.5, "📦 Data Acquisition & Split Architecture")
    c2_box = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True

    bullets_c2 = [
        ("Dataset Parameters:", True, ACCENT_CYAN),
        ("• Period: Jan 31, 2019 to Oct 03, 2026 (7.7 years of daily data).\n• Sample Size: 2,803 daily observations across 3 assets.\n• Automated fallback pipeline via yfinance API.", False, TEXT_LIGHT),
        ("Zero Look-Ahead Bias Protocol:", True, ACCENT_CYAN),
        ("• Chronological split: 90% Train / 10% Out-of-Sample Test.\n• Train: 2,522 days (Jan 31, 2019 to Dec 26, 2025).\n• Test: 281 days (Dec 27, 2025 to Oct 03, 2026).\n• No future data leakage: Normalization fit strictly on Train.", False, TEXT_MUTED),
        ("Derived Features Engineered:", True, ACCENT_CYAN),
        ("• Daily Log-Returns: r_t = 100 * ln(P_t / P_{t-1})\n• 30-day Annualized Realized Volatility (Vol30)\n• 30-day Simple Moving Averages (SMA30) & 24h Trading Volumes", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c2):
        p = tf_c2.paragraphs[0] if i == 0 else tf_c2.add_paragraph()
        p.text = txt
        p.font.size = Pt(12)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 3: EDA & STATIONARITY ANALYSIS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Exploratory Analysis & Stationarity Diagnostics", "2. Statistical Foundations", "Khawla Hawari")

    # Image Left
    create_card(s3, 0.8, 1.4, 6.2, 5.5, "📊 STL Decomposition & Price Dynamics")
    stl_path = "plots/fig3_stl_decomposition.png"
    if os.path.exists(stl_path):
        s3.shapes.add_picture(stl_path, Inches(1.0), Inches(2.0), width=Inches(5.8))

    # Card Right: Stationarity & Decomposition Results
    create_card(s3, 7.3, 1.4, 5.2, 5.5, "🔬 Rigorous Diagnostic Results")
    c3_box = s3.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.6))
    tf_c3 = c3_box.text_frame
    tf_c3.word_wrap = True

    bullets_c3 = [
        ("STL Decomposition Findings:", True, ACCENT_AMBER),
        ("• Trend: Dominates >95% of total price variance.\n• Seasonality: Negligible (<2% variance). Daily crypto trading exhibits no strong 7-day or monthly calendar cycle.\n• Outliers: March 2020 (Covid) & Nov 2022 (FTX) retained as true market regime shocks.", False, TEXT_LIGHT),
        ("Dual Stationarity Testing (ADF + KPSS):", True, ACCENT_CYAN),
        ("• Raw Prices & Log-Prices: Non-Stationary I(1)\n  ADF p = 0.88 (cannot reject unit root)\n  KPSS p = 0.01 (rejects stationarity)\n• Log-Returns: Strictly Stationary I(0)\n  ADF p < 0.001 (unit root strongly rejected)\n  KPSS p = 0.10 (stationarity cannot be rejected)", False, TEXT_MUTED),
        ("Methodological Decision:", True, ACCENT_EMERALD),
        ("Classical models (ARIMA, VAR) must be estimated strictly on stationary log-returns to avoid spurious regressions.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c3):
        p = tf_c3.paragraphs[0] if i == 0 else tf_c3.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 4: ARIMA & RESIDUAL DIAGNOSTICS
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "ARIMA Modeling & Mandatory Residual Diagnostics", "3. Classical Econometrics", "Khawla Hawari")

    # Image Left
    create_card(s4, 0.8, 1.4, 6.2, 5.5, "📉 Autocorrelation Functions (ACF & PACF)")
    acf_path = "plots/fig2_acf_pacf.png"
    if os.path.exists(acf_path):
        s4.shapes.add_picture(acf_path, Inches(1.0), Inches(2.0), width=Inches(5.8))

    # Card Right: Model & Diagnostics
    create_card(s4, 7.3, 1.4, 5.2, 5.5, "🧪 Three Essential Residual Tests")
    c4_box = s4.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.6))
    tf_c4 = c4_box.text_frame
    tf_c4.word_wrap = True

    bullets_c4 = [
        ("Selected Specification:", True, ACCENT_CYAN),
        ("• ARIMA(1,0,1) / ARMA(1,1) on BTC Returns.\n• AR(1) = -0.6376, MA(1) = 0.5865 (p < 0.001).\n• Minimizes AIC / BIC against higher-order candidates.", False, TEXT_LIGHT),
        ("1. Ljung-Box Test (White Noise):", True, ACCENT_EMERALD),
        ("• Q(10) = 14.28, p-value = 0.160 (> 0.05)\n• Conclusion: No remaining autocorrelation in residuals! The mean dynamics are cleanly captured.", False, TEXT_LIGHT),
        ("2. Jarque-Bera Test (Normality):", True, ACCENT_AMBER),
        ("• JB stat = 4,281, p < 10^-16\n• Conclusion: Heavy fat tails and leptokurtic distribution (Gaussian assumption rejected).", False, TEXT_MUTED),
        ("3. Engle ARCH-LM Test (Volatility Clustering):", True, ACCENT_AMBER),
        ("• LM stat = 128.4, p < 10^-16\n• Conclusion: Severe conditional heteroskedasticity detected! Proves that a GARCH model is strictly required.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c4):
        p = tf_c4.paragraphs[0] if i == 0 else tf_c4.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 5: MULTIVARIATE VAR & COINTEGRATION
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Multivariate Systems: VAR(5), Granger & Cointegration", "3. Classical Econometrics", "Khawla Hawari")

    # Card 1: VAR & Granger
    create_card(s5, 0.8, 1.4, 5.6, 5.5, "🔗 VAR(5) & Granger Causality Dynamics")
    c5_1 = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_c5_1 = c5_1.text_frame
    tf_c5_1.word_wrap = True

    bullets_c5_1 = [
        ("VAR(5) Lag Optimization:", True, ACCENT_CYAN),
        ("• Estimated on 3-variable stationary vector: [BTC, ETH, BNB log-returns].\n• Information criteria (AIC / FPE) select optimal order p = 5.", False, TEXT_LIGHT),
        ("Granger Causality Matrix (3x3):", True, ACCENT_AMBER),
        ("• ETH Returns -> BTC Returns: F = 2.94, p = 0.012 *\n• BNB Returns -> BTC Returns: F = 2.37, p = 0.038 *\n• BTC Returns -> ETH Returns: F = 3.15, p = 0.008 **", False, TEXT_MUTED),
        ("Key Methodological Nuance:", True, ACCENT_EMERALD),
        ("Granger causality indicates PREDICTIVE PRECEDENCE in information diffusion, NOT physical or legal causation.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c5_1):
        p = tf_c5_1.paragraphs[0] if i == 0 else tf_c5_1.add_paragraph()
        p.text = txt
        p.font.size = Pt(12)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # Card 2: Johansen & Why No VECM
    create_card(s5, 6.8, 1.4, 5.7, 5.5, "⚖️ Johansen Test & VECM Decision")
    c5_2 = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_c5_2 = c5_2.text_frame
    tf_c5_2.word_wrap = True

    bullets_c5_2 = [
        ("Johansen Cointegration Trace Test:", True, ACCENT_CYAN),
        ("• Python statsmodels (Case 2: det_order=0):\n  Trace Stat = 25.53 < Critical Value 29.80 (p > 0.05)\n• R urca (Case 3: ecdet='const'):\n  Trace Stat = 30.27 < Critical Value 34.91 (p > 0.05)\n• Both independent implementations confirm Rank r = 0.", False, TEXT_LIGHT),
        ("Why NO VECM? (Critical Defense Point!):", True, ACCENT_AMBER),
        ("• A Vector Error Correction Model (VECM) mathematically requires at least one cointegrating vector (r >= 1).\n• Running a VECM with r = 0 is an econometric specification error!\n• The correct and sound procedure is modeling in stationary log-returns via VAR(5).", False, TEXT_MUTED),
        ("Oral Defense Shield:", True, ACCENT_EMERALD),
        ("Absence of VECM is a proof of methodological rigor, not an omission.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c5_2):
        p = tf_c5_2.paragraphs[0] if i == 0 else tf_c5_2.add_paragraph()
        p.text = txt
        p.font.size = Pt(12)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 6: GARCH & VOLATILITY DYNAMICS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Conditional Volatility: GARCH(1,1) & GJR-GARCH", "4. Advanced Econometrics", "Amine Benfadhel")

    # Image Left
    create_card(s6, 0.8, 1.4, 6.2, 5.5, "🌪️ Conditional Volatility & Crisis Events")
    garch_path = "plots/fig4_garch_volatility_events.png"
    if os.path.exists(garch_path):
        s6.shapes.add_picture(garch_path, Inches(1.0), Inches(2.0), width=Inches(5.8))

    # Card Right
    create_card(s6, 7.3, 1.4, 5.2, 5.5, "📊 Estimated Parameters & Properties")
    c6_box = s6.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.6))
    tf_c6 = c6_box.text_frame
    tf_c6.word_wrap = True

    bullets_c6 = [
        ("GARCH(1,1) Specification:", True, ACCENT_CYAN),
        ("sigma_t^2 = omega + alpha * eps_{t-1}^2 + beta * sigma_{t-1}^2\n• omega = 1.10e-5 (p = 0.002)\n• alpha = 0.0631 (Shock reaction)\n• beta = 0.9272 (Storm persistence)", False, TEXT_LIGHT),
        ("Persistence & Stationarity:", True, ACCENT_AMBER),
        ("• alpha + beta = 0.9903 < 1.0\n• Strong persistence: market panics take weeks to dissipate.\n• Strictly covariance-stationary process.", False, TEXT_MUTED),
        ("Asymmetric GJR-GARCH Test:", True, ACCENT_CYAN),
        ("• Leverage term gamma = 0.0152 (p = 0.48, not significant).\n• Unlike traditional stocks, crypto exhibits symmetric volatility: major rallies trigger nearly the same volatility spikes as crashes.", False, TEXT_LIGHT),
        ("Standardized Residual Validation:", True, ACCENT_EMERALD),
        ("ARCH-LM on standardized residuals: p = 0.42 -> Conditional heteroskedasticity is successfully eliminated!", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c6):
        p = tf_c6.paragraphs[0] if i == 0 else tf_c6.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 7: DEEP LEARNING (LSTM VS GRU)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Deep Learning Architectures: PyTorch LSTM vs. GRU", "5. Deep Learning", "Amine Benfadhel")

    # Image Left
    create_card(s7, 0.8, 1.4, 6.2, 5.5, "⚡ Training & Validation Loss Curves")
    dl_path = "plots/fig5_loss_curves_lstm_gru.png"
    if os.path.exists(dl_path):
        s7.shapes.add_picture(dl_path, Inches(1.0), Inches(2.0), width=Inches(5.8))

    # Card Right
    create_card(s7, 7.3, 1.4, 5.2, 5.5, "🧠 Architecture & Complexity Comparison")
    c7_box = s7.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.6))
    tf_c7 = c7_box.text_frame
    tf_c7.word_wrap = True

    bullets_c7 = [
        ("Experimental Setup:", True, ACCENT_CYAN),
        ("• PyTorch implementation with Adam optimizer (lr = 0.001).\n• Sliding sequence window: L = 30 days.\n• Input dimension: 18 normalized features (Prices, Volumes, Returns, Vol30, SMA30 across 3 assets).\n• Target: BTC Log-Price at t+1.", False, TEXT_LIGHT),
        ("LSTM (Long Short-Term Memory):", True, ACCENT_AMBER),
        ("• 3 Gates: Input, Forget, Output + Cell State.\n• 2 layers, 64 hidden units = 25,217 parameters.\n• Slower convergence, higher risk of overfitting.", False, TEXT_MUTED),
        ("GRU (Gated Recurrent Unit):", True, ACCENT_EMERALD),
        ("• 2 Gates: Reset & Update (No separate cell state).\n• 2 layers, 64 hidden units = 19,073 parameters (24% fewer).\n• Converges faster and reaches lower validation MSE.", False, TEXT_LIGHT),
        ("Walk-Forward Inference:", True, ACCENT_CYAN),
        ("Rolling 1-step prediction across the entire 281-day test set.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c7):
        p = tf_c7.paragraphs[0] if i == 0 else tf_c7.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 8: THE FORECAST BENCHMARK
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Out-of-Sample Forecast Evaluation (281-Day Test)", "6. Forecast Evaluation", "Khalil Ayeb")

    # Table Left
    create_card(s8, 0.8, 1.4, 6.2, 5.5, "🏆 Master Metric Performance Table")
    
    # Add Table shape
    rows, cols = 7, 4
    left, top, width, height = Inches(1.0), Inches(2.1), Inches(5.8), Inches(4.5)
    table_shape = s8.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    headers = ["Model", "RMSE ($)", "MAE ($)", "MAPE (%)"]
    data_rows = [
        ["Naïve Random Walk (h=1)", "$1,725.43", "$1,164.85", "1.60% (1)"],
        ["Rolling ARIMA(1,0,1)", "$1,769.68", "$1,196.48", "1.65% (2)"],
        ["PyTorch GRU (h=1)", "$2,468.90", "$1,847.91", "2.56% (3)"],
        ["PyTorch LSTM (h=1)", "$3,776.48", "$3,396.66", "4.77% (4)"],
        ["Hybrid ARIMA-LSTM", "$15,319.04", "$13,967.77", "20.33% (5)"],
        ["Fixed ARIMA (h=281)", "$16,598.93", "$14,643.39", "21.49% (6)"]
    ]

    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = ACCENT_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

    for r, row in enumerate(data_rows):
        for c, val in enumerate(row):
            cell = table.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r % 2 == 0 else RGBColor(20, 30, 48)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = ACCENT_EMERALD if r == 0 else TEXT_LIGHT

    # Card Right: Forecast Image
    create_card(s8, 7.3, 1.4, 5.2, 5.5, "📈 Trajectory Comparison")
    fc_path = "plots/fig6_forecast_comparison.png"
    if os.path.exists(fc_path):
        s8.shapes.add_picture(fc_path, Inches(7.5), Inches(2.0), width=Inches(4.8))

    # ==========================================
    # SLIDE 9: DIEBOLD-MARIANO & EMH
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Statistical Significance: Diebold-Mariano Tests", "6. Forecast Evaluation", "Khalil Ayeb")

    # Card 1: DM Tests
    create_card(s9, 0.8, 1.4, 5.6, 5.5, "📐 Like-for-Like Diebold-Mariano (h=1)")
    c9_1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_c9_1 = c9_1.text_frame
    tf_c9_1.word_wrap = True

    bullets_c9_1 = [
        ("Newey-West HAC Robust Testing:", True, ACCENT_CYAN),
        ("Tested on matched 1-step forecast errors across 281 days:\n\n1. Naïve vs. Rolling ARIMA(1,0,1):\n   DM stat = -1.243, p-value = 0.214\n   -> Statistical equivalence! ARIMA cannot significantly outperform the random walk.\n\n2. Naïve vs. PyTorch GRU:\n   DM stat = -5.001, p-value = 5.7e-7 ***\n   -> Naïve is STATISTICALLY SUPERIOR.\n\n3. Naïve vs. PyTorch LSTM:\n   DM stat = -13.149, p-value < 10^-16 ***\n   -> Naïve is STATISTICALLY SUPERIOR.", False, TEXT_LIGHT),
        ("Multi-Horizon Trajectory (h=281):", True, ACCENT_AMBER),
        ("Naïve vs. Fixed Multi-step ARIMA: DM = -5.627, p = 1.8e-8.", False, TEXT_MUTED)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c9_1):
        p = tf_c9_1.paragraphs[0] if i == 0 else tf_c9_1.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # Card 2: EMH Theory
    create_card(s9, 6.8, 1.4, 5.7, 5.5, "🏛️ The Econometric & Financial Interpretation")
    c9_2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_c9_2 = c9_2.text_frame
    tf_c9_2.word_wrap = True

    bullets_c9_2 = [
        ("Fama's Efficient Market Hypothesis (EMH):", True, ACCENT_AMBER),
        ("• Weak-form EMH states that past price data cannot be used to predict future prices.\n• In crypto, high-frequency returns act as a Martingale difference sequence: E[P_{t+1} | I_t] ≈ P_t.", False, TEXT_LIGHT),
        ("Why Did Deep Learning Lose on Prices?", True, ACCENT_CYAN),
        ("• Zero Parameter Variance: The Naïve model estimates 0 parameters and suffers 0 estimation variance.\n• Noise Overfitting: LSTM/GRU attempt to fit micro-fluctuations, accumulating non-linear prediction variance.\n• Lagged Tracking: Neural networks predict with a slight phase lag behind market turns.", False, TEXT_MUTED),
        ("Major Takeaway:", True, ACCENT_EMERALD),
        ("Honest, transparent reporting: Simple models win on short-term price levels; AI models are best suited for volatility and regime modeling.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c9_2):
        p = tf_c9_2.paragraphs[0] if i == 0 else tf_c9_2.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 10: LLM EXPERIMENTS & AUDIT
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Generative AI Experimentation & Hallucination Audit", "7. GenAI & LLM Audit", "Khalil Ayeb")

    # Card 1: The 4 Experiments
    create_card(s10, 0.8, 1.4, 5.6, 5.5, "🤖 4 Structured Experiments Conducted")
    c10_1 = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf_c10_1 = c10_1.text_frame
    tf_c10_1.word_wrap = True

    bullets_c10_1 = [
        ("Exp 1: Statistical Hypothesis Generation:", True, ACCENT_CYAN),
        ("• Prompted LLM with descriptive moments & stationarity tests.\n• LLM correctly suggested GARCH from excess kurtosis (>18) and differencing for I(1) series.", False, TEXT_LIGHT),
        ("Exp 2: Non-Expert Layman Translation:", True, ACCENT_CYAN),
        ("• Successfully translated Ljung-Box p=0.160 into plain English for executives: 'Residuals are pure white noise; no predictable juice left'.", False, TEXT_MUTED),
        ("Exp 3: Investment Policy Recommendations:", True, ACCENT_CYAN),
        ("• Formulated risk policies under high GARCH volatility.\n• Identified need for position-sizing constraints during crisis clusters.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c10_1):
        p = tf_c10_1.paragraphs[0] if i == 0 else tf_c10_1.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # Card 2: Hallucination Matrix
    create_card(s10, 6.8, 1.4, 5.7, 5.5, "🛡️ Hallucination Audit (Human vs. LLM)")
    c10_2 = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_c10_2 = c10_2.text_frame
    tf_c10_2.word_wrap = True

    bullets_c10_2 = [
        ("Hallucination 1: Causal Misinterpretation", True, ACCENT_AMBER),
        ("• LLM Claim: 'ETH Granger-causes BTC, proving ETH price drives Bitcoin market movements.'\n• Human Correction: Granger causality only measures predictive lag order, NOT physical causation.", False, TEXT_LIGHT),
        ("Hallucination 2: Fabricated Statistical Significance", True, ACCENT_AMBER),
        ("• LLM claimed GJR-GARCH leverage was strongly significant.\n• Human Correction: Real p-value was 0.48 (non-significant).", False, TEXT_MUTED),
        ("Hallucination 3: Blind Deep Learning Bias", True, ACCENT_AMBER),
        ("• LLM assumed LSTM would automatically dominate ARIMA.\n• Human Audit: Real Diebold-Mariano tests proved Random Walk and ARIMA won.", False, TEXT_LIGHT)
    ]
    for i, (txt, bold, col) in enumerate(bullets_c10_2):
        p = tf_c10_2.paragraphs[0] if i == 0 else tf_c10_2.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 11: DEFENSE Q&A SHIELDS
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Defense Strategy: Top 3 Anticipated Questions", "8. Oral Defense", "All Team Members")

    # Q1
    create_card(s11, 0.8, 1.4, 3.6, 5.5, "❓ Q1: Why No VECM?")
    q1_box = s11.shapes.add_textbox(Inches(0.95), Inches(2.0), Inches(3.3), Inches(4.6))
    tf_q1 = q1_box.text_frame
    tf_q1.word_wrap = True
    b_q1 = [
        ("Professor's Question:", True, ACCENT_AMBER),
        ("'Why didn't you estimate a Vector Error Correction Model (VECM)?'", False, TEXT_LIGHT),
        ("Our Defense Answer:", True, ACCENT_EMERALD),
        ("Johansen cointegration tests in Python (Case 2, Trace=25.53 < 29.80) and R (Case 3, Trace=30.27 < 34.91) strictly prove cointegration rank r = 0.\n\nEstimating a VECM requires r >= 1. Estimating a VECM with r = 0 would be a fatal econometric error! We legitimately modeled the system using a stationary VAR(5).", False, TEXT_MUTED)
    ]
    for i, (txt, bold, col) in enumerate(b_q1):
        p = tf_q1.paragraphs[0] if i == 0 else tf_q1.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # Q2
    create_card(s11, 4.8, 1.4, 3.7, 5.5, "❓ Q2: Why Naïve Won?")
    q2_box = s11.shapes.add_textbox(Inches(4.95), Inches(2.0), Inches(3.4), Inches(4.6))
    tf_q2 = q2_box.text_frame
    tf_q2.word_wrap = True
    b_q2 = [
        ("Professor's Question:", True, ACCENT_AMBER),
        ("'Why did the Naïve Random Walk beat your LSTM and GRU?'", False, TEXT_LIGHT),
        ("Our Defense Answer:", True, ACCENT_EMERALD),
        ("Under the Efficient Market Hypothesis (EMH), high-frequency asset returns follow a Martingale difference sequence: E[P_{t+1}|I_t] ≈ P_t.\n\nThe Naïve model has zero parameter estimation error. Deep Learning overfits micro-noise and incurs lag latency.\n\nOur Diebold-Mariano test confirmed Naïve superiority with p < 10^-6.", False, TEXT_MUTED)
    ]
    for i, (txt, bold, col) in enumerate(b_q2):
        p = tf_q2.paragraphs[0] if i == 0 else tf_q2.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # Q3
    create_card(s11, 8.9, 1.4, 3.6, 5.5, "❓ Q3: ARCH vs GARCH?")
    q3_box = s11.shapes.add_textbox(Inches(9.05), Inches(2.0), Inches(3.3), Inches(4.6))
    tf_q3 = q3_box.text_frame
    tf_q3.word_wrap = True
    b_q3 = [
        ("Professor's Question:", True, ACCENT_AMBER),
        ("'Is ARCH a test or a model? What did you actually use?'", False, TEXT_LIGHT),
        ("Our Defense Answer:", True, ACCENT_EMERALD),
        ("Both! ARCH is a model (Engle 1982) and a diagnostic test (ARCH-LM).\n\nWe used the ARCH-LM test on ARIMA residuals (LM=128.4, p < 10^-16) to detect volatility clustering.\n\nThen, we used the upgraded GARCH(1,1) model (Bollerslev 1986) to capture the long-memory decay (persistence = 0.990).", False, TEXT_MUTED)
    ]
    for i, (txt, bold, col) in enumerate(b_q3):
        p = tf_q3.paragraphs[0] if i == 0 else tf_q3.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 12: CONCLUSION & TAKEAWAYS
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, RGBColor(10, 15, 30))
    add_header(s12, "Summary of Methodological Takeaways & Deliverables", "9. Conclusion", "All Team Members")

    # 4 takeaway cards
    card_w = 2.7
    card_h = 4.2
    top_pos = 1.6
    
    pillars = [
        ("1. Diagnostics First", ACCENT_BLUE, "Never evaluate a time-series model by RMSE alone.\n\nRigorous residual diagnostics (Ljung-Box, Jarque-Bera, ARCH-LM) determine whether statistical assumptions hold."),
        ("2. Parsimony & EMH", ACCENT_EMERALD, "Simple models dominate on price levels.\n\nNaïve ($1,725) and Rolling ARIMA ($1,769) beat complex neural networks, validating financial market efficiency."),
        ("3. AI for Volatility", ACCENT_CYAN, "Deep Learning and GARCH provide real value for non-linear volatility, risk estimation, and regime classification rather than direct price guessing."),
        ("4. Human in the Loop", ACCENT_AMBER, "Generative AI is a powerful assistant for coding and drafting, but prone to dangerous statistical hallucinations without human domain expertise.")
    ]

    for i, (ptitle, pcol, pdesc) in enumerate(pillars):
        cpos = 0.8 + i * 2.95
        card = create_card(s12, cpos, top_pos, card_w, card_h, ptitle, pcol)
        tbox = s12.shapes.add_textbox(Inches(cpos + 0.15), Inches(top_pos + 0.6), Inches(card_w - 0.3), Inches(card_h - 0.8))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = pdesc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT
        p.font.name = "Segoe UI"

    # Bottom summary banner
    banner = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.9))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = ACCENT_EMERALD
    banner.line.width = Pt(1.5)
    tf_b = banner.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "All deliverables (Report, Executed Notebook, R Markdown, Python/R Scripts & Data) are fully verified and pushed to GitHub!"
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = TEXT_LIGHT
    p_b.alignment = PP_ALIGN.CENTER

    output_path = "Presentation_MiniProjet_Series_Temporelles_BTC_ETH_BNB.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
