
import streamlit as st

st.set_page_config(page_title="Adaptation Planner", page_icon="", layout="wide")

st.title(" Adaptation Planner")
st.subheader("AI-informed adaptation and Loss & Damage response planning")

risk = st.selectbox("Select Risk Level", ["Low", "Moderate", "High", "Very High"])
sector = st.selectbox("Select Sector", ["Water", "Livestock", "Agriculture", "Health", "Social Protection", "Infrastructure"])

recommendations = {
    "Water": ["Rehabilitate boreholes", "Expand water harvesting", "Emergency water trucking", "Protect water catchments"],
    "Livestock": ["Livestock feed banks", "Veterinary support", "Pasture restoration", "Mobility planning"],
    "Agriculture": ["Drought-tolerant crops", "Climate-smart extension", "Planting calendar advisories", "Small-scale irrigation"],
    "Health": ["Heat-health alerts", "Mobile health outreach", "Water-borne disease surveillance", "Community awareness"],
    "Social Protection": ["Cash transfers", "Livelihood grants", "Targeted food support", "Shock-responsive safety nets"],
    "Infrastructure": ["Climate-resilient roads", "Water storage systems", "Flood-safe public facilities", "Early warning infrastructure"]
}

st.markdown("## Recommended Actions")

for action in recommendations[sector]:
    if risk in ["High", "Very High"]:
        st.error(f" Priority Action: {action}")
    elif risk == "Moderate":
        st.warning(f" Recommended: {action}")
    else:
        st.success(f" Preparedness: {action}")

st.info("This module will later connect automatically to district drought risk, AI vulnerability prediction, and estimated Loss & Damage.")
