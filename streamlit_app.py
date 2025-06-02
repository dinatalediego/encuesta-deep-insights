# streamlit_app.py
import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📊 Dashboard ENAHO 2024")

@st.cache_data
def cargar_datos():
    path = Path("datos/enaho_2024_limpio.csv")
    return pd.read_csv(path) if path.exists() else None

df = cargar_datos()

if df is not None:
    st.write("Vista previa de los datos:")
    st.dataframe(df.head())

    st.subheader("🎯 Análisis por Nivel Educativo")
    st.bar_chart(df["nivel_educativo_actual"].value_counts())
else:
    st.warning("Archivo 'enaho_2024_limpio.csv' no encontrado. Ejecuta primero el pipeline.")
