# Pipeline 🔄

[🔙 Back to README](../README.md#table-of-contents)

# Table of Contents

- [Pipeline 🔄](#pipeline-)
- [Table of Contents](#table-of-contents)
  - [Philosophy](#philosophy)
  - [Quick Overview](#quick-overview)
  - [For GetAround Specifically](#for-getaround-specifically)
  - [How to Adapt This Template](#how-to-adapt-this-template)
  - [Proof of Concept: Template Reusability](#proof-of-concept-template-reusability)
  - [Future Evolution (MLOps Vision)](#future-evolution-mlops-vision)
  - [Quick Reference](#quick-reference)

## Philosophy

This pipeline is a **reusable ML deployment template**, not a showcase of advanced ML techniques. The focus is on **scalability and architecture**, not feature engineering.

**Key principle:** Stub framework + plug your own logic.

---

## Quick Overview

```
S3 Bucket (datasets)
    ↓
load.py (data access layer)
    ↓
train.py (your model) → MLflow (tracking)
    ↓
predict.py (inference) → API → Dashboard
```

**What's real:**
- `load.py` - Data fetching from S3
- `train.py` - ML training + MLflow tracking
- `predict.py` - Model inference
- `libs/aws.py` - S3 utilities

**What's stub (extensible):**
- `extract.py` - TO BE REPLACED with your extraction logic
- `transform.py` - TO BE REPLACED with your transformations

---

## For GetAround Specifically

**Datasets:**
- `df_rentals.pkl` - Raw rental data (delay analysis)
- `df_cars_transformed.pkl` - Cleaned car features (pricing model)

**ML Task:** Predict `rental_price_per_day` from car features
- Model: LinearRegression (simple baseline)
- Preprocessing: Imputer + Scaler + OneHotEncoder
- MLflow: Model registry + preprocessor artifacts

**One-time cleanup:** `notebooks/ETL.ipynb` (outlier removal, cardinality reduction)

---

## How to Adapt This Template

1. **Replace datasets in S3:**
   ```bash
   s3://your-bucket/your-project/data/raw/your_data.pkl
   ```

2. **Modify `load.py`:**
   ```python
   def get_your_data():
       path_to_data = f'data/raw/your_data.pkl'
       return get_from_bucket(path_to_data)
   ```

3. **Update `train.py`:**
   - Change target/features
   - Swap LinearRegression for your model
   - Adjust preprocessing

4. **Update API routes:**
   - `_fastapi-servers-shared/src/route_load.py`
   - `_fastapi-servers-shared/src/route_predict.py`

5. **Redeploy:**
   ```bash
   make build
   make push SERVER=fe MSG="New project"
   ```

---

## Proof of Concept: Template Reusability

This architecture has been **successfully duplicated** on another project with minimal changes:
- Same Dockerfile structure
- Same Makefile orchestration
- Same deployment pipeline
- Different datasets + model

**Result:** 80% of code reused, 20% project-specific logic.

---

## Future Evolution (MLOps Vision)

Current structure is designed to integrate:

**Testing:** `pipeline/*/tests/` directories ready for pytest  
**CI/CD:** Jenkins integration planned  
**Orchestration:** Airflow DAGs for scheduled retraining  
**Monitoring:** MLflow metrics + alerting  

**Why this matters:**
- Clean separation of concerns (core vs libs)
- Dockerized services = easy CI/CD
- MLflow tracking = production-ready

---

## Quick Reference

| File | Purpose | When to modify |
|------|---------|----------------|
| `load.py` | Data access | New datasets |
| `train.py` | ML training | New model/features |
| `predict.py` | Inference | Model changes |
| `libs/aws.py` | S3 utilities | Never (generic) |
| `extract.py` | Stub | Replace with real ETL |
| `transform.py` | Stub | Replace with real transformations |

**Full code documentation:** See docstrings in each module.
