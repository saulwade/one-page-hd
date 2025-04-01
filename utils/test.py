import sys
import os

# Agregamos el path raíz del proyecto para que funcione el import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.queries import get_df_itd

# Obtener el resumen tipo ITD
df = get_df_itd()

# Mostrar los primeros registros
print(df.head(10))
