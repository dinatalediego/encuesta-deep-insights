# merge_enaho_modulos.py

"""
Une los módulos 100 y 200 de ENAHO 2024 en base al ID de hogar.
Aplica renombrado de columnas con diccionarios más amplios, y guarda CSV limpio
para posterior análisis educativo y de salud.
"""

import pandas as pd
from pathlib import Path
from procesamiento_enaho_mod100_200 import cargar_y_renombrar

# --- Diccionarios más amplios de renombrado ---
dict_rename_100 = {
    "conglome": "id_conglomerado",
    "vivienda": "id_vivienda",
    "hogar": "id_hogar",
    "ubigeo": "ubigeo",
    "p100": "asistencia_escolar",
    "p101": "nivel_educativo_actual",
    "p102": "grado_aprobado",
    "p103": "motivo_no_asiste",
    "p104": "tipo_centro_estudio",
    "p105": "lugar_estudio",
    "p106": "nivel_maximo",
    "p107": "termino_estudios",
    "p108": "anos_aprobados",
    "p109": "analfabeto",
    "p110": "sabe_leer"
}

dict_rename_200 = {
    "conglome": "id_conglomerado",
    "vivienda": "id_vivienda",
    "hogar": "id_hogar",
    "ubigeo": "ubigeo",
    "p200": "salud_afiliacion",
    "p201": "tipo_seguro",
    "p202": "lugar_atencion",
    "p203": "ultimo_control",
    "p204": "estado_salud_autop",
    "p205": "problemas_salud",
    "p206": "dias_enfermo",
    "p207": "hospitalizacion",
    "p208": "tipo_enfermedad",
    "p209": "motivo_no_atencion",
    "p210": "gasto_salud"
}

# --- Función principal de merge y exportación ---
def combinar_y_guardar(mod100_path, mod200_path, salida_csv, n=100):
    df_100 = cargar_y_renombrar(mod100_path, dict_rename_100, n)
    df_200 = cargar_y_renombrar(mod200_path, dict_rename_200, n)

    claves = ["id_conglomerado", "id_vivienda", "id_hogar", "ubigeo"]
    df_merge = pd.merge(df_100, df_200, on=claves, how="inner")

    df_merge.to_csv(salida_csv, index=False)
    print(f"✅ Archivo combinado guardado en {salida_csv} con {df_merge.shape[0]} filas y {df_merge.shape[1]} columnas.")
    return df_merge

if __name__ == "__main__":
    MOD_100_PATH = Path("./data/Enaho01-2024-100.csv")
    MOD_200_PATH = Path("./data/Enaho01-2024-200.csv")
    SALIDA_PATH = Path("./data/base_limpia_enaho.csv")

    combinar_y_guardar(MOD_100_PATH, MOD_200_PATH, SALIDA_PATH, n=100)
