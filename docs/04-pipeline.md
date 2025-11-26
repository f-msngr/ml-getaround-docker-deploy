# Pipeline 🔄

[🔙 Back to README](../README.md#table-of-contents)

# Table of Contents

- [Pipeline 🔄](#pipeline-)
- [Table of Contents](#table-of-contents)
  - [Philosophy](#philosophy)
  - [Quick Overview](#quick-overview)
  - [For GetAround Specifically](#for-getaround-specifically)
  - [API Integration](#api-integration)
  - [Quick Reference](#quick-reference)

## Philosophy

This pipeline is a **reusable ML deployment template**, not a showcase of advanced ML techniques. The focus is on **scalability and architecture**, not feature engineering.

**Key principle:** Stub framework + plug your own logic.

[⬆ Back to top](#table-of-contents)

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

[⬆ Back to top](#table-of-contents)

## For GetAround Specifically

**Datasets:**
- `df_rentals.pkl` - Raw rental data (delay analysis)
- `df_cars_transformed.pkl` - Cleaned car features (pricing model)

**ML Task:** Predict `rental_price_per_day` from car features
- Model: LinearRegression (simple baseline)
- Preprocessing: Imputer + Scaler + OneHotEncoder
- MLflow: Model registry + preprocessor artifacts

**One-time cleanup:** `notebooks/ETL.ipynb` (outlier removal, cardinality reduction)

[⬆ Back to top](#table-of-contents)

## API Integration

Pipeline functions are exposed via FastAPI routes following this pattern:
``` bash
pipeline/core/src/*.py (business logic)
    ↓
_fastapi-servers-shared/src/route_*.py (shared endpoints)
_fastapi-backend-server/src/route_*.py (backend-only endpoints)
    ↓
FastAPI servers (frontend uses shared, backend uses both)
```

**Separation of concerns:**
- **Shared routes** (`route_load`, `route_predict`) → Used by both servers
- **Backend routes** (`route_extract`, `route_transform`, `route_train`) → ETL/ML workflows

[⬆ Back to top](#table-of-contents)


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
