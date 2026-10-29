# Dataset: Taiwanese Bankruptcy Prediction

- **Fuente:** [UCI Machine Learning Repository (ID: 572)](https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction)
- **Recopilado por:** Taiwan Economic Journal (TEJ), periodo 1999-2009.
- **Observaciones:** 6,819 empresas taiwanesas registradas en la bolsa de valores TWSE.
- **Características:** 95 ratios financieros originales + 1 etiqueta binaria de quiebra (`Bankrupt?`).
- **Valores faltantes:** 0 (conjunto completamente auditado).
- **Desbalance:**
  - Empresas solventes (clase 0): 6,599 (96.77%)
  - Empresas en quiebra (clase 1): 220 (3.23%)
  - Proporción aproximada: 30 a 1.

## Nota sobre preprocesamiento y carga
El notebook principal `Proyecto_Final_Quiebra_Taiwan.ipynb` incluye un mecanismo de carga dual:
1. Lectura directa desde el archivo local `data/data.csv`.
2. Respaldo automatizado mediante `ucimlrepo` (`fetch_ucirepo(id=572)`) para ejecución directa en Google Colab sin requerir carga manual de archivos.
