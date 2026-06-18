import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="CLIMAID",
    page_icon="CL",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = "AI4LD_Tanzania/data/AI4LD_Simanjiro_396HH_Simulated_LossDamage_Dataset.xlsx"
MODEL_DIR = "AI4LD_Tanzania/models"

households = pd.read_excel(DATA_PATH)
household_count = len(households)
model_count = len([f for f in os.listdir(MODEL_DIR) if f.endswith(".pkl")])

st.markdown("""
<style>
.stApp {background-color:#F4F6F8;}
section[data-testid="stSidebar"] {background-color:#0B1F33;}
section[data-testid="stSidebar"] * {color:white;}
.hero {
    background: linear-gradient(135deg,#0B4F6C,#1565C0);
    padding:50px;
    border-radius:18px;
    color:white;
    margin-bottom:30px;
}
.hero-title {font-size:52px;font-weight:800;}
.hero-subtitle {font-size:25px;font-weight:600;margin-top:10px;}
.hero-text {font-size:17px;line-height:1.7;margin-top:15px;max-width:1100px;}
.card {
    background:white;
    padding:28px;
    border-radius:14px;
    box-shadow:0px 4px 14px rgba(0,0,0,0.08);
    border:1px solid #E0E0E0;
}
.card-value {font-size:34px;font-weight:800;color:#0B4F6C;}
.card-label {font-size:14px;color:#546E7A;text-transform:uppercase;font-weight:600;}
.section-title {font-size:28px;font-weight:800;color:#0B4F6C;margin-top:30px;}
.module-card {
    background:white;
    padding:25px;
    border-radius:14px;
    min-height:175px;
    box-shadow:0px 4px 14px rgba(0,0,0,0.06);
    border:1px solid #E0E0E0;
}
.footer {text-align:center;color:#607D8B;font-size:13px;padding:30px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## CLIMAID")
st.sidebar.markdown("Climate Intelligence for Adaptation and Loss & Damage")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
st.sidebar.markdown("""
Executive Dashboard  
National Climate Dashboard  
AI Prediction Centre  
Analytics and Explainability  
Report Generator  
Adaptation Planner  
Early Warning Centre  
Climate Finance Dashboard  
About CLIMAID
""")
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.markdown("AI models: Ready")
st.sidebar.markdown("Data: Loaded")
st.sidebar.markdown("Mode: Prototype")

st.markdown("""
<div class="hero">
    <div class="hero-title">CLIMAID</div>
    <div class="hero-subtitle">Climate Intelligence for Adaptation and Loss & Damage</div>
    <div class="hero-text">
        An AI-powered decision support platform integrating climate data, Earth observation,
        GIS, machine learning, and household vulnerability information to support climate
        adaptation planning and Loss and Damage assessment.
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="card"><div class="card-value">170</div><div class="card-label">Districts Mapped</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="card"><div class="card-value">{household_count}</div><div class="card-label">Household Records</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><div class="card-value">24</div><div class="card-label">Years Climate Data</div></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="card"><div class="card-value">{model_count}</div><div class="card-label">AI Model Files</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Platform Overview</div>', unsafe_allow_html=True)

st.write("""
CLIMAID supports decision-makers by translating climate stress, vulnerability, and household-level
Loss and Damage information into practical intelligence. The current MVP demonstrates national
risk mapping, AI-based Loss and Damage prediction, analytics, reporting, adaptation planning,
early warning, and climate finance prioritization.
""")


st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="module-card">
    <h3>Climate Risk Mapping</h3>
    <p>Interactive Tanzania district map for visualizing climate risk and vulnerability layers.</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="module-card">
    <h3>AI Loss and Damage Prediction</h3>
    <p>Machine learning models estimate economic loss, non-economic loss, and vulnerability.</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="module-card">
    <h3>Decision Support</h3>
    <p>Adaptation planning, early warning, reporting, and climate finance prioritization.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Current MVP Modules</div>', unsafe_allow_html=True)

st.write("""
1. National Climate Dashboard  
2. AI Prediction Centre  
3. Analytics and Explainability  
4. Report Generator  
5. Adaptation Planner  
6. Early Warning Centre  
7. Climate Finance Dashboard  
8. About CLIMAID  
""")

st.markdown("---")
st.markdown(f"""
<div class="footer">
CLIMAID Version 1.0 MVP<br>
Climate Intelligence for Adaptation and Loss & Damage<br>
Prototype Version • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
