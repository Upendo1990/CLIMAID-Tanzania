
import streamlit as st

st.set_page_config(page_title="Early Warning Centre", page_icon="", layout="wide")

st.title(" Early Warning Centre")
st.subheader("Prototype traffic-light climate risk alert system")

district = st.text_input("District", "Simanjiro")
vhi = st.slider("Vegetation Health Index (VHI)", 0, 100, 28)
rainfall_anomaly = st.slider("Rainfall Anomaly (%)", -100, 100, -35)

if vhi < 20 or rainfall_anomaly < -50:
    level = "Extreme"
    st.error(" EXTREME ALERT: Immediate response required.")
elif vhi < 30 or rainfall_anomaly < -30:
    level = "High"
    st.error(" HIGH ALERT: Drought response should be activated.")
elif vhi < 40 or rainfall_anomaly < -15:
    level = "Moderate"
    st.warning(" MODERATE ALERT: Strengthen monitoring and preparedness.")
else:
    level = "Low"
    st.success(" LOW ALERT: Continue routine monitoring.")

st.markdown("## Alert Summary")
st.write(f"District: **{district}**")
st.write(f"Risk Level: **{level}**")

st.markdown("## Recommended Early Actions")
if level in ["Extreme", "High"]:
    st.write("- Activate district drought response team.")
    st.write("- Disseminate early warning messages.")
    st.write("- Prepare water and livestock support.")
    st.write("- Conduct rapid Loss and Damage screening.")
else:
    st.write("- Continue monitoring rainfall, VHI and water availability.")
    st.write("- Update community preparedness plans.")
