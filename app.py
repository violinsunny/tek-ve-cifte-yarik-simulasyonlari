import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Site Ayarları
st.set_page_config(page_title="Tek ve Çifte Yarık Simülasyonları", layout="wide")

# 2. Arayüz (CSS) - Bloch Küresi stilinde karanlık ve neon yeşil tema
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        font-family: 'Courier New', monospace;
    }
    h1, h2, h3 { 
        color: #00FF00 !important; 
        text-shadow: 0 0 10px #00FF00;
        font-weight: bold;
    }
    p, span, label { 
        color: #00FF00 !important; 
    }
    /* Slider Renkleri */
    .stSlider [data-baseweb="slider"] {
        background-color: #003300;
    }
    /* Bilgi Kutuları */
    .info-box {
        border: 2px solid #00FF00;
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(0, 255, 0, 0.05);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    hr {
        border: 0.5px solid #00FF00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>[ OPTİK GİRİŞİM SİMÜLASYONU ]</h1>", unsafe_allow_html=True)

# 3. Parametreler (Yan Menü yerine üstte daha geniş kontrol paneli)
with st.container():
    st.markdown("### [ SİSTEM PARAMETRELERİ ]")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        lam_nm = st.slider("[WAVELENGTH_λ] (nm)", 400, 700, 532)
        d_um = st.slider("[SLIT_DISTANCE_d] (µm)", 20, 200, 100)
    with col_p2:
        a_um = st.slider("[SLIT_WIDTH_a] (µm)", 5, 50, 20)
        L_m = st.slider("[SCREEN_DISTANCE_L] (m)", 0.5, 3.0, 1.5)

# 4. Genel Hesaplamalar
x = np.linspace(-0.04, 0.04, 1200)
lam = lam_nm * 1e-9
d = d_um * 1e-6
a = a_um * 1e-6
L = L_m
theta = np.arctan(x / L)
beta = (np.pi * a * np.sin(theta)) / lam
alpha = (np.pi * d * np.sin(theta)) / lam

# Sabit Neon Yeşil Rengi
SABIT_RENK = '#00FF00' 

# --- ÇİFTE YARIK BÖLÜMÜ ---
st.markdown("---")
st.markdown("## 1) ÇİFTE YARIK DENEYİ")
intensity_double = (np.cos(alpha)**2) * (np.sinc(beta/np.pi)**2)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### [ YOĞUNLUK DAĞILIMI ]")
    fig_double = go.Figure()
    fig_double.add_trace(go.Scatter(
        x=x*100, y=intensity_double, 
        line=dict(color=SABIT_RENK, width=2), 
        fill='tozeroy', 
        fillcolor='rgba(0, 255, 0, 0.2)'
    ))
    fig_double.update_layout(
        template="plotly_dark", 
        paper_bgcolor='black', 
        plot_bgcolor='black', 
        xaxis=dict(title="Ekran (cm)", gridcolor='#003300'), 
        yaxis=dict(title="Yoğunluk", gridcolor='#003300'), 
        height=350
    )
    st.plotly_chart(fig_double, use_container_width=True)

with col2:
    st.markdown("### [ PROJEKSİYON ]")
    pattern_double = np.tile(intensity_double, (100, 1))
    fig_map_double = go.Figure(data=go.Heatmap(
        z=pattern_double, x=x*100, 
        colorscale=[[0, '#000000'], [1, SABIT_RENK]], 
        showscale=False
    ))
    fig_map_double.update_layout(
        template="plotly_dark", 
        paper_bgcolor='black', 
        plot_bgcolor='black', 
        xaxis=dict(title="Ekran (cm)"), 
        yaxis=dict(visible=False), 
        height=350
    )
    st.plotly_chart(fig_map_double, use_container_width=True)

st.markdown(f"""<div class="info-box">
<p style="margin:0;">[VERİ ANALİZİ]:</p>
<h3 style="margin:0;">Saçak Aralığı (Δx): {round((lam * L / d) * 1000, 3)} mm</h3>
</div>""", unsafe_allow_html=True)


# --- TEK YARIK BÖLÜMÜ ---
st.markdown("---")
st.markdown("## 2) TEK YARIK DENEYİ")
intensity_single = (np.sinc(beta/np.pi)**2) 

col3, col4 = st.columns(2)
with col3:
    st.markdown("### [ YOĞUNLUK DAĞILIMI ]")
    fig_single = go.Figure()
    fig_single.add_trace(go.Scatter(
        x=x*100, y=intensity_single, 
        line=dict(color=SABIT_RENK, width=2), 
        fill='tozeroy', 
        fillcolor='rgba(0, 255, 0, 0.2)'
    ))
    fig_single.update_layout(
        template="plotly_dark", 
        paper_bgcolor='black', 
        plot_bgcolor='black', 
        xaxis=dict(title="Ekran (cm)", gridcolor='#003300'), 
        yaxis=dict(title="Yoğunluk", gridcolor='#003300'), 
        height=350
    )
    st.plotly_chart(fig_single, use_container_width=True)

with col4:
    st.markdown("### [ PROJEKSİYON ]")
    pattern_single = np.tile(intensity_single, (100, 1))
    fig_map_single = go.Figure(data=go.Heatmap(
        z=pattern_single, x=x*100, 
        colorscale=[[0, '#000000'], [1, SABIT_RENK]], 
        showscale=False
    ))
    fig_map_single.update_layout(
        template="plotly_dark", 
        paper_bgcolor='black', 
        plot_bgcolor='black', 
        xaxis=dict(title="Ekran (cm)"), 
        yaxis=dict(visible=False), 
        height=350
    )
    st.plotly_chart(fig_map_single, use_container_width=True)

st.markdown(f"""<div class="info-box">
<p style="margin:0;">[VERİ ANALİZİ]:</p>
<h3 style="margin:0;">Merkezi Aydınlık Saçak Genişliği: {round((2 * lam * L / a) * 1000, 3)} mm</h3>
</div>""", unsafe_allow_html=True)

st.write("---")
st.markdown(" GÖZLEMCİ NOTU: Dalga boyu ($\lambda$) arttıkça kırınım desenindeki saçak genişliği artar.")
