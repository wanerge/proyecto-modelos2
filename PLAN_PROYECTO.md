# Plan: Proyecto final – Predicción de quiebra (Taiwanese Bankruptcy, UCI-572)
Materia: Modelos y Simulación de Sistemas II (UdeA) · Carpeta de trabajo: `proyecto-modelos2/`

## 1. Problema y enfoque
Entregar **un notebook maestro `.ipynb` compatible con Google Colab**, en español, con código comentado y explicado, que cubra *todas* las secciones de la Guía del proyecto (§2–§5 + discusión), más repo ordenado (README, requirements, .gitignore), borrador de informe IEEE en LaTeX (≤10 págs.) y sección de explicabilidad. Las decisiones (qué modelo/técnica se prueba, se descarta o se elige) se toman **por análisis de los datos** y se documentan de forma corta en un "Registro de decisiones", usando el estado del arte solo como guía.

## 2. Lo que entendí de la carpeta `Informacion/`
**Guía (rúbrica):** §2 Descripción del problema (10%) · §3 Estado del arte (10%, ≥4 artículos, 1 pág.) · §4 Entrenamiento y evaluación (15%): validación, tabla de hiperparámetros/mallas, **≥5 modelos** (paramétrico gaussiano/regresión, no paramétrico, ensamble de árboles, ANN, SVM), métricas justificadas, resultados con **IC** en train/val/test, figuras con ejes y caption · §5 Reducción de dimensión (15%): análisis individual de variables, **PCA** y **UMAP** reevaluando los **2 mejores modelos con nuevo ajuste de hiperparámetros**, tabla con % de reducción · Discusión/conclusiones comparando con §3 · Evaluación final 50%: objetivos, ≤10 págs., repo claro, video 10 min + preguntas individuales. §2 y §3 ya se entregaron en el avance.

**Avance ya entregado:** problema supervisado, clasificación binaria desbalanceada; 4 artículos (Liang 2016, Wang & Liu 2021, Pham 2025, Azad 2026).

**Teoría – fases (Clase 01, ciclo de 5 pasos):** 1 Obtener datos → 2 Limpiar/preparar → 3 Entrenar modelo → 4 Probar → 5 Mejorar. Clase 06: split train/test (80/20 típico), k-fold dentro de train para hiperparámetros, test una sola vez; patrón de dispersión `media ± 2·std`. Clase 05: matriz de confusión, F-β, MCC, BACC, G-mean, ROC/AUC, advertencia de accuracy con desbalance. Clase 18–22: filtros/wrappers/embebidos, Fisher, PCA (varianza acumulada), UMAP (`umap-learn`, `fit` en train y `transform` en test). Clase 23: SHAP/LIME.

**Estilo del profesor (labs):** celdas con contexto teórico → código → gráficos → conclusión; comentarios en español; `Pipeline`, `StratifiedKFold`, `GridSearchCV`, `learning_curve`, funciones `experimentar(...)` que devuelven tablas. Trampas a evitar: escalar/PCA/selección antes de CV, mirar test para elegir, accuracy como métrica, una sola semilla.

**Hallazgos propios sobre `data.csv` (verificados):**
| Hecho | Implicación |
|---|---|
| 6819×96; 220 quiebras (3.23%), 0 nulos, 0 duplicados | Estratificar siempre; test con ~66 positivos si 70/30 |
| `Net Income Flag` es **constante** (todo 1) → 94 predictores útiles (el avance dice 2 binarias; corregir en informe) | Eliminar en preprocesado |
| `Liability-Assets Flag`: solo 8 filas con valor 1 (6 quiebras) | Variable casi-perfecta pero muy rara; vigilar |
| Nombres de columnas con espacios al inicio y carácter `¥` mal codificado | Limpiar nombres al cargar |
| 24 columnas con valores hasta ~1e10; 62/95 con \|skew\|>5 | Necesita `QuantileTransformer`/log/`RobustScaler` dentro del pipeline (árboles no lo requieren) |
| 28 pares con \|r\|>0.9 (12 con \|r\|>0.99, algunos r=±1) | Redundancia → motiva §5 (PCA/UMAP/filtros) |
| Mejor AUC univariado ≈0.89 (Persistent EPS, Net Income/Total Assets, Net profit before tax/Paid-in capital, Retained Earnings/Total Assets, ROA) | Rentabilidad domina, coherente con literatura |
| Línea base rápida (5-fold, 70% train, QuantileTransformer): AUC 0.92–0.94, AP 0.26–0.45, F2 0.24–0.52 al umbral 0.5; RF recall 0.21 pese a AUC 0.94; KNN débil (AUC 0.85) | **El umbral y el desbalance deciden el resultado**; todo corre en segundos → grids amplios viables en Colab |

