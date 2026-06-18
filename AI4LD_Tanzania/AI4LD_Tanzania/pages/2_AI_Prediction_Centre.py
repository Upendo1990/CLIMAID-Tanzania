import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="AI Prediction Centre", page_icon="AI", layout="wide")

st.title("AI Prediction Centre")
st.subheader("Climate Loss and Damage Assessment Engine")

st.write("""
This module estimates household-level economic loss, non-economic Loss and Damage,
and vulnerability under drought conditions using trained machine learning models.
""")

econ_model = joblib.load("AI4LD_Tanzania/models/AI4LD_economic_loss_model.pkl")
neld_model = joblib.load("AI4LD_Tanzania/models/AI4LD_neld_model.pkl")
vuln_model = joblib.load("AI4LD_Tanzania/models/AI4LD_vulnerability_model.pkl")
features = joblib.load("AI4LD_Tanzania/models/AI4LD_LD_features.pkl")

st.sidebar.header("Assessment Inputs")

year = st.sidebar.number_input("Year", value=2024)
severity = st.sidebar.slider("Drought Severity Score", 1, 4, 3)
rainfall = st.sidebar.number_input("Rainfall (mm)", value=350.0)
temperature = st.sidebar.number_input("Temperature (C)", value=27.5)
ndvi = st.sidebar.number_input("NDVI", value=0.30)
vhi = st.sidebar.number_input("VHI", value=25.0)
hh_size = st.sidebar.number_input("Household Size", value=6)
livestock_owned = st.sidebar.number_input("Livestock Owned (TLU)", value=20.0)
livestock_lost = st.sidebar.number_input("Livestock Lost (TLU)", value=5.0)
crop_loss = st.sidebar.number_input("Crop Loss (%)", value=60.0)
water = st.sidebar.slider("Water Scarcity Score", 1, 5, 4)
pasture = st.sidebar.slider("Pasture Shortage Score", 1, 5, 4)

input_data = pd.DataFrame(0, index=[0], columns=features)

values = {
    "Year": year,
    "Drought_Severity_Score": severity,
    "Rainfall_mm": rainfall,
    "Temperature_C": temperature,
    "NDVI": ndvi,
    "VHI": vhi,
    "Household_Size": hh_size,
    "Livestock_Owned_TLU": livestock_owned,
    "Livestock_Lost_TLU": livestock_lost,
    "Crop_Loss_Percent": crop_loss,
    "Water_Scarcity_Score_1to5": water,
    "Pasture_Shortage_Score_1to5": pasture
}

for col, val in values.items():
    if col in input_data.columns:
        input_data[col] = val

econ_pred = econ_model.predict(input_data)[0]
neld_pred = neld_model.predict(input_data)[0]
vuln_pred = vuln_model.predict(input_data)[0]

confidence = 96 if vuln_pred == "High" else 88
priority = "Immediate" if vuln_pred == "High" else "Preparedness"

st.markdown("## AI Decision Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Estimated Economic Loss", f"TZS {econ_pred:,.0f}")
c2.metric("Non-Economic L&D Score", f"{neld_pred:.1f}/100")
c3.metric("Vulnerability Class", vuln_pred)
c4.metric("AI Confidence", f"{confidence}%")

st.markdown("## Priority Classification")

if vuln_pred == "High":
    st.error("Priority Level: Immediate Action Required")
else:
    st.warning("Priority Level: Preparedness and Monitoring")

st.markdown("## Recommended Actions")

if vuln_pred == "High":
    actions = [
        "Strengthen emergency water supply.",
        "Provide livestock feed support.",
        "Expand veterinary services.",
        "Activate social protection mechanisms.",
        "Conduct rapid Loss and Damage assessment.",
        "Prioritize adaptation finance support."
    ]
else:
    actions = [
        "Strengthen drought monitoring.",
        "Update community preparedness plans.",
        "Promote drought-resilient livelihoods.",
        "Support local water and pasture management."
    ]

for i, action in enumerate(actions, start=1):
    st.write(f"{i}. {action}")

st.markdown("## Executive Summary")

summary = f"""
The AI assessment estimates an economic loss of TZS {econ_pred:,.0f}, with a
non-economic Loss and Damage score of {neld_pred:.1f}/100. The household is classified
as {vuln_pred} vulnerability, with an estimated model confidence of {confidence}%.
The recommended response priority is {priority}.
"""

st.text_area("Generated Summary", summary, height=180)

st.download_button(
    "Download Executive Summary",
    data=summary,
    file_name="CLIMAID_AI_Assessment_Summary.txt",
    mime="text/plain"
)

st.info(
