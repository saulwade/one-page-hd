# utils/queries.py

import pandas as pd
import sqlite3

def get_df_itd():
    # Leer base de datos
    conn = sqlite3.connect("db/inventarios.db")
    df_db = pd.read_sql("SELECT * FROM data_one_page", conn)
    conn.close()

    # Preparar tipos
    df_db["tienda"] = df_db["tienda"].astype(str).str.strip()
    df_db["Semana3"] = pd.to_numeric(df_db["Semana3"], errors="coerce").astype("Int64")
    df_db["Año"] = pd.to_numeric(df_db["Año"], errors="coerce").astype("Int64")

    # Leer rangos
    df_rangos = pd.read_csv("config/rango_inventarios.csv")
    df_rangos["tienda"] = df_rangos["tienda"].astype(str).str.strip()
    df_rangos["semana_inicio"] = pd.to_numeric(df_rangos["semana_inicio"], errors="coerce") + 1  # ✅ sumamos 1 a todas

    # Leer planes
    df_planes = pd.read_excel("config/Planes por tienda.xlsx")
    df_planes["tienda"] = df_planes["#"].astype(str).str.strip()
    df_planes = df_planes[["tienda", "Plan MC", "Plan MNC", "Plan MT"]]

    resultados = []

    for _, row in df_rangos.iterrows():
        tienda = row["tienda"]
        semana_ini = row["semana_inicio"]
        semana_fin = row["semana_fin"]
        año_ini = row["año_inicio"]
        año_fin = row["año_fin"]

        try:
            semana_ini = int(semana_ini)
            semana_fin = int(semana_fin)
            año_ini = int(año_ini)
            año_fin = int(año_fin)
        except (ValueError, TypeError):
            print(f"⚠️ Error en tienda {tienda}: año o semana inválida. Saltando...")
            continue

        df_tienda = df_db[df_db["tienda"] == tienda].copy()
        if df_tienda.empty:
            print(f"⚠️ Tienda {tienda} no encontrada en la base. Saltando...")
            continue

        df_tienda["orden"] = df_tienda["Año"] * 100 + df_tienda["Semana3"]
        lim_inf = año_ini * 100 + semana_ini
        lim_sup = año_fin * 100 + semana_fin

        df_filtrado = df_tienda[(df_tienda["orden"] >= lim_inf) & (df_tienda["orden"] <= lim_sup)]

        total_mc = df_filtrado["MC+"].sum()
        total_mnc = df_filtrado["MNC +"].sum()
        total_mt = df_filtrado["MT +"].sum()
        total_ventas = df_filtrado["Sales $"].sum()

        mc_pond = round((total_mc / total_ventas) * 100, 2) if total_ventas else None
        mnc_pond = round((total_mnc / total_ventas) * 100, 2) if total_ventas else None
        mt_pond = round((total_mt / total_ventas) * 100, 2) if total_ventas else None

        resultados.append({
            "tienda": tienda,
            "MC %": mc_pond,
            "MNC %": mnc_pond,
            "MT %": mt_pond
        })

    df_resultado = pd.DataFrame(resultados)

    # Unir con planes
    df_final = df_resultado.merge(df_planes, how="left", on="tienda")

    # Reordenar y renombrar columnas
    df_final = df_final[[
        "tienda", "MC %", "Plan MC", "MNC %", "Plan MNC", "MT %", "Plan MT"
    ]].rename(columns={
        "tienda": "Distrito / Tienda",
        "Plan MC": "MC% Plan",
        "Plan MNC": "MNC % Plan",
        "Plan MT": "MT % Plan"
    })

    return df_final
