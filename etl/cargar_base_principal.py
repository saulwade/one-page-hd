# etl/cargar_base_principal.py

import pandas as pd
import sqlite3
from datetime import datetime
import os

# Ruta al archivo Excel
df = pd.read_excel(r"C:\Users\1069657\OneDrive - Home Depot Mexico S.A. de C.V\One Page\data\data.xlsx")

# Limpiar columnas si es necesario (quitar espacios en nombres de columna)
df.columns = [col.strip() for col in df.columns]
df.rename(columns={'#': 'tienda'}, inplace=True)

# Asegúrate de que tenga las columnas 'Semana3' y 'Año'
# Si no existen, las creamos a partir de la columna original (asumimos que es columna B)
if "Semana3" not in df.columns or "Año" not in df.columns:
    # Busca la columna que contiene valores tipo '2025-03-10.11'
    columna_fecha = df.columns[1]  # normalmente es la columna B
    df["Año"] = df[columna_fecha].astype(str).str[:4].astype(int)
    df["Semana3"] = df[columna_fecha].astype(str).str[-2:].astype(int)

# Agregar columna de fecha de carga
df["fecha_carga"] = datetime.today().strftime("%Y-%m-%d")

# Crear conexión SQLite
conn = sqlite3.connect("db/inventarios.db")

# Insertar en la base de datos (reemplaza tabla si ya existe)
df.to_sql("data_one_page", conn, if_exists="replace", index=False)

# Confirmar
print("✅ Base de datos cargada correctamente con", len(df), "registros.")

conn.close()
