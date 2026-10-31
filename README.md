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

| Modelo | Espacio | Reducción | Val PR-AUC ($\pm 2\sigma$) | Test PR-AUC | Test ROC-AUC | Test $F_2$ | Test Recall | Test Precision | Test MCC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Regresion Logistica | Original (94) | 0.0% | 0.372 ± 0.098 | 0.401 | 0.938 | 0.480 | 0.621 | 0.252 | 0.365 |
| LDA (Shrinkage) | Original (94) | 0.0% | 0.379 ± 0.147 | 0.432 | 0.936 | 0.539 | 0.712 | 0.273 | 0.413 |
| KNN (k=15, distance) | Original (94) | 0.0% | 0.316 ± 0.137 | 0.435 | 0.884 | **0.550** | 0.788 | 0.249 | 0.413 |
| Random Forest | Original (94) | 0.0% | 0.393 ± 0.123 | 0.404 | 0.947 | 0.536 | 0.682 | 0.288 | 0.417 |
| Red Neuronal MLP | Original (94) | 0.0% | 0.338 ± 0.242 | **0.480** | 0.942 | 0.506 | 0.606 | 0.305 | 0.404 |
| SVM (RBF Kernel) | Original (94) | 0.0% | 0.383 ± 0.163 | 0.418 | 0.940 | 0.478 | 0.606 | 0.260 | 0.367 |
| Random Forest | PCA 90% Var (k=23) | 75.5% | 0.319 ± 0.134 | 0.382 | 0.931 | 0.494 | 0.682 | 0.236 | 0.369 |
| SVM (RBF Kernel) | PCA 90% Var (k=23) | 75.5% | 0.349 ± 0.146 | 0.378 | 0.932 | 0.531 | 0.758 | 0.241 | 0.397 |
| Random Forest | PCA 95% Var (k=31) | 67.0% | 0.336 ± 0.122 | 0.394 | 0.934 | 0.458 | 0.621 | 0.223 | 0.339 |
| SVM (RBF Kernel) | PCA 95% Var (k=31) | 67.0% | 0.374 ± 0.143 | 0.408 | 0.932 | 0.503 | 0.651 | 0.264 | 0.386 |
| Random Forest | UMAP (k=10) | 89.4% | 0.301 ± 0.176 | 0.327 | 0.905 | 0.482 | 0.697 | 0.216 | 0.354 |
| SVM (RBF Kernel) | UMAP (k=10) | 89.4% | 0.250 ± 0.115 | 0.268 | 0.909 | 0.465 | 0.788 | 0.176 | 0.335 |
| Random Forest | UMAP (k=20) | 78.7% | 0.262 ± 0.131 | 0.304 | 0.907 | 0.450 | 0.515 | 0.298 | 0.366 |
| SVM (RBF Kernel) | UMAP (k=20) | 78.7% | 0.202 ± 0.085 | 0.212 | 0.898 | 0.470 | 0.758 | 0.187 | 0.339 |
| Gaussian NB (Extra) | Original (94) | 0.0% | 0.255 ± 0.066 | 0.267 | 0.925 | 0.473 | 0.849 | 0.171 | 0.342 |
| HistGradientBoosting (Extra) | Original (94) | 0.0% | 0.425 ± 0.108 | 0.453 | **0.954** | 0.522 | 0.576 | 0.380 | **0.446** |

> Todos los valores reproducen literalmente los archivos de `results/` generados por el notebook (ningún número se transcribe a mano). En negrita, el mejor valor de cada columna. Los intervalos de confianza al 95 % (bootstrap estratificado, 1 000 réplicas) de los modelos del espacio original están en `results/tabla_modelos_base.csv`.

