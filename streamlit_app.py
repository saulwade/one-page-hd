# streamlit_app.py

import streamlit as st
from utils.queries import get_df_itd
import pandas as pd

st.set_page_config(page_title="Dashboard ITD", layout="wide")

st.title("🟠 Dashboard ITD - The Home Depot")

df = get_df_itd()

# Filtros
tiendas_disponibles = df["Distrito / Tienda"].sort_values().unique()
tiendas_seleccionadas = st.multiselect("Selecciona tiendas", tiendas_disponibles, default=tiendas_disponibles)
df_filtrado = df[df["Distrito / Tienda"].isin(tiendas_seleccionadas)]

# Tabla
st.dataframe(df_filtrado.style.format({
    "MC %": "{:.2f}%",
    "MC% Plan": lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else "",
    "MNC %": "{:.2f}%",
    "MNC % Plan": lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else "",
    "MT %": "{:.2f}%",
    "MT % Plan": lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else "",
}), use_container_width=True)
# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Tiendas seleccionadas", len(df_filtrado))
col2.metric("MC% Promedio", f"{df_filtrado['MC %'].mean():.2f}%")
col3.metric("MNC% Promedio", f"{df_filtrado['MNC %'].mean():.2f}%")
