# %%PASO 1 Extrar los datos del csv y mostrar la informacion basica

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

df = pd.read_csv( "data/transactions.csv")

print("DATASET LOADED:")
print(df.head())
print("\nDATASET INFO:")
print(df.info())

# %%PASO 2 Mostrar la distribucion de clases en el dataset 
# cuantas transacciones son fraudulentas y cuantas no lo son

print("\nCLASS DISTRIBUTION:")
print(df["Class"].value_counts())

print("\nFRAUD PERCENTAGE:")
print(df["Class"].value_counts(normalize=True) * 100)

# %%PASO 3 Filtrado de datos

fraud_df = df[df["Class"] == 1]

# Filtrar solo las transacciones normales (Class = 0)
normal_df = df[df["Class"] == 0]

# Mostramos las primeras filas de fraude para ver cómo son
print("\nFRAUD TRANSACTIONS SAMPLE:")
print(fraud_df.head())

# Mostramos estadísticas básicas del importe en fraude
print("\nFRAUD AMOUNT STATS:")
print(fraud_df["Amount"].describe())

# %%PASO 4 Representaciones gráficas

def plot_normal():
  
# Histograma de transacciones normales
  
    plt.hist(normal_df["Amount"], bins=50)

    # Añadimos etiquetas claras
  
    plt.xlim(0, 5000)
    plt.ylim(0,10000)
    plt.title("Normal Transactions (Zoomed)")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Frequency")
  
# Mostramos
  
    plt.show()


def plot_fraud():
  
    # Histograma de transacciones fraudulentas
  
    plt.hist(fraud_df["Amount"], bins=50)

# Etiquetas
  
    plt.xlim(0, 2300)
    plt.ylim(0,300)
    plt.title("Fraud Transactions (Zoomed)")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Frequency")
  
# Mostramos
    plt.show() 

def plot_comparison():
  
# Histograma NORMAL usando densidad
  
    plt.hist(normal_df["Amount"], bins=50, density=True, alpha=0.5, label="Normal")

# Histograma FRAUDE usando densidad
  
    plt.hist(fraud_df["Amount"], bins=50, density=True, alpha=0.5, label="Fraud")

# Ajustamos rango para ver bien
  
    plt.xlim(0, 2300)

# Etiquetas claras
  
    plt.title("Fraud vs Normal (Normalized Distribution)")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Density")

# Leyenda
  
    plt.legend()

    plt.show()
  

# %%PASO 5 Crear reglas de deteccion de fraude

# Creamos una copia del dataset original
# Esto evita modificar accidentalmente el dataframe principal

df_rules = df.copy()

# ---------------------------------------------------
# REGLA 1 - TRANSACCIONES MUY ALTAS
# ---------------------------------------------------

# Calculamos el percentil 99 del importe
# Todo lo que esté por encima será considerado sospechoso

threshold = df_rules["Amount"].quantile(0.99)

# Creamos una nueva columna booleana
# True = sospechoso
# False = normal

df_rules["High_Amount_Flag"] = (
    df_rules["Amount"] > threshold
)

# ---------------------------------------------------
# REGLA 2 - TRANSACCIONES CON IMPORTE 0
# ---------------------------------------------------

# Las transacciones con valor 0 pueden ser anómalas

df_rules["Zero_Amount_Flag"] = (
    df_rules["Amount"] == 0
)

# ---------------------------------------------------
# REGLA 3 - TRANSACCIONES MUY PEQUEÑAS
# ---------------------------------------------------

# Cantidades extremadamente bajas
# pueden utilizarse para testear tarjetas robadas

df_rules["Small_Amount_Flag"] = (
    df_rules["Amount"] < 1
)

# ---------------------------------------------------
# COMBINAMOS LAS REGLAS
# ---------------------------------------------------

# Si una transacción cumple UNA de las reglas,
# Se marca como sospechosa

df_rules["Rule_Fraud"] = (

    df_rules["High_Amount_Flag"] |

    df_rules["Zero_Amount_Flag"] |

    df_rules["Small_Amount_Flag"]

)

