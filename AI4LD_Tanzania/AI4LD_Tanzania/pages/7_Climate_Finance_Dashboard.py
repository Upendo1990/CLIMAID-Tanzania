
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Climate Finance Dashboard", page_icon="", layout="wide")

st.title(" Climate Finance Dashboard")
st.subheader("Adaptation and Loss & Damage finance prioritization prototype")

households = st.number_input("Number of affected households", value=1000)
mean_loss = st.number_input("Mean estimated economic loss per household (TZS)", value=2500000)
adaptation_cost = st.number_input("Estimated adaptation support per household (TZS)", value=800000)

total_loss = households * mean_loss
total_adaptation_need = households * adaptation_cost
finance_gap = total_loss - total_adaptation_need

c1, c2, c3 = st.columns(3)

c1.metric("Estimated Economic Loss", f"TZS {total_loss:,.0f}")
c2.metric("Adaptation Finance Need", f"TZS {total_adaptation_need:,.0f}")
c3.metric("Indicative Finance Gap", f"TZS {finance_gap:,.0f}")

st.markdown("## Finance Interpretation")

if finance_gap > 0:
    st.warning("Estimated losses exceed current adaptation support needs. This area should be prioritized for Loss & Damage and adaptation finance.")
else:
    st.success("Estimated adaptation support may be sufficient for immediate household-level needs.")

st.info("Future version: integrate real district population, exposure, vulnerability, and climate finance tracking.")
