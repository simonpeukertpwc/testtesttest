pip install -U pip
pip install streamlit
pip install networkx


import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(
    page_title="Sogrim",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache(allow_output_mutation=True)
def load_data():
  with open('./app/data.json') as f:
    json_data = json.load(f)
    gpd_data = gpd.GeoDataFrame.from_features(json_data["features"]).set_index("gemeinde.NAME")
    return gpd_data

@st.cache
def get_data_unit(feature):
  data_unit = {
      "BEVDICHTE_SQKM_2019": "p/sqkm",
      "AUSLAENDER_ANTEIL_2019": "%",
      "ALTERSVERTEILUNG_ANTEIL_0_19_2019": "%",
      "ALTERSVERTEILUNG_ANTEIL_20_64_2019": "%",
      "ALTERSVERTEILUNG_ANTEIL_65PLUS_2019": "%",
      "PRIVATHAUSHALTE_2019": "Hshlt.",
      "GESAMTFLAECHE_SQKM_2016": "sqkm",
      "LANDWIRTSCHAFTSFLAECHE_ANTEIL_2004": "%",
      "WALD_GEHOELZE_ANTEIL_2004": "%",
      "UNPRODUKTIVE_FLAECHE_ANTEIL_2004": "%",
      "BESCHAEFTIGTE_ERSTERSEKTOR_2018": "p.",
      "BESCHAEFTIGTE_ZWEITERSEKTOR_2018": "p.",
      "BESCHAEFTIGTE_DRITTERSEKTOR_2018": "p.",
      "NEUWOHNUNGEN_PRO_1000_2018": "Wo./1,000p",
      "SOZAILHILFEQUOTE_2019": "%",
      "WAEHLERANTEIL_SP_2019": "%",
      "WAEHLERANTEIL_SVP_2019": "%",
      "AVG_INCOME_PRO_STEUERPFLPERSON": "Chf/p.",
      "ANZAHL_FAHRZEUGE": "Fhrz.",
      "ANZAHL_HALTESTELLEN_OV": "Hltst.",
      "ANZAHL_FILIALEN_MIGROS": "Fil."
  }
  return data_unit[feature]


st.sidebar.title("Sogrim")
nav = st.sidebar.radio(
    "Navigation", ("Data Exploration", "Location Optimizer"))
st.sidebar.header("About")
st.sidebar.write("""The purpose of SOGRIM is to help Migros optimize their store locations.
For this purpose, we leverage a wide range of data points from various pubic data sources such as the Federal Bureau of Statistics.""")

data = load_data()



if nav == "Location Optimizer":
  choice_model = st.selectbox("Select a Model", ["linregModel","knnModel","rfModel","xgbrModel","ensemble"])

  col1, col2, col3 = st.columns(3)

  col1.metric("# Consolidations", len(
      data[data[choice_model] < data.ANZAHL_FILIALEN_MIGROS]))
  col2.metric("# Same", len(
      data[data[choice_model] == data.ANZAHL_FILIALEN_MIGROS]))
  col3.metric("# Opportunities", len(
      data[data[choice_model] > data.ANZAHL_FILIALEN_MIGROS]))

  fig = px.choropleth_mapbox(data,
                           geojson=data.geometry,
                           locations=data.index,
                           color=(data[choice_model]-data.ANZAHL_FILIALEN_MIGROS),
                           center={"lat": 46.9, "lon": 8.2275},
                           mapbox_style="open-street-map",
                           zoom=7,
                           color_continuous_scale=["red", "green", "blue"],
                           color_continuous_midpoint=0,
                           opacity=0.5,width=1600, height=800)

  st.plotly_chart(fig)

  st.dataframe(data.drop("geometry", axis=1))
