# Predicción de Quiebra Empresarial con Aprendizaje de Máquina (Taiwanese Bankruptcy)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wanerge/proyecto-modelos2/blob/main/Proyecto_Final_Quiebra_Taiwan.ipynb)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status: Finalizado](https://img.shields.io/badge/Status-Completado-success.svg)]()

Trabajo final de laboratorio para la materia **Modelos y Simulación de Sistemas II** de la Universidad de Antioquia (UdeA). Implementa el ciclo completo de diseño y evaluación experimental en Machine Learning para la detección temprana de quiebra empresarial sobre el conjunto de datos de referencia *Taiwanese Bankruptcy Prediction* (UCI Machine Learning Repository ID: 572).

---

## 🎥 Video de la Entrega

[Entrega Final Modelos Y Simulacion 2 // Predicción de Quiebra Empresarial con Aprendizaje de Máquina](https://www.youtube.com/watch?v=ue51Dx1Ptnc)

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
├── Proyecto_Final_Quiebra_Taiwan.ipynb  # Notebook maestro: todo el proceso, ejecutable de principio a fin (Colab)
├── requirements.txt                    # Dependencias de Python requeridas
├── proyecto_modelos_2.pdf              # Informe en formato IEEE (compilado desde informe/main.tex)
├── data/
│   ├── README.md                       # Ficha técnica del dataset
│   └── data.csv                        # Dataset en formato CSV (11 MB)
├── figures/                            # Gráficos generados por el notebook (300 DPI)
├── results/                            # Tablas exportadas por el notebook en CSV
│   ├── tabla_hiperparametros_malla.csv # Mallas de hiperparámetros evaluadas por modelo
│   ├── tabla_modelos_base.csv          # 6 modelos en el espacio original (Train / Val / Test, IC bootstrap)
│   ├── tabla_pca_resultados.csv        # Random Forest y SVM en PCA
│   ├── tabla_umap_resultados.csv       # Random Forest y SVM en UMAP
│   ├── tabla_modelos_adicionales.csv   # Gaussian NB e HistGradientBoosting
│   └── comparativa_global_espacios.csv # Original vs. PCA vs. UMAP
└── informe/
    ├── main.tex                        # Informe en formato IEEE (compilar desde esta carpeta)
    └── refs.bib                        # Referencias bibliográficas en BibTeX
```

---

## 🚀 Instrucciones de Ejecución

### Opción 1: Ejecutar directamente en Google Colab
Haga clic en la insignia superior **"Open in Colab"** o cargue el archivo `Proyecto_Final_Quiebra_Taiwan.ipynb` en Colab. El notebook descarga el dataset desde UCI mediante `ucimlrepo`, por lo que **no requiere subir archivos manualmente**.

> **Tiempo de ejecución:** la búsqueda de hiperparámetros hace que el notebook completo tarde varios minutos (unos 6 min en un PC de escritorio con 24 núcleos; bastante más en Colab). El archivo ya incluye todas las salidas guardadas.

### Opción 2: Ejecución en Entorno Local
1. Clone el repositorio:
   ```bash
   git clone https://github.com/wanerge/proyecto-modelos2.git
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

## 🧪 Cómo se ajustan los modelos (resumen)

1. El 30 % de las empresas (2,046 con 66 quiebras) se reserva como **Test** y no interviene en ninguna decisión.
2. Con el 70 % restante (Train) se prueba una **malla pequeña de hiperparámetros** por modelo (`results/tabla_hiperparametros_malla.csv`) con validación cruzada de 5 pliegues y se elige la combinación con mayor **PR-AUC**.
3. Con esa combinación se repite la validación 5×3 (15 pliegues) para calibrar el umbral de decisión maximizando **F2**.
4. El procedimiento se repite en cada espacio de variables (original, PCA y UMAP).

---

## 📊 Síntesis de Resultados Empíricos

| Modelo | Espacio | Reducción | Hiperparámetros elegidos | Train PR-AUC | Val PR-AUC (±2σ) | Test PR-AUC | Test ROC-AUC | Test F2 | Recall | Precisión |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Regresion Logistica | Espacio Original (94 vars) | 0.0% | `C=0.001` | 0.403 | 0.384 ± 0.120 | 0.410 | 0.942 | 0.494 | 0.651 | 0.252 |
| LDA (Shrinkage) | Espacio Original (94 vars) | 0.0% | `shrinkage=0.99` | 0.311 | 0.312 ± 0.088 | 0.318 | 0.925 | 0.469 | 0.864 | 0.166 |
| KNN | Espacio Original (94 vars) | 0.0% | `n_neighbors=31, weights=distance` | 1.000 | 0.347 ± 0.126 | 0.453 | 0.918 | 0.558 | 0.773 | 0.264 |
| Random Forest | Espacio Original (94 vars) | 0.0% | `max_depth=None, min_samples_leaf=5` | 0.982 | 0.416 ± 0.102 | 0.464 | 0.953 | 0.563 | 0.667 | 0.346 |
| Red Neuronal MLP | Espacio Original (94 vars) | 0.0% | `alpha=0.01, hidden_layer_sizes=(64, 32)` | 0.653 | 0.338 ± 0.242 | 0.480 | 0.942 | 0.506 | 0.606 | 0.305 |
| SVM (RBF Kernel) | Espacio Original (94 vars) | 0.0% | `C=0.1, gamma=0.001` | 0.397 | 0.391 ± 0.119 | 0.419 | 0.939 | 0.531 | 0.667 | 0.293 |
| Random Forest | PCA 90% Var (k=23) | 75.5% | `max_depth=12, min_samples_leaf=10` | 0.941 | 0.343 ± 0.139 | 0.420 | 0.934 | 0.511 | 0.651 | 0.274 |
| SVM (RBF Kernel) | PCA 90% Var (k=23) | 75.5% | `C=0.1, gamma=0.003` | 0.417 | 0.401 ± 0.136 | 0.426 | 0.941 | 0.559 | 0.742 | 0.282 |
| Random Forest | PCA 95% Var (k=31) | 67.0% | `max_depth=None, min_samples_leaf=10` | 0.961 | 0.350 ± 0.133 | 0.417 | 0.935 | 0.501 | 0.682 | 0.243 |
| SVM (RBF Kernel) | PCA 95% Var (k=31) | 67.0% | `C=0.1, gamma=0.003` | 0.419 | 0.403 ± 0.134 | 0.443 | 0.944 | 0.568 | 0.742 | 0.293 |
| Random Forest | UMAP (k=10) | 89.4% | `max_depth=6, min_samples_leaf=5` | 0.463 | 0.297 ± 0.175 | 0.331 | 0.914 | 0.506 | 0.682 | 0.249 |
| SVM (RBF Kernel) | UMAP (k=10) | 89.4% | `C=100, gamma=0.003` | 0.237 | 0.241 ± 0.113 | 0.259 | 0.905 | 0.512 | 0.727 | 0.234 |
| Random Forest | UMAP (k=20) | 78.7% | `max_depth=None, min_samples_leaf=5` | 0.935 | 0.274 ± 0.122 | 0.314 | 0.906 | 0.443 | 0.849 | 0.152 |
| SVM (RBF Kernel) | UMAP (k=20) | 78.7% | `C=10, gamma=scale` | 0.212 | 0.216 ± 0.074 | 0.215 | 0.903 | 0.468 | 0.667 | 0.214 |
| Gaussian NB (Extra) | Espacio Original (94 vars) | 0.0% | `var_smoothing=1e-09` | 0.253 | 0.256 ± 0.066 | 0.267 | 0.925 | 0.469 | 0.849 | 0.168 |
| HistGradientBoosting (Extra) | Espacio Original (94 vars) | 0.0% | `learning_rate=0.05, max_depth=3` | 0.713 | 0.373 ± 0.097 | 0.430 | 0.951 | 0.554 | 0.742 | 0.275 |

> Los valores se generan a partir de los archivos de `results/` producidos por el notebook. Los intervalos de confianza al 95 % (bootstrap estratificado, 1,000 réplicas) están en `results/tabla_modelos_base.csv`. Con solo 66 quiebras en Test, las diferencias de F2 entre modelos no son concluyentes.

---

## 🤖 Declaración de uso de inteligencia artificial y responsabilidad

Utilizamos un asistente de inteligencia artificial (GitHub Copilot, en Visual Studio Code) como herramienta de apoyo para proponer la estructura del trabajo, escribir y depurar código, ejecutar los experimentos, generar tablas y figuras, redactar y reformular textos y compilar el informe.

Nosotros definimos el problema y el alcance, decidimos los criterios metodológicos, solicitamos y revisamos cada modificación, corregimos afirmaciones no sustentadas por los resultados y verificamos que las cifras del texto coincidieran con las salidas del notebook. **Todos los integrantes asumimos plena responsabilidad por el contenido del informe y del repositorio.** La herramienta de IA no figura como autora ni asume responsabilidad alguna.
