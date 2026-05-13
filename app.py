import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Sayfa Ayarları
st.set_page_config(page_title="Yarık Deneyleri Simülasyonu", layout="centered")

# 2. Arayüz Tasarımı
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
    }
    /* Slider ve Genel Metin Renkleri */
    div[data-testid="stMarkdownContainer"] { 
        color: #00FF00; 
        font-family: 'Courier New', monospace; 
    }
    /* Başlıklar */
    h1, h2, h3 { 
        color: #00FF00 !important; 
        text-shadow: 0 0 10px #00FF00;
        font-family: 'Courier New', monospace;
    }
    /* Slider Stili */
    .stSlider > div [data-baseweb="slider"] {
        background-color: #00FF00;
    }
    /* Kart Yapıları */
    .metric-box {
        border: 2px solid #00FF00; 
        padding: 15px; 
        border-radius: 10px;
        background-color: rgba(0, 255, 0, 0.05);
        font-family: 'Courier New', monospace;
        margin-bottom: 20px;
    }
    hr {
        border: 0.5px solid #00FF00;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>[ Yarık Deneyleri Simülasyonu ]</h1>", unsafe_allow_html=True)

# 3. Kontrol Paneli (Siber Sliderlar)
st.markdown("### [ PARAMETRE_GİRİŞİ ]")
col_p1, col_p2 = st.columns(2)
with col_p1:
    lam_nm = st.slider("DALGA_BOYU (nm)", 400, 700, 532)
    d_um = st.slider("YARIK_ARALIĞI (µm)", 20, 200, 100)
with col_p2:
    a_um = st.slider("YARIK_GENİŞLİĞİ (µm)", 5, 50, 20)
    L_m = st.slider("EKRAN_MESAFESİ (m)", 0.5, 3.0, 1.5)

# 4. Matematiksel Hesaplamalar
x = np.linspace(-0.04, 0.04, 1000)
lam = lam_nm * 1e-9
d = d_um * 1e-6
a = a_um * 1e-6
L = L_m
theta = np.arctan(x / L)
beta = (np.pi * a * np.sin(theta)) / lam
alpha = (np.pi * d * np.sin(theta)) / lam

# Renk Sabiti
NEON_GREEN = '#00FF00'

# Çifte Yarık Deneyi
st.write("---")
st.markdown("## 01_ÇİFTE_YARIK_ANALİZİ")

intensity_double = (np.cos(alpha)**2) * (np.sinc(beta/np.pi)**2)

# Grafik Tasarımı
fig_double = go.Figure()
fig_double.add_trace(go.Scatter(x=x*100, y=intensity_double, line=dict(color=NEON_GREEN, width=2), fill='tozeroy'))
fig_double.update_layout(
    template="plotly_dark", 
    paper_bgcolor='black', 
    plot_bgcolor='black',
    xaxis=dict(title="MESAFE (cm)", gridcolor='#113311', color=NEON_GREEN),
    yaxis=dict(title="YOĞUNLUK", gridcolor='#113311', color=NEON_GREEN),
    height=300,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_double, use_container_width=True)

# Projeksiyon
pattern_double = np.tile(intensity_double, (50, 1))
fig_map_double = go.Figure(data=go.Heatmap(z=pattern_double, x=x*100, colorscale=[[0, 'black'], [1, NEON_GREEN]], showscale=False))
fig_map_double.update_layout(template="plotly_dark", paper_bgcolor='black', plot_bgcolor='black', height=150, margin=dict(l=20, r=20, t=10, b=10), yaxis=dict(visible=False))
st.plotly_chart(fig_map_double, use_container_width=True)

st.markdown(f"""
<div class="metric-box">
    <p><b>[DATA_OUTPUT]:</b> Saçak Aralığı (Δx): {round((lam * L / d) * 1000, 3)} mm</p>
</div>
""", unsafe_allow_html=True)


# Tek yarık Deneyi
st.write("---")
st.markdown("## 02_TEK_YARIK_ANALİZİ")

intensity_single = (np.sinc(beta/np.pi)**2)

fig_single = go.Figure()
fig_single.add_trace(go.Scatter(x=x*100, y=intensity_single, line=dict(color=NEON_GREEN, width=2), fill='tozeroy'))
fig_single.update_layout(
    template="plotly_dark", 
    paper_bgcolor='black', 
    plot_bgcolor='black',
    xaxis=dict(title="MESAFE (cm)", gridcolor='#113311', color=NEON_GREEN),
    yaxis=dict(title="YOĞUNLUK", gridcolor='#113311', color=NEON_GREEN),
    height=300,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_single, use_container_width=True)

# Projeksiyon
pattern_single = np.tile(intensity_single, (50, 1))
fig_map_single = go.Figure(data=go.Heatmap(z=pattern_single, x=x*100, colorscale=[[0, 'black'], [1, NEON_GREEN]], showscale=False))
fig_map_single.update_layout(template="plotly_dark", paper_bgcolor='black', plot_bgcolor='black', height=150, margin=dict(l=20, r=20, t=10, b=10), yaxis=dict(visible=False))
st.plotly_chart(fig_map_single, use_container_width=True)

st.markdown(f"""
<div class="metric-box">
    <p><b>[DATA_OUTPUT]:</b> Merkezi Aydınlık Saçak Genişliği: {round((2 * lam * L / a) * 1000, 3)} mm</p>
</div>
""", unsafe_allow_html=True)

st.write("---")
st.markdown("GÖZLEMCİ NOTU: Yarık genişliği (a) azaldığında, kırınım deseni ekranda daha geniş bir alana yayılır.")
