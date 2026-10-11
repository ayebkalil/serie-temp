import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def update_presentation():
    pptx_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\Presentation_TimeSeries_BTC_ETH_BNB_TEKUP2026.pptx"
    orig_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\Presentation_TimeSeries_BTC_ETH_BNB_TEKUP2026_orig.pptx"
    
    if not os.path.exists(orig_path):
        import shutil
        shutil.copyfile(pptx_path, orig_path)
        
    prs = Presentation(orig_path)
    
    # Theme colors matching template
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    TEXT_DARK = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139)
    ACCENT_BLUE = RGBColor(37, 99, 235)
    ACCENT_CYAN = RGBColor(14, 165, 233)
    ACCENT_AMBER = RGBColor(245, 158, 11)
    ACCENT_EMERALD = RGBColor(16, 185, 129)

    print("Loaded original presentation with", len(prs.slides), "slides.")

    # ----------------------------------------------------
    # 1. UPDATE SLIDE 5: Fix Speaker to Amine Benfadhel
    # ----------------------------------------------------
    slide_var = prs.slides[4] # Slide 5: VAR, Granger and Johansen
    for s in slide_var.shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                if "Khawla Hawari" in p.text:
                    p.text = "Presented by Amine Benfadhel"
                    print("Updated Slide 5 speaker to Amine Benfadhel.")

    # ----------------------------------------------------
    # 2. UPDATE SLIDE 6: Replace unannotated chart with Fig 4 (Covid, China, FTX Crashes)
    # ----------------------------------------------------
    slide_garch = prs.slides[5] # Slide 6: GARCH
    # Find Shape 5 (Chart) and remove it
    chart_shape = None
    for s in slide_garch.shapes:
        if s.has_chart:
            chart_shape = s
            break
            
    if chart_shape:
        sp_elem = chart_shape._element
        sp_elem.getparent().remove(sp_elem)
        print("Removed unannotated line chart from Slide 6.")
        
    # Add Figure 4 (GARCH Volatility with labeled crash events)
    fig4_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\plots\fig4_garch_volatility_events.png"
    if os.path.exists(fig4_path):
        slide_garch.shapes.add_picture(
            fig4_path,
            Inches(0.60), Inches(2.00),
            width=Inches(7.60), height=Inches(4.75)
        )
        print("Added fig4_garch_volatility_events.png with Covid, China, and FTX crash labels to Slide 6.")

    # ----------------------------------------------------
    # Helper to create a card shape
    # ----------------------------------------------------
    def add_card(slide, left, top, width, height, title="", title_color=ACCENT_BLUE):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)
        
        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # Helper to add standard footer (speaker + number)
    def add_footer(slide, speaker_text, slide_num):
        tb_spk = slide.shapes.add_textbox(Inches(6.40), Inches(7.02), Inches(5.60), Inches(0.28))
        tf_spk = tb_spk.text_frame
        p_spk = tf_spk.paragraphs[0]
        p_spk.text = speaker_text
        p_spk.font.size = Pt(11)
        p_spk.font.color.rgb = TEXT_MUTED

        tb_num = slide.shapes.add_textbox(Inches(12.20), Inches(7.02), Inches(0.50), Inches(0.28))
        tf_num = tb_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = str(slide_num)
        p_num.font.size = Pt(11)
        p_num.font.color.rgb = TEXT_MUTED

    # ----------------------------------------------------
    # 3. CREATE NEW SLIDE A: STL Decomposition & Correlograms
    # ----------------------------------------------------
    layout_light = prs.slide_layouts[1]
    slide_stl = prs.slides.add_slide(layout_light)
    slide_stl.placeholders[100].text = "EXPLORATORY ANALYSIS"
    slide_stl.placeholders[101].text = "STL Decomposition and Autocorrelation Structure"
    slide_stl.placeholders[102].text = "Visual proof of stochastic trend dominance (>99%), absence of seasonality, and return memory cutoff"

    # Embed Fig 3 (STL Decomposition)
    fig3_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\plots\fig3_stl_decomposition.png"
    if os.path.exists(fig3_path):
        slide_stl.shapes.add_picture(
            fig3_path,
            Inches(0.60), Inches(2.00),
            width=Inches(6.00), height=Inches(4.75)
        )

    # Embed Fig 2 (ACF & PACF)
    fig2_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\plots\fig2_acf_pacf.png"
    if os.path.exists(fig2_path):
        slide_stl.shapes.add_picture(
            fig2_path,
            Inches(6.80), Inches(2.00),
            width=Inches(5.90), height=Inches(4.75)
        )

    add_footer(slide_stl, "Presented by Khawla Hawari", 4)
    print("Created Slide A: STL Decomposition & ACF/PACF.")

    # ----------------------------------------------------
    # 4. CREATE NEW SLIDE B: Dynamic Contagion (60-Day Rolling Correlation)
    # ----------------------------------------------------
    slide_dcc = prs.slides.add_slide(layout_light)
    slide_dcc.placeholders[100].text = "MULTIVARIATE SYSTEM"
    slide_dcc.placeholders[101].text = "Dynamic Market Contagion: 60-Day Rolling Correlations"
    slide_dcc.placeholders[102].text = "Empirical evidence of correlation spikes during systemic panics vs. altcoin decoupling"

    # Embed Fig 7 (Dynamic correlation)
    fig7_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\plots\fig7_dynamic_correlation.png"
    if os.path.exists(fig7_path):
        slide_dcc.shapes.add_picture(
            fig7_path,
            Inches(0.60), Inches(2.00),
            width=Inches(7.50), height=Inches(4.75)
        )

    # Add explanatory cards on the right
    add_card(slide_dcc, 8.35, 2.00, 4.35, 1.45, "🚨 Crisis Contagion (0.90 - 0.95)", ACCENT_AMBER)
    tb_c1 = slide_dcc.shapes.add_textbox(Inches(8.55), Inches(2.50), Inches(3.95), Inches(0.85))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p1 = tf_c1.paragraphs[0]
    p1.text = "Correlation surges to near-unity during severe liquidations (Covid March 2020 & FTX Nov 2022), reflecting cross-market panic contagion."
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = TEXT_DARK

    add_card(slide_dcc, 8.35, 3.65, 4.35, 1.45, "🔄 Altcoin Decoupling (0.40 - 0.60)", ACCENT_CYAN)
    tb_c2 = slide_dcc.shapes.add_textbox(Inches(8.55), Inches(4.15), Inches(3.95), Inches(0.85))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p2 = tf_c2.paragraphs[0]
    p2.text = "Calm market conditions and 'alt-seasons' see correlation drop, allowing ETH and BNB to trade on separate smart-contract/exchange dynamics."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_DARK

    add_card(slide_dcc, 8.35, 5.30, 4.35, 1.45, "⚖️ Correlation ≠ Cointegration", ACCENT_EMERALD)
    tb_c3 = slide_dcc.shapes.add_textbox(Inches(8.55), Inches(5.80), Inches(3.95), Inches(0.85))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p3 = tf_c3.paragraphs[0]
    p3.text = "High daily co-movement (0.83) does NOT imply a permanent long-run anchor. Johansen test confirms r = 0; no statistical arbitrage leash."
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_DARK

    add_footer(slide_dcc, "Presented by Amine Benfadhel", 7)
    print("Created Slide B: Dynamic Contagion (60-day rolling correlation).")

    # ----------------------------------------------------
    # 5. CREATE NEW SLIDE C: Deep Learning Loss Curves (LSTM vs GRU)
    # ----------------------------------------------------
    slide_dl = prs.slides.add_slide(layout_light)
    slide_dl.placeholders[100].text = "DEEP LEARNING"
    slide_dl.placeholders[101].text = "Deep Learning Loss Curves: LSTM vs. GRU"
    slide_dl.placeholders[102].text = "Comparing training dynamics, convergence velocity, and parameter parsimony over 40 epochs"

    # Embed Fig 5 (Loss curves)
    fig5_path = r"C:\Users\ayebk\OneDrive\Desktop\serie temp\plots\fig5_loss_curves_lstm_gru.png"
    if os.path.exists(fig5_path):
        slide_dl.shapes.add_picture(
            fig5_path,
            Inches(0.60), Inches(2.00),
            width=Inches(7.50), height=Inches(4.75)
        )

    # Add explanatory cards on the right
    add_card(slide_dl, 8.35, 2.00, 4.35, 1.45, "⚡ Parameter Efficiency", ACCENT_CYAN)
    tb_dl1 = slide_dl.shapes.add_textbox(Inches(8.55), Inches(2.50), Inches(3.95), Inches(0.85))
    tf_dl1 = tb_dl1.text_frame
    tf_dl1.word_wrap = True
    p_dl1 = tf_dl1.paragraphs[0]
    p_dl1.text = "GRU utilizes 19,073 parameters (24% fewer than LSTM's 25,217), enabling faster training and lower risk of parameter bloat on financial series."
    p_dl1.font.size = Pt(10.5)
    p_dl1.font.color.rgb = TEXT_DARK

    add_card(slide_dl, 8.35, 3.65, 4.35, 1.45, "📉 Convergence Velocity", ACCENT_EMERALD)
    tb_dl2 = slide_dl.shapes.add_textbox(Inches(8.55), Inches(4.15), Inches(3.95), Inches(0.85))
    tf_dl2 = tb_dl2.text_frame
    tf_dl2.word_wrap = True
    p_dl2 = tf_dl2.paragraphs[0]
    p_dl2.text = "GRU achieves a lower validation MSE (0.00041 vs 0.00062) and stabilizes earlier (epoch 38 vs 45) under identical Adam (lr = 0.002) optimization."
    p_dl2.font.size = Pt(10.5)
    p_dl2.font.color.rgb = TEXT_DARK

    add_card(slide_dl, 8.35, 5.30, 4.35, 1.45, "🛡️ Generalization & Dropout", ACCENT_AMBER)
    tb_dl3 = slide_dl.shapes.add_textbox(Inches(8.55), Inches(5.80), Inches(3.95), Inches(0.85))
    tf_dl3 = tb_dl3.text_frame
    tf_dl3.word_wrap = True
    p_dl3 = tf_dl3.paragraphs[0]
    p_dl3.text = "Train and validation losses converge tightly with zero evidence of severe overfitting, thanks to 0.20 dropout and strict chronological windowing."
    p_dl3.font.size = Pt(10.5)
    p_dl3.font.color.rgb = TEXT_DARK

    add_footer(slide_dl, "Presented by Amine Benfadhel", 10)
    print("Created Slide C: Deep Learning Loss Curves.")

    # ----------------------------------------------------
    # REORDER SLIDES TO LOGICAL 13-SLIDE FLOW
    # ----------------------------------------------------
    # Original order:
    # 0: Title (1)
    # 1: Data & Design (2)
    # 2: EDA & Stationarity (3)
    # 3: ARIMA & Diagnostics (4)
    # 4: VAR, Granger, Johansen (5)
    # 5: GARCH Volatility (6 - now with Fig 4 crash labels)
    # 6: DL Architectures (7)
    # 7: Out-of-sample Forecast (8)
    # 8: GenAI Audit (9)
    # 9: Conclusion (10)
    # 10: NEW Slide A (STL & Correlograms) -> should go after slide 2 (index 3)
    # 11: NEW Slide B (Dynamic Contagion) -> should go after VAR/Johansen (index 6)
    # 12: NEW Slide C (DL Loss Curves) -> should go after DL Arch (index 9)

    slide_ids = prs.slides._sldIdLst
    # Current elements in list
    s_a = slide_ids[10] # Slide A
    s_b = slide_ids[11] # Slide B
    s_c = slide_ids[12] # Slide C

    # Remove the 3 newly appended from the end
    slide_ids.remove(s_a)
    slide_ids.remove(s_b)
    slide_ids.remove(s_c)

    # Insert s_a at position 3 (after Slide 3 EDA)
    slide_ids.insert(3, s_a)

    # Insert s_b at position 6 (after Slide 5 VAR/Johansen, which became index 5)
    slide_ids.insert(6, s_b)

    # Insert s_c at position 9 (after DL Arch, which became index 8)
    slide_ids.insert(9, s_c)

    # Renumber slide footers
    for idx, slide in enumerate(prs.slides):
        for s in slide.shapes:
            if s.has_text_frame:
                for p in s.text_frame.paragraphs:
                    # If single number matching slide number placeholder
                    if p.text.strip().isdigit() and len(p.text.strip()) <= 2:
                        p.text = str(idx + 1)

    prs.save(pptx_path)
    print("Successfully saved updated presentation to:", pptx_path)
    print(f"Total slides in updated presentation: {len(prs.slides)}")

if __name__ == "__main__":
    update_presentation()
