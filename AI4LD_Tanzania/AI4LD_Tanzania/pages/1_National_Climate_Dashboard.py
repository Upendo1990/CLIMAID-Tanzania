import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Analytics and Explainability",
    layout="wide"
)

st.title("Analytics and Explainability")
st.subheader("Understanding Climate Loss and Damage Patterns")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "AI4LD_Simanjiro_396HH_Simulated_LossDamage_Dataset.xlsx"
)

FEATURES_PATH = os.path.join(BASE_DIR, "models", "AI4LD_LD_features.pkl")
ECON_MODEL_PATH = os.path.join(BASE_DIR, "models", "AI4LD_economic_loss_model.pkl")
NELD_MODEL_PATH = os.path.join(BASE_DIR, "models", "AI4LD_neld_model.pkl")
VULN_MODEL_PATH = os.path.join(BASE_DIR, "models", "AI4LD_vulnerability_model.pkl")

df = pd.read_excel(DATA_PATH)

st.write(
    "This module explores household Loss and Damage patterns and explains which variables "
    "are most important in the AI prediction models."
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Households", len(df))
c2.metric("Mean Economic Loss", f"TZS {df['Economic_Loss_TZS'].mean():,.0f}")
c3.metric("Mean NELD Score", f"{df['NELD_Score_0to100'].mean():.1f}/100")
c4.metric("High Vulnerability", (df["Vulnerability_Class"] == "High").sum())

st.markdown("---")

st.header("Loss and Damage by Drought Class")

summary = df.groupby("Drought_Class").agg(
    Mean_Economic_Loss_TZS=("Economic_Loss_TZS", "mean"),
    Mean_NELD_Score=("NELD_Score_0to100", "mean"),
    Mean_Total_LD_Score=("Total_Loss_Damage_Score_0to100", "mean"),
    Households=("Household_ID", "count")
).reset_index()

st.dataframe(summary, use_container_width=True)

st.bar_chart(
    summary.set_index("Drought_Class")[["Mean_Total_LD_Score"]]
)

st.header("Economic Loss Distribution")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["Economic_Loss_TZS"], bins=25)
ax.set_xlabel("Economic Loss (TZS)")
ax.set_ylabel("Number of Households")
ax.set_title("Distribution of Economic Loss")
st.pyplot(fig)

st.header("Non-Economic Loss and Damage by Vulnerability Class")

neld_summary = df.groupby("Vulnerability_Class")["NELD_Score_0to100"].mean().reset_index()
st.bar_chart(neld_summary.set_index("Vulnerability_Class"))

st.header("AI Model Feature Importance")

model_choice = st.selectbox(
    "Select AI model",
    [
        "Economic Loss Model",
        "NELD Model",
        "Vulnerability Model"
    ]
)

features = joblib.load(FEATURES_PATH)

if model_choice == "Economic Loss Model":
    model = joblib.load(ECON_MODEL_PATH)
elif model_choice == "NELD Model":
    model = joblib.load(NELD_MODEL_PATH)
else:
    model = joblib.load(VULN_MODEL_PATH)

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

st.dataframe(importance, use_container_width=True)

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.barh(importance["Feature"].head(12), importance["Importance"].head(12))
ax2.invert_yaxis()
ax2.set_xlabel("Importance")
ax2.set_title(f"Top Feature Importance: {model_choice}")
st.pyplot(fig2)

st.header("Interpretation")

st.info(
    "The analytics module helps users understand how drought severity, rainfall, vegetation condition, "
    "livestock loss, water scarcity, pasture shortage, and household characteristics contribute to "
    "economic and non-economic Loss and Damage."
)
