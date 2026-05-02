import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Site İsmi
st.set_page_config(page_title="Tek ve Çifte Yarık Simülasyonları", layout="wide")

# 2. Yazı Stili
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 { color: #f0f6fc; font-weight: 300; }
    p { color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# Başlık
st.title("Tek ve Çifte Yarık Simülasyonları")

# 3. Parametreler
with st.sidebar:
    st.header("Parametreler")
    lam_nm = st.slider("Dalga Boyu (nm)", 400, 700, 532)
    d_um = st.slider("Yarık Aralığı (µm)", 20, 200, 100)
    a_um = st.slider("Yarık Genişliği (µm)", 5, 50, 20)
    L_m = st.slider("Ekran Mesafesi (m)", 0.5, 3.0, 1.5)

# 4. Genel Hesaplamalar
x = np.linspace(-0.04, 0.04, 1200)
lam = lam_nm * 1e-9
d = d_um * 1e-6
a = a_um * 1e-6
L = L_m
theta = np.arctan(x / L)
beta = (np.pi * a * np.sin(theta)) / lam
alpha = (np.pi * d * np.sin(theta)) / lam

# Sabit Tema Rengi
SABIT_RENK = '#00f2fe' 

# Çifte Yarık Deneyi
st.header("1) Çifte Yarık Deneyi")
intensity_double = (np.cos(alpha)**2) * (np.sinc(beta/np.pi)**2)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Yoğunluk Dağılımı")
    fig_double = go.Figure()
    fig_double.add_trace(go.Scatter(x=x*100, y=intensity_double, line=dict(color=SABIT_RENK, width=2), fill='tozeroy', fillcolor='rgba(0, 242, 254, 0.1)'))
    fig_double.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title="Ekran (cm)", gridcolor='#30363d'), yaxis=dict(title="Yoğunluk", gridcolor='#30363d'), height=350)
    st.plotly_chart(fig_double, use_container_width=True)

with col2:
    st.subheader("Projeksiyon")
    pattern_double = np.tile(intensity_double, (100, 1))
    fig_map_double = go.Figure(data=go.Heatmap(z=pattern_double, x=x*100, colorscale=[[0, '#0e1117'], [1, SABIT_RENK]], showscale=False))
    fig_map_double.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title="Ekran (cm)"), yaxis=dict(visible=False), height=350)
    st.plotly_chart(fig_map_double, use_container_width=True)

st.markdown(f"""<div style="background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 40px;">
<p style="margin:0; color: {SABIT_RENK};">Çifte Yarık Analizi:</p><h3 style="margin:0;">Saçak Aralığı (Δx): {round((lam * L / d) * 1000, 3)} mm</h3></div>""", unsafe_allow_html=True)

# Tek Yarık Deneyi
st.header("2) Tek Yarık Deneyi")
intensity_single = (np.sinc(beta/np.pi)**2) 

col3, col4 = st.columns(2)
with col3:
    st.subheader("Yoğunluk Dağılımı")
    fig_single = go.Figure()
    fig_single.add_trace(go.Scatter(x=x*100, y=intensity_single, line=dict(color=SABIT_RENK, width=2), fill='tozeroy', fillcolor='rgba(0, 242, 254, 0.1)'))
    fig_single.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title="Ekran (cm)", gridcolor='#30363d'), yaxis=dict(title="Yoğunluk", gridcolor='#30363d'), height=350)
    st.plotly_chart(fig_single, use_container_width=True)

with col4:
    st.subheader("Projeksiyon")
    pattern_single = np.tile(intensity_single, (100, 1))
    fig_map_single = go.Figure(data=go.Heatmap(z=pattern_single, x=x*100, colorscale=[[0, '#0e1117'], [1, SABIT_RENK]], showscale=False))
    fig_map_single.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title="Ekran (cm)"), yaxis=dict(visible=False), height=350)
    st.plotly_chart(fig_map_single, use_container_width=True)

st.markdown(f"""<div style="background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d;">
<p style="margin:0; color: {SABIT_RENK};">Tek Yarık Analizi:</p><h3 style="margin:0;">Merkezi Aydınlık Saçak Genişliği: {round((2 * lam * L / a) * 1000, 3)} mm</h3></div>""", unsafe_allow_html=True)