**Estado del arte – cautelas para la discusión:** Liang usa muestra balanceada 239/239 (no comparable); Wang & Liu mejor F2=0.423 (NB+ENN, 5 particiones aleatorias); Pham F1=0.985 es sobre datos **remuestreados/balanceados** (verificar en el paper antes de afirmar "fuga" en la sustentación); Azad (CV 5-fold estratificado, resampling solo en train) F1≈0.69–0.71, Recall≈0.81, AUC≈0.93 es el más comparable.

## 3. Estructura de entrega (dentro de `proyecto-modelos2/`)
```
proyecto-modelos2/
├─ Proyecto_Final_Quiebra_Taiwan.ipynb   ← notebook maestro (Colab)
├─ data/data.csv                          ← copia del CSV (11 MB). Respaldo: ucimlrepo (id=572)
├─ figures/  results/                     ← PNG/CSV/.tex exportados desde el notebook (para el informe)
├─ informe/ main.tex, refs.bib            ← borrador IEEEtran
├─ README.md (badge Open in Colab, instrucciones) · requirements.txt · .gitignore (Informacion/)
```
Carga de datos (celda 1 del notebook): `data/data.csv` local → clonar repo/URL raw en Colab → `ucimlrepo`. `USUARIO/REPO` quedará como placeholder hasta que tengas la URL de GitHub.

## 4. Convenciones del notebook
- Español; cada sección abre con **"¿Qué hacemos y por qué?"** (objetivo, clase de teoría relacionada, qué se decide) y cierra con **"Interpretación / Decisión"** (corta).
- Código comentado explicando el *porqué*; funciones auxiliares agrupadas en una sección inicial (métricas, IC, gráficos, tablas).
- **Registro de decisiones** (tabla acumulativa): decisión · opciones probadas · evidencia · elegida · por qué se descartó el resto.
- `SEED=42`, `TEST_SIZE`, `N_SPLITS`, `N_REPEATS` como constantes visibles; flag `RUN_HEAVY` para búsquedas largas.
- Todo preprocesado/remuestreo/PCA/UMAP **dentro de `Pipeline`** (imblearn) → sin fuga de datos. Test se usa una sola vez por modelo final.
- Figuras: título, ejes con nombre, leyenda; tablas/figuras numeradas con caption; export automático a `figures/` y `results/`.
- Compatibilidad Colab: sklearn ≥1.3, Python 3.10–3.13; `!pip install umap-learn imbalanced-learn shap ucimlrepo` en la primera celda.

## 5. Fases (mapeadas a la Guía y al ciclo de la Clase 01)

### Fase 0 – Preparación del repo y entorno
Estructura de carpetas, copia de `data.csv`, `.gitignore`, `requirements.txt`, entorno local (instalar `imbalanced-learn`, `umap-learn`, `shap`, `ucimlrepo`, `nbconvert/ipykernel`; **requiere tu aprobación al implementar**).

### Fase 1 – Obtener datos y descripción del problema (Guía §2 · Clase 01 paso 1)
Contexto y justificación de ML (resumen del avance); composición del dataset (N, variables agrupadas por familia contable, nulos, tipos, codificación, duplicados); EDA: desbalance, distribución/asimetría, outliers de magnitud 1e10, correlaciones, comparación por clase de variables clave; paradigma (supervisado, clasificación binaria desbalanceada, costo asimétrico FN>FP). Incluye la corrección sobre `Net Income Flag`.

### Fase 2 – Estado del arte (Guía §3)
Tabla comparativa corta (≤1 pág.) de los 4 artículos + "Lecciones → decisiones de diseño" (p. ej. resampling solo en train, métricas F2/MCC/PR-AUC, robust scaling).

