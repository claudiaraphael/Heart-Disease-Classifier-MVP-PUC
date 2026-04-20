# Heart Disease Classifier — MVP

A machine learning-powered web application for predicting cardiac disease risk based on clinical patient data. Built as an MVP for the **Intelligent Systems** sprint at PUC-Rio.

- **Dataset source:** [Heart Disease Dataset — Kaggle](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)

---

## Overview

The system allows a user to input a patient's clinical data through a web form and receive an immediate binary prediction — **low risk** or **high risk** — produced by a trained Support Vector Machine (SVM) model. Predictions and patient records are persisted in a local SQLite database.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Backend | Python 3, Flask, Flask-CORS, Flask-OpenAPI3, SQLAlchemy |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Machine Learning | scikit-learn (SVM pipeline), pandas, numpy |
| Database | SQLite 3 |
| Testing | pytest |
| Experimentation | Jupyter Notebook |

---

## Project Structure

```
MVP oficial/
├── api/
│   ├── app.py                    # Flask application and routes
│   ├── logger.py                 # Rotating file logger setup
│   ├── requirements.txt          # Python dependencies
│   ├── test_api.py               # API endpoint tests (pytest)
│   ├── test_modelos.py           # ML model accuracy test (pytest)
│   ├── model/
│   │   ├── paciente.py           # Patient SQLAlchemy ORM model
│   │   ├── pipeline.py           # Loads trained .pkl pipeline
│   │   ├── preprocessador.py     # Data preprocessing helpers
│   │   ├── carregador.py         # CSV dataset loader
│   │   └── avaliador.py          # Model evaluation utilities
│   ├── schemas/
│   │   ├── paciente_schema.py    # Pydantic request/response schemas
│   │   └── error_schema.py       # Error response schema
│   ├── MachineLearning/
│   │   ├── notebooks/
│   │   │   └── heart_disease_classification.ipynb
│   │   ├── data/
│   │   │   ├── heart.csv
│   │   │   ├── X_test_heart_disease.csv
│   │   │   └── y_test_heart_disease.csv
│   │   └── pipelines/
│   │       └── svm_heart_disease_pipeline.pkl
│   └── database/
│       └── pacientes.sqlite3     # Auto-created on first run
└── front/
    ├── index.html
    ├── styles.css
    └── scripts.js
```

---

## Machine Learning Model

### Dataset

- **Source:** UCI Heart Disease dataset (combined Cleveland, Hungary, Switzerland, Long Beach VA)
- **Samples:** 1,025 patients
- **Features:** 13 clinical features (numeric)
- **Target:** Binary — `0` (no disease) / `1` (disease)
- **Class balance:** ~51% disease / ~49% no disease

### Clinical Features

| Feature | Description |
|---|---|
| `age` | Age in years |
| `sex` | 1 = Male, 0 = Female |
| `cp` | Chest pain type (0–3) |
| `trestbps` | Resting blood pressure (mmHg) |
| `chol` | Serum cholesterol (mg/dl) |
| `fbs` | Fasting blood sugar > 120 mg/dl (1 = yes) |
| `restecg` | Resting ECG results (0–2) |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise-induced angina (1 = yes) |
| `oldpeak` | ST depression induced by exercise |
| `slope` | Slope of peak exercise ST segment (0–2) |
| `ca` | Number of major vessels colored by fluoroscopy (0–3) |
| `thal` | Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect) |

### Model Selection

Four algorithms were evaluated with three scaling strategies (no scaling, StandardScaler, MinMaxScaler) using 10-fold stratified cross-validation:

| Algorithm | Best CV Accuracy |
|---|---|
| K-Nearest Neighbors | ~95% |
| Decision Tree | ~83% |
| Naive Bayes | ~85% |
| **SVM (RBF kernel)** | **97.56%** |

**Chosen model:** SVM with `C=100`, `gamma=0.1`, `kernel='rbf'`, scaled with `StandardScaler`.

- Cross-validation accuracy: **97.56%**
- Test set accuracy (205 samples): **100%**

The full training process, EDA, hyperparameter search, and model export are documented in [api/MachineLearning/notebooks/heart_disease_classification.ipynb](api/MachineLearning/notebooks/heart_disease_classification.ipynb).

---

## API

**Base URL:** `http://127.0.0.1:5000`

Interactive documentation (Swagger / ReDoc) is available at `http://127.0.0.1:5000/openapi`.

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Redirects to the frontend |
| `GET` | `/pacientes` | Returns all stored patients |
| `POST` | `/paciente` | Adds a patient and returns the ML prediction |
| `GET` | `/paciente?name=<name>` | Retrieves a patient by name |
| `DELETE` | `/paciente?name=<name>` | Deletes a patient by name |

### Example POST `/paciente`

**Request body:**
```json
{
  "name": "John Doe",
  "age": 52,
  "sex": 1,
  "cp": 0,
  "trestbps": 125,
  "chol": 212,
  "fbs": 0,
  "restecg": 1,
  "thalach": 168,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": 2,
  "ca": 2,
  "thal": 3
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 52,
  "sex": 1,
  "cp": 0,
  "trestbps": 125,
  "chol": 212,
  "fbs": 0,
  "restecg": 1,
  "thalach": 168,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": 2,
  "ca": 2,
  "thal": 3,
  "outcome": 1
}
```

`outcome`: `0` = low risk, `1` = high risk.

---

## Frontend

A single-page web interface built with vanilla HTML/CSS/JS, served directly by Flask at `http://127.0.0.1:5000/`.

**Features:**
- Form with all 13 clinical inputs for a new patient
- Immediate risk prediction result card (low / high risk)
- Patient history table with color-coded risk badges
- Dark / Light theme toggle

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Navigate to the api folder
cd api

# Create and activate a virtual environment
python -m venv .venv

# On Windows
.venv\Scripts\activate
# On macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running

```bash
# From the api/ directory with the virtual environment active
python app.py
```

The application will be available at:
- **Frontend:** http://127.0.0.1:5000/
- **API docs:** http://127.0.0.1:5000/openapi

The SQLite database is created automatically on first run at `api/database/pacientes.sqlite3`.

---

## Running Tests

All tests must be run from inside the `api/` directory.

```bash
cd api/

# Run all tests
pytest -v

# Run only API endpoint tests
pytest -v test_api.py

# Run only ML model accuracy test
pytest -v test_modelos.py
```

The model test asserts that the SVM pipeline achieves at least **80% accuracy** on the 205-sample holdout test set.

---

## Disclaimer

This tool is for educational and research purposes only. It is **not** a substitute for professional medical diagnosis. Always consult a qualified healthcare provider for any health concerns.
