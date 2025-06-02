# pipeline_enaho_mlops.py

"""
Flujo End-to-End para modelado predictivo con la ENAHO 2024
Preparado para MLOps: incluye versionado, seguimiento con MLflow, interpretabilidad con SHAP,
despliegue listo para integración CI/CD.

Estructura:
1. Carga y preprocesamiento
2. Feature Engineering
3. Modelado supervisado (RandomForest)
4. Interpretación con SHAP
5. MLflow Tracking
6. Preparado para servir con API o Streamlit en etapa de despliegue
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pathlib import Path
import os

# Ruta relativa para MLOps
BASE_PATH = Path(".")
DATA_PATH = BASE_PATH / "datos" / "enaho_2024_limpio.csv"
ARTIFACTS_PATH = BASE_PATH / "artifacts"
ARTIFACTS_PATH.mkdir(exist_ok=True)

# 1. Carga de datos
def cargar_datos(path):
    print(f"📥 Cargando datos desde {path}")
    return pd.read_csv(path)

# 2. Preprocesamiento modular
def preprocesamiento(columnas_numericas, columnas_categoricas):
    imputador_num = SimpleImputer(strategy="median")
    imputador_cat = SimpleImputer(strategy="most_frequent")

    escalador = StandardScaler()
    encoder = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", imputador_num), ("scaler", escalador)]), columnas_numericas),
            ("cat", Pipeline([("imputer", imputador_cat), ("encoder", encoder)]), columnas_categoricas),
        ]
    )

    return preprocessor

# 3. Entrenamiento, tracking y visualización

def entrenar_modelo(X_train, X_test, y_train, y_test, preprocessor):
    modelo = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ])

    mlflow.set_experiment("ENAHO_2024_MLOPS")

    with mlflow.start_run():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        f1 = f1_score(y_test, y_pred, average='macro')
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(modelo, "modelo_rf_enaho")

        print("\n📊 Reporte de clasificación:")
        print(classification_report(y_test, y_pred))

        # SHAP para interpretabilidad
        explainer = shap.Explainer(modelo.named_steps["classifier"], X_test, feature_names=X_test.columns)
        shap_values = explainer(X_test)

        plt.title("SHAP Summary Plot")
        shap.summary_plot(shap_values, X_test, show=False)
        plt.savefig(ARTIFACTS_PATH / "shap_summary_plot.png")
        mlflow.log_artifact(ARTIFACTS_PATH / "shap_summary_plot.png")

    return modelo

# Función principal del pipeline

def main():
    df = cargar_datos(DATA_PATH)

    columnas_numericas = ["edad", "ingreso_mensual", "n_miembros_hogar"]
    columnas_categoricas = ["sexo", "region", "tipo_vivienda"]
    target = "vive_en_pobreza"

    X = df[columnas_numericas + columnas_categoricas]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    preprocessor = preprocesamiento(columnas_numericas, columnas_categoricas)
    modelo_final = entrenar_modelo(X_train, X_test, y_train, y_test, preprocessor)

    print("\n✅ Entrenamiento completado y modelo listo para despliegue.")

if __name__ == "__main__":
    main()
