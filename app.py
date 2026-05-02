import streamlit as st 
import numpy as np
import plotly.graph_objects as go

# 1. Sayfa Ayarları (Karanlık tema ve geniş düzen)
st.set_page_config(page_title="Çifte Yarık Simülasyonu", layout="wide")

# 2. CSS ile Stil Verme (Font ve renkler)
st.markdown("""
  <style>
  .stApp { backround-color: #0e1117; color: white; }
  </style>
  """, unsafe_allow_html=True)

# 3. Kenar Çubuğu (Parametreler)
st.sidebar.header("Deney Parametreleri")
lambda_nm = st.sidebar.slider("Dalga Boyu (nm)", 400, 700, 550)
d_mm = st.sidebar.slider("Yarık Aralığı (mm)", 0.1, 1.0, 0.5)
L_m = st.sidebar.slider("Ekran Mesafesi (m)", 1.0, 5.0, 2.0)

# 4. Hesaplama
x = np.linspace(-0.02, 0.02, 1000)
L_lambda = (lambda_nm * 1e-9) * L_m
intensity = np.cos((np.pi * (d_mm * 1e-3) * x) / L_lambda)**2

# 5. Grafik
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=intensity, line=dict(color='#00fbbf')))
fig.update_layout(template="plotly_dark", height=600)
st.plotly_chart(fig, use_container_width=True)
