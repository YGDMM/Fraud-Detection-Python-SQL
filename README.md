# Fraud Detection Analysis using Python, SQL and Machine Learning

This project explores financial transaction data in order to identify suspicious behavior and analyze fraud-related patterns using:

- Python
- SQL
- Data visualization
- Rule-based detection
- Machine Learning

The project simulates part of a real fraud analysis workflow, beginning with exploratory analysis and evolving toward Machine Learning-based fraud detection.

---

# Project Objectives

- Analyze transaction behavior
- Detect suspicious patterns
- Explore fraud concentration trends
- Compare rule-based systems against Machine Learning
- Visualize fraud-related behaviors
- Build a basic fraud detection pipeline

---

# Techniques Used

## Exploratory Data Analysis (EDA)

- Dataset inspection
- Class imbalance analysis
- Transaction distribution analysis
- Fraud vs normal comparison

## Rule-Based Detection

Implemented several basic fraud detection rules:

- High transaction amount detection
- Small-value transaction detection
- Zero-amount detection
- Statistical anomaly detection (Z-Score)

## SQL Fraud Analysis

SQL queries were used to identify:

- repeated transaction amounts
- fraud concentration patterns
- suspicious low-value behavior
- comparative fraud vs normal distributions

## Data Visualization

Several visualizations were created using matplotlib:

- histograms
- comparative distributions
- fraud concentration graphs
- performance comparison charts
- confusion matrix visualization

## Machine Learning

A Random Forest classifier was implemented using scikit-learn.

The model was evaluated using:

- Precision
- Recall
- F1-Score
- Confusion Matrix
- Feature Importance analysis

---

# Key Findings

- Fraudulent transactions represented a very small percentage of the dataset.
- Fraud activity showed concentration around specific rounded transaction amounts.
- Rule-based systems showed limited effectiveness in detecting complex fraud behavior.
- Machine Learning significantly improved fraud detection capability.
- Certain anonymized variables played a major role in fraud classification.

---

# Project Structure

```text
Fraud-Analysis/

├── .venv/
├── data/
│   ├── transactions.csv
│   └── fraud.db
│
├── notebooks/
│   ├── analysis.py
│   └── randomforest.py
│
├── visuals/
│   ├── fraud_vs_normal_concentration.png
│   ├── ML_features.png
│   └── confusion_matrix.png
│   └── Rules vs ML
│
├── findings.md
├── requirements.txt
└── README.md
```

---

# Technologies Used

- Python
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- SQLite

---

# Future Improvements

Potential future developments include:

- behavioral fraud analysis
- time-series analysis
- real-time fraud detection
- feature engineering
- unsupervised anomaly detection
- graph/network analysis

---

# Disclaimer

This project was developed for educational and portfolio purposes only.

The dataset used contains anonymized financial transaction information.

---

# Author

Background:
- Criminology
- Cyber Investigation
- Fraud Analysis
- Intelligence & Security Studies
## 👤 Author

Focus: Fraud Analysis | Data Analysis | Cyber Investigation