### Fase 3 – Preparar datos y diseño experimental (Guía §4.1 · Clase 01 paso 2 · Clase 05/06)
1. Limpieza: nombres, eliminar constante, (duplicados exactos/r=±1 se evalúan en Fase 6).
2. **Split** estratificado hold-out (propuesta 70/30 → 66 positivos en test para IC más estrecho; alternativa del curso 80/20; constante `TEST_SIZE`). Test intocable.
3. **Validación interna:** `RepeatedStratifiedKFold` (5×3) sobre train para hiperparámetros.
4. **Preprocesado a decidir por evidencia** (screening rápido): Standard vs log/signed-log vs Robust vs Quantile(normal) ; clipping/winsorización de 1e10.
5. **Desbalance a decidir por evidencia:** nada, `class_weight`, RandomUnderSampler, SMOTE, SMOTE-ENN/ENN — siempre dentro del pipeline y solo en folds de entrenamiento.
6. **Métricas y justificación:** reportar ROC-AUC, **PR-AUC**, F1, **F2**, MCC, Recall, Precisión, BACC, G-mean, matriz de confusión. *Propuesta (a confirmar con evidencia en el notebook):* elegir hiperparámetros con **PR-AUC** (independiente del umbral, robusta al desbalance) y fijar el **umbral operativo** maximizando F2 sobre predicciones *out-of-fold* de train; accuracy solo informativa. Se documentan MCC/F2 como alternativas descartadas/complementarias.
7. **Intervalos de confianza:** validación = `media ± 2·std` (patrón del profesor) y t-IC entre folds; **test = bootstrap estratificado 95%** (1000 remuestreos); train = métrica resubstitución (para mostrar sobreajuste).

### Fase 4 – Tamizaje y selección de familias (Guía §4.1 · Clase 01 paso 3)
Comparar rápido (misma partición/CV) candidatos por familia y **elegir el mejor representante** de cada una con argumento corto; lo descartado queda en el registro:
| Familia obligatoria | Candidatos a tamizar | Notas |
|---|---|---|
| Paramétrico (Clase 02/03) | LogReg (L1/L2), LDA (shrinkage), QDA (reg_param) | GaussianNB queda como **análisis extra** (Wang & Liu lo reportan como mejor en F2) |
| No paramétrico (Clase 04) | KNN (+ opcional Parzen del lab 2) | Requiere escalado; débil en 94-D → se espera mejora con PCA/UMAP |
| Ensamble de árboles (Clase 10) | Random Forest, Bagging/ExtraTrees | Boosting (Clase 11) queda como **análisis extra** |
| ANN (Clase 13) | `MLPClassifier` | Sin `class_weight` → sampler en pipeline |
| SVM (Clase 16) | `SVC` lineal / RBF / poly | `decision_function` para umbral y PR-AUC |

### Fase 5 – Entrenamiento y evaluación de los 5 modelos (Guía §4.1 tabla + §4.2 · Clase 01 paso 4)
Tabla de hiperparámetros y mallas (propuesta; las grandes con `RandomizedSearchCV`):
- LogReg: `C`∈{1e-4…100}, `penalty`∈{l1,l2}, `class_weight`. · LDA: `shrinkage`∈{None,auto,0.1,0.3,0.5,0.9}. · QDA: `reg_param`∈{0,0.01,0.1,0.5,0.9}.
- KNN: `n_neighbors`∈{3,5,11,21,51,101}, `weights`, `p`∈{1,2}.
- RF: `n_estimators`∈{100,300,600}, `max_depth`∈{None,6,10,20}, `min_samples_leaf`∈{1,2,5,10}, `max_features`∈{sqrt,0.3,0.7}, `class_weight`.
- MLP: `hidden_layer_sizes`∈{(10),(20),(50),(20,10),(50,25)}, `activation`∈{relu,tanh,logistic}, `alpha`∈{1e-4,1e-2,0.1,1}, `learning_rate_init`, early stopping.
- SVM: `kernel`∈{linear,rbf,poly}, `C`∈{1e-2…100}, `gamma`∈{scale,1e-4…1}, `class_weight`.