# Convertimos True/False a 1/0

df_rules["Rule_Fraud"] = (
    df_rules["Rule_Fraud"].astype(int)
)

# ---------------------------------------------------
# RESULTADOS
# ---------------------------------------------------

print("\nRULE-BASED FRAUD DETECTION:")

print(df_rules["Rule_Fraud"].value_counts())


# %% PASO 5.1 - Detección estadística de anomalías

# ---------------------------------------------------
# CALCULAMOS MEDIA Y DESVIACIÓN TÍPICA
# ---------------------------------------------------

# Media del importe de transacciones

mean_amount = df_rules["Amount"].mean()

# Desviación típica:
# mide cuánto se alejan los valores de la media

std_amount = df_rules["Amount"].std()

# ---------------------------------------------------
# CREAMOS EL Z-SCORE
# ---------------------------------------------------

# El z-score indica:
# cuántas desviaciones típicas
# se aleja un valor respecto a la media

df_rules["Amount_Zscore"] = (

    (df_rules["Amount"] - mean_amount)

    / std_amount

)

# ---------------------------------------------------
# DETECTAMOS ANOMALÍAS
# ---------------------------------------------------

# Si el valor se aleja más de 3 desviaciones,
# suele considerarse anómalo

df_rules["Anomaly_Flag"] = (

    abs(df_rules["Amount_Zscore"]) > 3

)

# ---------------------------------------------------
# COMBINAMOS TODAS LAS REGLAS
# ---------------------------------------------------

df_rules["Rule_Fraud"] = (

    df_rules["High_Amount_Flag"] |

    df_rules["Zero_Amount_Flag"] |

    df_rules["Small_Amount_Flag"] |

    df_rules["Anomaly_Flag"]

)

# Convertimos True/False a 1/0

df_rules["Rule_Fraud"] = (
    df_rules["Rule_Fraud"].astype(int)
)

# ---------------------------------------------------
# RESULTADOS
# ---------------------------------------------------

print("\nANOMALY DETECTION RESULTS:")

print(df_rules["Rule_Fraud"].value_counts())


# %% PASO 6 Evaluar el rendimiento del detector de fraude

from sklearn.metrics import classification_report

print("\nEVALUATION OF RULES:")
print(classification_report(df_rules["Class"], df_rules["Rule_Fraud"]))


# %% PASO 7 EXPORTAR A SQL


# Creamos una base de datos llamada fraud.db

conn = sqlite3.connect("data/fraud.db")

# Exportamos el dataframe completo a una tabla SQL llamada "transactions"

df.to_sql("transactions", conn, if_exists="replace", index=False)

# Mensaje de confirmación

print("SQLite database created successfully!")

# %% PASO 8 SQL QUERIE PRUEBA

# Conectamos a la base de datos
conn = sqlite3.connect("data/fraud.db")

# Creamos una consulta SQL

query = """
SELECT Amount, Class
FROM transactions
WHERE Amount > 1000
"""

# Ejecutamos consulta SQL y guardamos resultado en pandas

high_amount_df = pd.read_sql(query, conn)

# Mostramos resultados

print("\nHIGH AMOUNT TRANSACTIONS:")

print(high_amount_df.head())

# %% PASO 8.1 - SQL QUERIES TOP TRANSACTIONS

# Consulta SQL:
# Obtener las 10 transacciones con mayor importe

query = """

SELECT Amount, Class

FROM transactions

ORDER BY Amount DESC

LIMIT 10

"""

# Ejecutamos consulta SQL y guardamos resultado

high_transactions = pd.read_sql(query, conn)

# Mostramos resultados

print("\nTOP 10 HIGHEST TRANSACTIONS:")

print(high_transactions)


# %% PASO 8.2 - SQL QUERIES  FRAUD VS NORMAL IMPORT RANGE

