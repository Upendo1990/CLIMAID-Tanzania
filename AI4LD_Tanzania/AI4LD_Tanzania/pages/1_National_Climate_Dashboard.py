import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import random
import os

st.set_page_config(
    page_title="National Climate Dashboard",
    page_icon="",
    layout="wide"
)

@st.cache_data
def load_districts():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    shapefile_path = os.path.join(
        base_dir,
        "maps",
        "tza_admbnda_adm2_20181019.shp"
    )

    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs(epsg=4326)

    random.seed(42)
    risk_levels = ["Low", "Moderate", "High", "Very High"]
    gdf["Risk_Level"] = [random.choice(risk_levels) for _ in range(len(gdf))]

    return gdf


districts = load_districts()

st.title("National Climate Dashboard")
st.subheader("Interactive Tanzania District Climate Risk Map")

st.write(
    "This dashboard visualizes Tanzania district boundaries and climate-risk categories. "
    "The risk layer will be updated with operational drought indicators in future versions."
)

st.sidebar.header("Map Controls")

regions = ["All Tanzania"] + sorted(districts["ADM1_EN"].dropna().unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

risk_options = ["All", "Low", "Moderate", "High", "Very High"]
selected_risk = st.sidebar.selectbox("Select Risk Level", risk_options)

map_data = districts.copy()

if selected_region != "All Tanzania":
    map_data = map_data[map_data["ADM1_EN"] == selected_region]

if selected_risk != "All":
    map_data = map_data[map_data["Risk_Level"] == selected_risk]

districts_list = ["All Districts"] + sorted(map_data["ADM2_EN"].dropna().unique())
selected_district = st.sidebar.selectbox("Select District", districts_list)

if selected_district != "All Districts":
    map_data = map_data[map_data["ADM2_EN"] == selected_district]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Regions", districts["ADM1_EN"].nunique())
c2.metric("Districts", districts["ADM2_EN"].nunique())
c3.metric("Selected Districts", len(map_data))
c4.metric("Risk Layer", selected_risk)

colors = {
    "Low": "#2E7D32",
    "Moderate": "#F9A825",
    "High": "#ED6C02",
    "Very High": "#B71C1C"
}

m = folium.Map(
    location=[-6.3, 35.0],
    zoom_start=6,
    tiles="CartoDB positron"
)

def style_function(feature):
    risk = feature["properties"].get("Risk_Level", "Low")
    return {
        "fillColor": colors.get(risk, "#CCCCCC"),
        "color": "#0B3C5D",
        "weight": 0.8,
        "fillOpacity": 0.65,
    }

def highlight_function(feature):
    return {
        "fillColor": "#0B3C5D",
        "color": "#000000",
        "weight": 3,
        "fillOpacity": 0.75,
    }

folium.GeoJson(
    map_data,
    name="Tanzania District Risk Layer",
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["ADM1_EN", "ADM2_EN", "ADM2_PCODE", "Risk_Level"],
        aliases=["Region:", "District:", "District Code:", "Risk Level:"],
        localize=True
    )
).add_to(m)

folium.LayerControl().add_to(m)

st_folium(m, height=700, width=1200)

st.markdown("---")
st.header("Selected Area Summary")

if selected_district != "All Districts" and len(map_data) > 0:
    row = map_data.iloc[0]

    a, b, c, d = st.columns(4)
    a.metric("Region", row["ADM1_EN"])
    b.metric("District", row["ADM2_EN"])
    c.metric("District Code", row["ADM2_PCODE"])
    d.metric("Risk Level", row["Risk_Level"])
else:
    st.info("Select a specific district from the sidebar to view district-level details.")

st.markdown("## Risk Legend")

l1, l2, l3, l4 = st.columns(4)
l1.success("Low")
l2.warning("Moderate")
l3.warning("High")
l4.error("Very High")

st.caption(
    "Boundary source: Tanzania administrative level 2 boundaries from OCHA/HDX COD-AB."
)