Resultados: curvas de validación (hiperparámetro vs PR-AUC con banda de IC), curvas de aprendizaje, tabla **Train / Validación (±IC) / Test (IC bootstrap)** por modelo, curvas ROC y PR superpuestas, matrices de confusión al umbral elegido, ranking y selección de los **2 mejores modelos** (con argumento: desempeño, estabilidad, costo, interpretabilidad). Opcional: prueba pareada (Wilcoxon/Friedman) entre los mejores.

### Fase 6 – Análisis individual de variables (Guía §5.1 · Clase 18/19/21)
Calculado **solo con train**: correlación con la clase (punto-biserial/Spearman), **AUC univariado**, **índice de Fisher**, información mutua, KS/Mann-Whitney; redundancia (mapa de correlación agrupado, pares |r|>0.9, VIF opcional); contraste con Lasso/L1 y RF (embebidos). Regla explícita de candidatas a eliminar (constantes, duplicadas |r|≥0.99, redundantes de menor poder discriminante, discriminación ≈0.5) y evaluación breve del efecto de quitarlas.

### Fase 7 – Extracción lineal: PCA (Guía §5.2 · Clase 20)
`Pipeline(scaler → PCA(k) → modelo)` para los 2 mejores modelos; criterio de *k* justificado: varianza acumulada (90/95/99%), scree, y curva PR-AUC (CV) vs *k* con regla de **1 error estándar**; **re-ajuste de hiperparámetros** en el nuevo espacio; tabla con *k*, **% de reducción = 1−k/94**, y todas las métricas (train/val/test con IC).

### Fase 8 – Extracción no lineal: UMAP (Guía §5.3 · Clase 22)
`Pipeline(scaler → UMAP → modelo)` con `fit` solo en train y `transform` en validación/test; barrido de `n_components`∈{2,3,5,10,20,30}, `n_neighbors`∈{15,30,50}, `min_dist`∈{0,0.1,0.5}; visualización 2-D coloreada por clase (junto a PCA 2-D); re-ajuste de hiperparámetros; misma tabla que PCA. Se documenta variabilidad por semilla y costo computacional.

### Fase 9 – Mejorar, extras y discusión (Guía §5 punto 12 · Clase 01 paso 5 · Clase 23)
- **Extras:** GaussianNB (Clase 03) y boosting `HistGradientBoosting`/`GradientBoosting` (Clase 11) con el mismo protocolo, solo como análisis de contraste.
- **Explicabilidad del mejor modelo:** SHAP global/local (árboles) y/o importancia por permutación; contraste con Fase 6 y con las variables reportadas en la literatura.
- **Discusión y conclusiones:** comparación base vs PCA vs UMAP (rendimiento vs reducción), comparación con §3 explicando por qué las cifras no son directamente comparables (balanceo del test, métricas), limitaciones (periodo 1999-2009, sin identificador de empresa/tiempo, pocos positivos, umbral/costos), trabajo futuro.

### Fase 10 – Validación integral y entrega
Ejecutar el notebook de principio a fin (local y chequeo de compatibilidad Colab), medir tiempos (meta: razonable en Colab gratuito), confirmar reproducibilidad (semilla), generar `figures/` y `results/`. **Borrador IEEE LaTeX** (`informe/main.tex`, ≤10 págs.) con tablas y figuras exportadas; **README** final (badge Colab, cómo reproducir) y `requirements.txt`.

## 6. Riesgos / consideraciones
- `umap-learn`/`numba`/`shap` pueden dar problemas con Python 3.13 local; plan B: venv con 3.11/3.12 o validar en Colab.
- Pocos positivos (220): IC anchos; usar CV repetida y bootstrap; no sobre-interpretar diferencias pequeñas entre modelos.
- UMAP con `random_state` fijo es más lento pero reproducible; `transform` en test es aproximado.
- El informe no debe superar 10 páginas: priorizar 1–2 tablas y figuras clave por sección; el resto queda en el notebook.
- El video (10 min) y las preguntas individuales no están en el alcance acordado; el notebook explicado sirve de base para prepararlos.