# Consulta SQL: 
query = """

SELECT

    CASE

        WHEN Amount < 10 THEN 'LOW'

        WHEN Amount BETWEEN 10 AND 100 THEN 'MEDIUM'

        WHEN Amount BETWEEN 100 AND 1000 THEN 'HIGH'

        ELSE 'VERY_HIGH'

    END AS Amount_Category,

    Class,

    COUNT(*) as Total_Transactions

FROM transactions

GROUP BY Amount_Category, Class

ORDER BY Amount_Category

"""

amount_analysis = pd.read_sql(query, conn)

print("\nFRAUD DISTRIBUTION BY AMOUNT CATEGORY:")

print(amount_analysis)


# %% PASO 8.3 - SQL QUERIES  FRAUD TRANSACTIONS LOW AMOUNT


# Consulta SQL:
query = """

SELECT

    COUNT(*) as Fraud_Count,

    AVG(Amount) as Average_Amount,

    MIN(Amount) as Min_Amount,

    MAX(Amount) as Max_Amount

FROM transactions

WHERE Class = 1

AND Amount < 10

"""

small_fraud = pd.read_sql(query, conn)

print("\nLOW-AMOUNT FRAUD ANALYSIS:")

print(small_fraud)


# %% PASO 8.4 - FRAUD REPETITION RATE


# Consulta SQL:

# Detectamos importes fraudulentos repetidos

# y calculamos cuántos casos representan del fraude total

query = """

WITH repeated_fraud AS (

    SELECT

        ROUND(Amount, 0) as Rounded_Amount,

        COUNT(*) as Frequency

    FROM transactions

    WHERE Class = 1

    GROUP BY Rounded_Amount

    HAVING COUNT(*) > 2

)

SELECT

    SUM(Frequency) as Total_Repeated_Fraud,

    (

        SELECT COUNT(*)

        FROM transactions

        WHERE Class = 1

    ) as Total_Fraud_Cases,

    ROUND(

        SUM(Frequency) * 100.0 /

        (

            SELECT COUNT(*)

            FROM transactions

            WHERE Class = 1

        ),

        2

    ) as Repetition_Percentage

FROM repeated_fraud

"""

# Ejecutamos consulta

fraud_repetition = pd.read_sql(query, conn)

# Mostramos resultados

print("\nFRAUD REPETITION ANALYSIS:")

print(fraud_repetition)


# %% PASO 8.5 - FRAUD VS NORMAL REPETITION COMPARISON


# Consulta SQL:

# Calculamos el porcentaje de repetición
# tanto para fraude como para transacciones normales

query = """

WITH repeated_transactions AS (

    SELECT

        Class,

        ROUND(Amount, 0) as Rounded_Amount,

        COUNT(*) as Frequency

    FROM transactions

    GROUP BY Class, Rounded_Amount

    HAVING COUNT(*) > 2

),

totals AS (

    SELECT

        Class,

        COUNT(*) as Total_Cases

    FROM transactions

    GROUP BY Class

)

SELECT

    r.Class,

    SUM(r.Frequency) as Repeated_Cases,

    t.Total_Cases,

    ROUND(

        SUM(r.Frequency) * 100.0 / t.Total_Cases,

        2

    ) as Repetition_Percentage

FROM repeated_transactions r

JOIN totals t

ON r.Class = t.Class

GROUP BY r.Class

ORDER BY r.Class

"""

# Ejecutamos consulta

comparison_df = pd.read_sql(query, conn)

# Mostramos resultados

print("\nFRAUD VS NORMAL REPETITION ANALYSIS:")

print(comparison_df)


# %% PASO 8.6 - FRAUD AMOUNT CONCENTRATION


# Consulta SQL:
# Calculamos qué porcentaje del fraude
# representa cada cantidad repetida

query = """

SELECT

    ROUND(Amount, 0) as Rounded_Amount,

    COUNT(*) as Frequency,

    ROUND(

        COUNT(*) * 100.0 /

        (SELECT COUNT(*) FROM transactions WHERE Class = 1),

        2

    ) as Fraud_Percentage

FROM transactions

WHERE Class = 1

GROUP BY Rounded_Amount

HAVING COUNT(*) > 2

ORDER BY Frequency DESC

LIMIT 15

"""

