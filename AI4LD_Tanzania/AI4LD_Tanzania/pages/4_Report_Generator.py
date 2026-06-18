
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Report Generator",
    page_icon="",
    layout="wide"
)

st.title(" CLIMAID Report Generator")
st.subheader("Generate Climate Loss and Damage Assessment Reports")

DATA_PATH = "AI4LD_Tanzania/data/AI4LD_Simanjiro_396HH_Simulated_LossDamage_Dataset.xlsx"

df = pd.read_excel(DATA_PATH)

st.write("""
This module generates downloadable climate Loss and Damage summaries for decision-makers, 
researchers, local authorities, and adaptation planners.
""")

st.sidebar.header("Report Settings")

selected_ward = st.sidebar.selectbox(
    "Select Ward",
    ["All Wards"] + sorted(df["Ward"].unique())
)

selected_vulnerability = st.sidebar.selectbox(
    "Select Vulnerability Class",
    ["All"] + sorted(df["Vulnerability_Class"].unique())
)

report_df = df.copy()

if selected_ward != "All Wards":
    report_df = report_df[report_df["Ward"] == selected_ward]

if selected_vulnerability != "All":
    report_df = report_df[report_df["Vulnerability_Class"] == selected_vulnerability]

st.markdown("## Report Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Households", len(report_df))
c2.metric("Mean Economic Loss", f"TZS {report_df['Economic_Loss_TZS'].mean():,.0f}")
c3.metric("Mean NELD Score", f"{report_df['NELD_Score_0to100'].mean():.1f}/100")
c4.metric("High Vulnerability", (report_df["Vulnerability_Class"] == "High").sum())

st.markdown("---")

st.header("Filtered Household Records")
st.dataframe(report_df, use_container_width=True)

st.header("Automated Report Narrative")

mean_loss = report_df["Economic_Loss_TZS"].mean()
mean_neld = report_df["NELD_Score_0to100"].mean()
high_count = (report_df["Vulnerability_Class"] == "High").sum()

report_text = f"""
CLIMAID Climate Loss and Damage Assessment Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Area selected: {selected_ward}
Vulnerability filter: {selected_vulnerability}

Summary:
A total of {len(report_df)} household records were included in this assessment. 
The mean estimated economic loss is TZS {mean_loss:,.0f}. 
The mean Non-Economic Loss and Damage score is {mean_neld:.1f}/100. 
A total of {high_count} households are classified as highly vulnerable.

Interpretation:
The results suggest that climate-related stressors, including drought severity, water scarcity, 
pasture shortage, livestock loss, and crop loss, contribute substantially to household-level 
Loss and Damage. Households classified as highly vulnerable should be prioritized for targeted 
adaptation support, early warning communication, social protection, water access interventions, 
and livelihood resilience measures.

Recommended Actions:
- Prioritize rapid Loss and Damage assessment in high-risk areas.
- Strengthen drought early warning systems.
- Support water access and pasture management.
- Provide targeted livestock and livelihood support.
- Integrate household vulnerability into local adaptation planning.
- Use verified field data before operational decision-making.

Prototype Note:
This report is generated from simulated demonstration data and should not be used as verified 
field evidence until replaced with real household survey data.
"""

st.text_area("Report Text", report_text, height=420)

st.download_button(
    label="Download Report as TXT",
    data=report_text,
    file_name="CLIMAID_Loss_and_Damage_Report.txt",
    mime="text/plain"
)

csv = report_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="CLIMAID_Filtered_LossDamage_Data.csv",
    mime="text/csv"
)
