# ==========================================
# PHASE 4 - MACHINE LEARNING (RANDOM FOREST)
# ==========================================

# %% IMPORTS

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report

# %% LOAD DATASET

df = pd.read_csv(
    "/Users/maxandpower/Proyectos/Fraud Analysis/data/transactions.csv"
)

print("DATASET LOADED")
print(df.head())

# %% FEATURES AND TARGET

# X = variables de entrada
# y = variable objetivo (fraude o no fraude)

X = df.drop("Class", axis=1)

y = df["Class"]

print("\nFEATURES:")
print(X.columns)

print("\nTARGET:")
print(y.head())

# %% TRAIN / TEST SPLIT

# 80% entrenamiento
# 20% test

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)

print("\nTRAINING DATA:", X_train.shape)

print("TEST DATA:", X_test.shape)


# %% RANDOM FOREST MODEL

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)

# Entrenamos modelo

model.fit(X_train, y_train)

print("\nMODEL TRAINED SUCCESSFULLY")


# %% PREDICTIONS

y_pred = model.predict(X_test)

print("\nPREDICTIONS COMPLETED")

# %% PREDICTIONS

y_pred = model.predict(X_test)

print("\nPREDICTIONS COMPLETED")

# %% EVALUATION

print("\nMODEL EVALUATION:")

print(classification_report(y_test, y_pred))

# %% CONFUSION MATRIX

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# MATRIZ DE CONFUSIÓN
# =========================

cm = confusion_matrix(y_test, y_pred)

# =========================
# MOSTRAMOS MATRIZ
# =========================

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

# Etiquetas

plt.title("Fraud Detection Confusion Matrix")

plt.xlabel("Predicted Label")

plt.ylabel("True Label")

plt.show()


FEATURE IMPORTANCE

import pandas as pd
import matplotlib.pyplot as plt

# =========================
# IMPORTANCIA DE VARIABLES
# =========================

importance = model.feature_importances_

# Creamos dataframe

feature_importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": importance

})

# Ordenamos de mayor a menor

feature_importance = feature_importance.sort_values(

    by="Importance",

    ascending=False

)

# =========================
# MOSTRAMOS TOP VARIABLES
# =========================

print("\nTOP IMPORTANT FEATURES:")

print(feature_importance.head(10))

# =========================
# GRÁFICO
# =========================

top_features = feature_importance.head(10)

plt.figure(figsize=(10,6))

plt.barh(

    top_features["Feature"],

    top_features["Importance"]

)

plt.title("Top 10 Most Important Features")

plt.xlabel("Importance")

plt.ylabel("Feature")

plt.gca().invert_yaxis()

plt.show()

# %% RULES VS ML COMPARISON

import pandas as pd

# =========================
# RESULTADOS REGLAS
# =========================

rules_precision = 0.00
rules_recall = 0.16
rules_f1 = 0.01

# =========================
# RESULTADOS RANDOM FOREST
# =========================

ml_precision = 0.94
ml_recall = 0.82
ml_f1 = 0.87

# =========================
# CREAMOS TABLA
# =========================

comparison_table = pd.DataFrame({

    "Metric": [

        "Precision",

        "Recall",

        "F1-Score"

    ],

    "Rule_Based_System": [

        rules_precision,

        rules_recall,

        rules_f1

    ],

    "Random_Forest": [

        ml_precision,

        ml_recall,

        ml_f1

    ]

})

# =========================
# MOSTRAMOS RESULTADO
# =========================

print("\nRULES VS MACHINE LEARNING")

print(comparison_table)


# %% PERFORMANCE COMPARISON GRAPH

import matplotlib.pyplot as plt
import numpy as np

# =========================
# DATOS
# =========================

metrics = [

    "Precision",

    "Recall",

    "F1-Score"

]

rules_scores = [

    rules_precision,

    rules_recall,

    rules_f1

]

ml_scores = [

    ml_precision,

    ml_recall,

    ml_f1

]

# =========================
# POSICIONES
# =========================

x = np.arange(len(metrics))

width = 0.35

# =========================
# GRÁFICO
# =========================

plt.figure(figsize=(10,6))

plt.bar(

    x - width/2,

    rules_scores,

    width,

    label="Rule-Based"

)

plt.bar(

    x + width/2,

    ml_scores,

    width,

    label="Random Forest"

)

# =========================
# ETIQUETAS
# =========================

plt.xticks(x, metrics)

plt.ylabel("Score")

plt.title("Rules vs Machine Learning Performance")

plt.legend()

plt.ylim(0,1)

plt.show()
