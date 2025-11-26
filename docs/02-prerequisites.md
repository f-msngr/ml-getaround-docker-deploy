# Prerequisites ☁️

[🔙 Back to README](../README.md#table-of-contents)

# Table of Contents

- [Prerequisites ☁️](#prerequisites-️)
- [Table of Contents](#table-of-contents)
  - [Overview](#overview)
- [AWS S3 Bucket](#aws-s3-bucket)
- [PostgreSQL Database](#postgresql-database)
- [HuggingFace Account](#huggingface-account)
- [Environment Configuration](#environment-configuration)

## Overview

This project requires **external cloud resources** before you can run it locally or deploy it.

**What you need:**
- ☁️ **AWS S3 Bucket** - Dataset storage + MLflow artifact store
- 🗄️ **PostgreSQL Database** - MLflow metrics backend
- 🤗 **HuggingFace Account** - Deployment platform (optional for local dev)

[⬆ Back to top](#table-of-contents)

---
# AWS S3 Bucket

**Steps:**

1. **Create IAM User** (if not already done)
   - AWS Console → IAM → Users → Create user
   - Attach policy: `AmazonS3FullAccess`
   - Generate access keys → **Save them securely**

2. **Create S3 Bucket**
   - Open AWS S3 Console
   - Create bucket (or use existing one)
   - Note bucket name: `<YOUR_BUCKET_NAME>`

3. **Create Project Folder**
   - Inside your bucket, create folder: `<YOUR_PROJECT_NAME>/`
   - This will match `PROJECT_NAME` in `.env`

**Save these values** (needed later):
- `AWS_REGION` (e.g., `eu-west-1`)
- `AWS_ACCESS_KEY` (from IAM user)
- `AWS_SECRET_KEY` (from IAM user)
- `AWS_S3_BUCKET` (bucket name)
- `PROJECT_NAME` (folder name)

[⬆ Back to top](#table-of-contents)

---
# PostgreSQL Database

**Recommended:** [NeonDB](https://neon.tech) (free tier, serverless)

**Steps:**

1. **Create NeonDB Account**
   - Go to https://neon.tech
   - Sign up (GitHub OAuth recommended)

2. **Create Project**
   
   <img src='../assets/screenshots/NeonDB_project_creation.png' alt='NeonDB project creation' width='400'>

3. **Copy Connection String**
```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

**Save this value** (needed later):
- `BACKEND_STORE_URI` (connection string from step 3)

[⬆ Back to top](#table-of-contents)

---
# HuggingFace Account

**Required for:** Production deployment only (skip for local dev)

**Steps:**

1. **Create Account**
   - Go to https://huggingface.co/join

2. **No additional setup needed yet**
   - Spaces will be created during deployment
   - See [05-deployment.md](05-deployment.md) for details

[⬆ Back to top](#table-of-contents)

---
# Environment Configuration

**Now configure `.env` with all values collected above:**
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required variables:**
```bash
# Project
PROJECT_NAME=<YOUR_PROJECT_NAME>

# AWS S3
AWS_REGION=<YOUR_AWS_REGION>
AWS_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
AWS_SECRET_KEY=<YOUR_AWS_SECRET_KEY>
AWS_S3_BUCKET=<YOUR_AWS_S3_BUCKET>
ARTIFACT_ROOT=s3://<YOUR_AWS_S3_BUCKET>/<YOUR_PROJECT_NAME>/mlflow-artifacts/

# Database
BACKEND_STORE_URI=<YOUR_NEONDB_CONNECTION_STRING>

# Other variables
# Leave defaults for now, will be configured later if needed
```

**⚠️ Security:**
- Never commit `.env` to git
- `.env` is already in `.gitignore`

[⬆ Back to top](#table-of-contents)