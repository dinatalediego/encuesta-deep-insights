# procesamiento_enaho_mod100_200.py

"""
Módulo de carga y renombrado de variables para los módulos 100 y 200 de ENAHO 2024.
Sólo se toman las primeras 100 filas de cada archivo.
La lógica de renombrado se estructura con diccionarios separados y estilo modular
para facilitar mantenimiento y extensión futura (MLOps-friendly).
"""

import pandas as pd
from pathlib import Path

# --- Rutas de entrada ---
MOD_100_PATH = Path("./data/Enaho01-2024-100.csv")
MOD_200_PATH = Path("./data/Enaho01-2024-200.csv")

# --- Diccionarios de renombrado ---
dict_rename_100 = {
    "conglome": "id_conglomerado",
    "vivienda": "id_vivienda",
    "hogar": "id_hogar",
    "ubigeo": "ubigeo",
    "p100": "asistencia_escolar",
    "p101": "nivel_educativo_actual"#,
    # Agrega más según el diccionario completo
}

dict_rename_200 = {
    "conglome": "id_conglomerado",
    "vivienda": "id_vivienda",
    "hogar": "id_hogar",
    "ubigeo": "ubigeo",
    "p200": "salud_afiliacion",
    "p201": "tipo_seguro"#,
    # Agrega más según el diccionario completo
}

# --- Función de carga y renombrado ---
def cargar_y_renombrar(path, diccionario_renombre, n=100):
    df = pd.read_csv(path, encoding='latin1').head(n)
    df = df.rename(columns=diccionario_renombre)
    return df

# --- Carga de datos ---
def main():
    df_100 = cargar_y_renombrar(MOD_100_PATH, dict_rename_100)
    df_200 = cargar_y_renombrar(MOD_200_PATH, dict_rename_200)

    print("✅ Modulo 100 columnas:", df_100.columns.tolist())
    print("✅ Modulo 200 columnas:", df_200.columns.tolist())

    return df_100, df_200

if __name__ == "__main__":
    df_mod100, df_mod200 = main()
