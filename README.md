# Predicción de Quiebra Empresarial con Aprendizaje de Máquina (Taiwanese Bankruptcy)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USUARIO/REPO/blob/main/Proyecto_Final_Quiebra_Taiwan.ipynb)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status: Finalizado](https://img.shields.io/badge/Status-Completado-success.svg)]()

Trabajo final de laboratorio para la materia **Modelos y Simulación de Sistemas II** de la Universidad de Antioquia (UdeA). Implementa el ciclo completo de diseño y evaluación experimental en Machine Learning para la detección temprana de quiebra empresarial sobre el conjunto de datos de referencia *Taiwanese Bankruptcy Prediction* (UCI Machine Learning Repository ID: 572).

---

## 👥 Integrantes del Equipo
- **Wanerge Almanza Velasquez**
- **Jhon Fredy Hoyos Cardenas**
- **Miguel Angel Castiblanco Florez**

**Docente:** Julián D. Arias-Londoño  
**Institución:** Departamento de Ingeniería de Sistemas, Facultad de Ingeniería, Universidad de Antioquia (Medellín, Colombia)

---

## 📌 Resumen del Proyecto y Características del Dataset
- **Fuente Oficial:** [UCI Machine Learning Repository - Dataset 572](https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction)
- **Periodo:** 1999 - 2009 (Taiwan Economic Journal - TEJ, Bolsa de Taiwán TWSE).
- **Muestras:** 6,819 firmas auditadas.
- **Predictores:** 94 variables continuas contables y financieras útiles (tras descartar la columna `Net Income Flag` por varianza cero).
- **Variable Objetivo (`Bankrupt?`):**
  - **Clase 0 (Solvente):** 6,599 empresas (96.77%)
  - **Clase 1 (Quiebra):** 220 empresas (3.23%)
  - **Proporción de Desbalance:** **30 a 1**.

---

## 📂 Estructura del Repositorio

```text
proyecto-modelos2/
├── Proyecto_Final_Quiebra_Taiwan.ipynb  # Notebook maestro unificado (compatible con Google Colab)
├── requirements.txt                    # Dependencias de Python requeridas
├── PLAN_PROYECTO.md                    # Documento formal de planificación por fases
├── data/
│   ├── README.md                       # Ficha técnica del dataset
│   └── data.csv                        # Dataset en formato CSV (11 MB)
├── figures/                            # Gráficos generados para el informe (300 DPI)
│   ├── fig1_desbalance_clases.png
│   ├── fig2_asimetria_outliers.png
│   ├── fig3_matriz_correlaciones.png
│   ├── fig4_curvas_roc_pr_base.png
│   ├── fig5_matrices_confusion_base.png
│   ├── fig6_pca_varianza_explicada.png
│   ├── fig7_umap_pca_2d.png
│   └── fig8_shap_summary.png
├── results/                            # Tablas comparativas y análisis exportados en CSV
│   ├── pares_alta_correlacion.csv
│   ├── analisis_individual_variables.csv
│   ├── variables_candidatas_eliminar.csv
│   ├── tabla_modelos_base.csv
│   ├── tabla_pca_resultados.csv
│   ├── tabla_umap_resultados.csv
│   ├── tabla_modelos_adicionales.csv
│   └── comparativa_global_espacios.csv
└── informe/
    ├── main.tex                        # Borrador del informe en formato IEEE Transactions (<= 10 págs.)
    └── refs.bib                        # Referencias bibliográficas en BibTeX
```

---

## 🚀 Instrucciones de Ejecución

### Opción 1: Ejecutar directamente en Google Colab
Haga clic en la insignia superior **"Open in Colab"** o cargue el archivo `Proyecto_Final_Quiebra_Taiwan.ipynb` en Colab. El notebook detectará automáticamente el entorno y descargará el dataset directamente desde UCI mediante `ucimlrepo`, por lo que **no requiere subir archivos manualmente**.

### Opción 2: Ejecución en Entorno Local
1. Clone el repositorio:
   ```bash
   git clone https://github.com/USUARIO/REPO.git
   cd proyecto-modelos2
   ```
2. Cree y active un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```
3. Instale las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie Jupyter Notebook:
   ```bash
   jupyter notebook Proyecto_Final_Quiebra_Taiwan.ipynb
   ```

---

## 📊 Síntesis de Resultados Empíricos

| Modelo | Espacio | Reducción (%) | Val PR-AUC ($\pm 2\sigma$) | Test PR-AUC [95% CI] | Test ROC-AUC | Test $F_2$ [95% CI] | Test Recall | Test Precision |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | Original (94) | 0.0% | **0.393 $\pm$ 0.123** | 0.404 [0.291, 0.525] | **0.941** | **0.536 [0.430, 0.635]** | 0.742 | 0.254 |
| **SVM (RBF Kernel)** | Original (94) | 0.0% | 0.383 $\pm$ 0.163 | 0.418 [0.302, 0.539] | 0.938 | 0.478 [0.371, 0.577] | 0.697 | 0.224 |
| **Random Forest** | PCA (k=23) | **75.5%** | 0.324 $\pm$ 0.149 | 0.387 [0.275, 0.508] | 0.935 | 0.515 [0.410, 0.618] | 0.742 | 0.231 |
| **SVM (RBF Kernel)** | PCA (k=31) | **67.0%** | 0.374 $\pm$ 0.136 | 0.406 [0.290, 0.528] | 0.939 | **0.538 [0.432, 0.639]** | 0.652 | 0.316 |
| **HistGradientBoosting** | Original (94) | 0.0% | 0.425 $\pm$ 0.108 | **0.453 [0.338, 0.572]** | 0.933 | 0.522 [0.415, 0.621] | 0.758 | 0.233 |
