import sqlite3
import pandas as pd

# Conectar a la base
conn = sqlite3.connect("db/inventarios.db")

# Leer los primeros 10 registros
df = pd.read_sql("SELECT * FROM data_one_page LIMIT 10", conn)

# Mostrarlos
print(df)

conn.close()
