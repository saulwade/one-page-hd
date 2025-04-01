import streamlit as st
from utils.queries import get_df_itd
import pandas as pd

st.set_page_config(page_title="Dashboard ITD", layout="wide")

st.title("🟠 Dashboard ITD - The Home Depot")

# Obtener datos procesados
df = get_df_itd()

# Filtros interactivos
tiendas_disponibles = df["tienda"].sort_values().unique()
tiendas_seleccionadas = st.multiselect("Selecciona tiendas", tiendas_disponibles, default=tiendas_disponibles)

df_filtrado = df[df["tienda"].isin(tiendas_seleccionadas)]

# Mostrar tabla
st.dataframe(df_filtrado.style.format({
    "MC acumulado": "${:,.0f}",
    "Ventas acumuladas": "${:,.0f}",
    "MC% ponderado": "{:.2f}%",
}), use_container_width=True)

# Métricas generales
col1, col2, col3 = st.columns(3)
col1.metric("Tiendas seleccionadas", len(df_filtrado))
col2.metric("MC Total", f"${df_filtrado['MC acumulado'].sum():,.0f}")
col3.metric("MC% Promedio", f"{df_filtrado['MC% ponderado'].mean():.2f}%")
