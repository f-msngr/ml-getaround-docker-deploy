# Prerequisites 

[🔙 Back to README](../README.md#table-of-contents)

# Table of Contents

## Bucket ☁️
Open your existing <AWS_S3_BUCKET> in your your AWS S3 manager (as $AWS_S3_BUCKET)  
(If you don't have any existing bucket, create one)  
Create new <PROJECT_NAME> folder in <AWS_S3_BUCKET> (will match $PROJECT_NAME in .env)  

```bash
# Edit and rename .env.example to .env to fit your configuration and credentials
mv .env.example .env
nano .env
# Set values 
#   - PROJECT_NAME
#   - AWS_REGION
#   - AWS_ACCESS_KEY
#   - AWS_SECRET_KEY
#   - AWS_S3_BUCKET
#   - ARTIFACT_ROOT
```

## Database setup 🗄️

Create New PostGRESQL Database (use of NeonDB here)  

<img src='../assets/screenshots/NeonDB_project_creation.png' alt='NeonDB_new_db_creation' width='300'>

```bash
# Set connection string to your new database given by the db manager console 
#   - BACKEND_STORE_URI=<CONNECTION_STRING_TO_THE_NEWLY_CREATED_DB>
```