# Ejecutamos consulta

fraud_concentration = pd.read_sql(query, conn)

# Mostramos resultados

print("\nFRAUD AMOUNT CONCENTRATION:")

print(fraud_concentration)

# Cerramos conexión

conn.close()

# %% PASO 8.7 FRAUD VS NORMAL PERCENTAGE COMPARISON

conn = sqlite3.connect(
    "data/fraud.db")

query_fraud = """
SELECT
    ROUND(Amount, 0) AS Rounded_Amount,
    COUNT(*) AS Frequency,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions WHERE Class = 1), 4) AS Percentage
FROM transactions
WHERE Class = 1
GROUP BY Rounded_Amount
HAVING COUNT(*) > 2
ORDER BY Percentage DESC
LIMIT 10
"""

fraud_table = pd.read_sql(query_fraud, conn)

print("\n===== FRAUD TOP PATTERNS =====")
print(fraud_table)


conn = sqlite3.connect("data/fraud.db")

query_normal = """

SELECT

    ROUND(Amount, 0) AS Rounded_Amount,

    COUNT(*) AS Frequency,

    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions WHERE Class = 0), 4) AS Percentage

FROM transactions

WHERE Class = 0

GROUP BY Rounded_Amount

HAVING COUNT(*) > 1000

ORDER BY Percentage DESC

LIMIT 10

"""

normal_table = pd.read_sql(query_normal, conn)

print("\n===== NORMAL TOP PATTERNS =====")

print(normal_table)


# %% PASO 8.8 - GRÁFICO DE COMPARACIÓN

# =========================
# UNIMOS TABLAS EXISTENTES
# =========================

fraud_table["Type"] = "Fraud"
normal_table["Type"] = "Normal"

# Concatenamos ambas tablas

combined_table = pd.concat([fraud_table, normal_table])

# =========================
# ORDENAMOS POR IMPACTO
# =========================

# Queremos ver los patrones más relevantes globalmente

combined_table = combined_table.sort_values(
    by="Percentage",
    ascending=False
).reset_index(drop=True)

# =========================
# MOSTRAMOS RESULTADO FINAL
# =========================

print("\n===== FINAL COMPARISON: FRAUD vs NORMAL =====")
print(combined_table)



# %% PASO 8.9 - PROFESSIONAL COMPARISON GRAPH

# =========================
# Unimos cantidades únicas
# =========================

all_amounts = sorted(
    set(fraud_table["Rounded_Amount"]).union(
        set(normal_table["Rounded_Amount"])
    )
)

# =========================
# Creamos listas de porcentajes
# =========================

fraud_percentages = []
normal_percentages = []

for amount in all_amounts:

    # FRAUD
    fraud_match = fraud_table[
        fraud_table["Rounded_Amount"] == amount
    ]

    if not fraud_match.empty:
        fraud_percentages.append(
            fraud_match["Percentage"].values[0]
        )
    else:
        fraud_percentages.append(0)

    # NORMAL
    normal_match = normal_table[
        normal_table["Rounded_Amount"] == amount
    ]

    if not normal_match.empty:
        normal_percentages.append(
            normal_match["Percentage"].values[0]
        )
    else:
        normal_percentages.append(0)

# =========================
# Posiciones de barras
# =========================

x = np.arange(len(all_amounts))

width = 0.4

# =========================
# Creamos gráfico
# =========================

plt.figure(figsize=(14,6))

# Barras FRAUD

plt.bar(
    x - width/2,
    fraud_percentages,
    width,
    label="Fraud"
)

# Barras NORMAL

plt.bar(
    x + width/2,
    normal_percentages,
    width,
    label="Normal"
)

# =========================
# Etiquetas
# =========================

plt.title("Fraud vs Normal Transaction Concentration")

plt.xlabel("Rounded Transaction Amount")

plt.ylabel("Percentage Inside Each Class")

plt.xticks(x, all_amounts)

plt.legend()

plt.show()


#  %% PASO GENERAL - ejecución de Funciones

if __name__ == "__main__":
    plot_comparison()

