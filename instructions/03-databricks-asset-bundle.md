# LLM Instructions: Building Databricks App Asset Bundles

## Purpose
These instructions guide you to generate complete, production-ready Databricks Asset Bundle (DAB) configurations for deploying Databricks Apps. Use these guidelines to create well-structured, maintainable bundle configurations.

---

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Project Structure](#project-structure)
3. [Configuration File Requirements](#configuration-file-requirements)
4. [App Configuration Patterns](#app-configuration-patterns)
5. [Resource Integration](#resource-integration)
6. [Target Environments](#target-environments)
7. [Best Practices](#best-practices)
8. [Complete Examples](#complete-examples)
9. [Common Patterns](#common-patterns)
10. [Troubleshooting Guidelines](#troubleshooting-guidelines)

---

## 1. Core Concepts

### What is a Databricks Asset Bundle?
A Databricks Asset Bundle (DAB) is a declarative configuration system for deploying and managing Databricks resources including Apps, Jobs, Pipelines, Models, and more. It uses YAML configuration files to define infrastructure as code.

### Key Components
- **databricks.yml**: Main bundle configuration file (required, must be at root)
- **Resources**: Databricks objects (apps, jobs, clusters, etc.)
- **Targets**: Environment-specific configurations (dev, staging, prod)
- **Include**: Modular configuration files for better organization
- **Variables**: Reusable values across configurations
- **Workspace**: Settings for Databricks workspace connection

---

## 2. Project Structure

### Standard Directory Layout for Databricks Apps

```
project-root/
├── databricks.yml                 # Main bundle configuration (REQUIRED)
├── resources/                     # Resource definitions (RECOMMENDED)
│   ├── app.yml                   # App resource configuration
│   ├── job.yml                   # Job resource configuration
│   └── [other-resources].yml     # Additional resources
├── src/                          # Source code directory
│   └── app/                      # App-specific code
│       ├── app.py                # Main application file (Streamlit, Dash, Gradio, etc.)
│       ├── app.yaml              # App runtime configuration
│       ├── requirements.txt      # Python dependencies
│       └── tests/                # Unit tests
│           ├── __init__.py
│           └── test_app.py
├── .gitignore                    # Git ignore patterns
└── README.md                     # Documentation

```

### File Purposes

| File | Purpose | Required |
|------|---------|----------|
| `databricks.yml` | Main bundle entry point, defines bundle name, includes, and targets | YES |
| `resources/app.yml` | App resource definition with source code path and permissions | NO (but recommended) |
| `resources/job.yml` | Job definitions that app can interact with | NO |
| `src/app/app.py` | Application code (Streamlit, Dash, Gradio, etc.) | YES (for apps) |
| `src/app/app.yaml` | App runtime configuration (command, environment variables) | YES (for apps) |
| `src/app/requirements.txt` | Python package dependencies | YES (for Python apps) |

---

## 3. Configuration File Requirements

### 3.1 databricks.yml (Main Bundle File)

**MANDATORY FIELDS:**
```yaml
bundle:
  name: <unique-bundle-name>  # REQUIRED: Use lowercase, hyphens, no spaces
```

**STANDARD STRUCTURE:**
```yaml
bundle:
  name: <bundle-name>
  databricks_cli_version: <version-constraint>  # OPTIONAL: e.g., ">= 0.218.0"

include:
  - resources/*.yml  # Include all resource files

variables:
  <variable-name>:
    description: <description>
    default: <default-value>

workspace:
  root_path: <custom-root-path>  # OPTIONAL: Custom workspace path

permissions:  # OPTIONAL: Top-level permissions for all resources
  - level: CAN_VIEW
    group_name: <group-name>
  - level: CAN_MANAGE
    user_name: <user-email>

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: <workspace-url>
  
  prod:
    mode: production
    workspace:
      host: <workspace-url>
```

**KEY RULES:**
1. Must be named exactly `databricks.yml`
2. Must be at the root of the project
3. Must contain `bundle.name`
4. At least one target should have `default: true`
5. Use `include` to reference other YAML files

---

### 3.2 resources/app.yml (App Resource Definition)

**STRUCTURE:**
```yaml
resources:
  apps:
    <unique-app-identifier>:  # Must match bundle name or be unique
      name: "<display-name>"
      source_code_path: <relative-path-to-app-directory>  # e.g., ../src/app
      description: "<app-description>"
      
      # Optional: Reference other resources
      resources:
        - name: "<resource-identifier>"
          description: "<resource-description>"
          job:
            id: ${resources.jobs.<job-name>.id}  # Reference to job resource
            permission: "CAN_MANAGE_RUN"  # or "CAN_VIEW", "CAN_MANAGE"
        
        - name: "<another-resource>"
          description: "<description>"
          sql_warehouse:
            id: <warehouse-id>
            permission: "CAN_USE"
```

**KEY FIELDS:**

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `name` | Display name for the app | YES | `"My Streamlit App"` |
| `source_code_path` | Path to app source code directory | YES | `../src/app` |
| `description` | App description | NO | `"Dashboard for analytics"` |
| `resources` | List of Databricks resources the app can access | NO | See structure above |

**RESOURCE PERMISSIONS:**
- `CAN_VIEW`: Read-only access
- `CAN_MANAGE_RUN`: Can trigger runs
- `CAN_MANAGE`: Full management access
- `CAN_USE`: For SQL warehouses

---

### 3.3 src/app/app.yaml (App Runtime Configuration)

**STRUCTURE:**
```yaml
command:
  - <executable>     # e.g., streamlit, python, dash
  - <sub-command>    # e.g., run, -m
  - <entry-file>     # e.g., app.py, dash_app.py

env:
  - name: <ENV_VAR_NAME>
    value: <static-value>
  
  - name: <ENV_VAR_FROM_RESOURCE>
    valueFrom: <resource-name>  # References resource from app.yml
```

**FRAMEWORK-SPECIFIC COMMANDS:**

| Framework | Command Configuration |
|-----------|----------------------|
| **Streamlit** | `command: [streamlit, run, app.py]` |
| **Dash** | `command: [python, dash_app.py]` |
| **Gradio** | `command: [python, gradio_app.py]` |
| **Flask** | `command: [python, flask_app.py]` |
| **FastAPI** | `command: [uvicorn, main:app, --host, 0.0.0.0, --port, 8000]` |

**ENVIRONMENT VARIABLE PATTERNS:**

```yaml
env:
  # Static values
  - name: APP_TITLE
    value: "My Dashboard"
  
  # Reference job ID from resources
  - name: JOB_ID
    valueFrom: app-job  # Must match name in app.yml resources
  
  # Reference SQL warehouse
  - name: WAREHOUSE_ID
    valueFrom: analytics-warehouse
  
  # API endpoints
  - name: API_BASE_URL
    value: "https://api.example.com"
```

---

### 3.4 src/app/requirements.txt (Python Dependencies)

**STRUCTURE:**
```
# Core dependencies with pinned versions
<package>==<version>
<package>==<version>

# Framework (choose one or multiple)
streamlit==1.43.0
dash==2.14.0
gradio==4.0.0

# Databricks SDK (REQUIRED for most apps)
databricks-sdk==0.46.0

# Testing (RECOMMENDED)
pytest==8.3.5

# Common data/ML libraries
pandas==2.1.0
numpy==1.24.0
plotly==5.17.0
```

**REQUIRED PACKAGES FOR DATABRICKS APPS:**
- `databricks-sdk`: For interacting with Databricks APIs
- Web framework: `streamlit`, `dash`, `gradio`, etc.

**VERSION PINNING:**
- Always pin major.minor.patch versions for reproducibility
- Use `==` not `>=` for production deployments

---

## 4. App Configuration Patterns

### 4.1 Basic Streamlit App Pattern

**resources/app.yml:**
```yaml
resources:
  apps:
    my-streamlit-app:
      name: "My Streamlit App"
      source_code_path: ../src/app
      description: "A basic Streamlit dashboard"
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py
```

**src/app/app.py:**
```python
import streamlit as st
from databricks.sdk import WorkspaceClient

# Initialize Databricks client
w = WorkspaceClient(profile="Oauth")

st.title("My Streamlit App")
st.write("Connected to Databricks!")
```

---

### 4.2 App with Job Integration Pattern

**resources/app.yml:**
```yaml
resources:
  apps:
    job-trigger-app:
      name: "Job Trigger App"
      source_code_path: ../src/app
      description: "App that triggers Databricks jobs"
      
      resources:
        - name: "etl-job"
          description: "ETL job resource"
          job:
            id: ${resources.jobs.etl_pipeline.id}
            permission: "CAN_MANAGE_RUN"
```

**resources/job.yml:**
```yaml
resources:
  jobs:
    etl_pipeline:
      name: "ETL Pipeline Job"
      tasks:
        - task_key: extract_task
          spark_python_task:
            python_file: ../src/job/extract.py
          environment_key: default
      
      environments:
        - environment_key: default
          spec:
            client: "1"
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py

env:
  - name: JOB_ID
    valueFrom: etl-job  # Must match resource name in app.yml
```

**src/app/app.py:**
```python
import os
import streamlit as st
from databricks.sdk import WorkspaceClient

JOB_ID = os.getenv("JOB_ID")
w = WorkspaceClient(profile="Oauth")

st.title("Job Trigger Dashboard")

if st.button(f"Trigger ETL Job (ID: {JOB_ID})"):
    try:
        response = w.jobs.run_now(job_id=JOB_ID)
        st.success(f"Job started! Run ID: {response.run_id}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

---

### 4.3 App with SQL Warehouse Integration

**resources/app.yml:**
```yaml
resources:
  apps:
    analytics-dashboard:
      name: "Analytics Dashboard"
      source_code_path: ../src/app
      description: "Dashboard with SQL warehouse queries"
      
      resources:
        - name: "analytics-warehouse"
          description: "SQL warehouse for queries"
          sql_warehouse:
            id: "abc123def456"  # Your SQL warehouse ID
            permission: "CAN_USE"
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py

env:
  - name: WAREHOUSE_ID
    valueFrom: analytics-warehouse
  - name: CATALOG
    value: "main"
  - name: SCHEMA
    value: "analytics"
```

**src/app/app.py:**
```python
import os
import streamlit as st
from databricks.sdk import WorkspaceClient

WAREHOUSE_ID = os.getenv("WAREHOUSE_ID")
CATALOG = os.getenv("CATALOG")
SCHEMA = os.getenv("SCHEMA")

w = WorkspaceClient(profile="Oauth")

st.title("Analytics Dashboard")

query = f"SELECT * FROM {CATALOG}.{SCHEMA}.sales LIMIT 100"

if st.button("Run Query"):
    try:
        result = w.sql.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=query
        )
        st.dataframe(result.result.data_array)
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

---

### 4.4 Multi-Resource App Pattern

**resources/app.yml:**
```yaml
resources:
  apps:
    ml-operations-app:
      name: "ML Operations Dashboard"
      source_code_path: ../src/app
      description: "Comprehensive ML operations interface"
      
      resources:
        - name: "training-job"
          description: "Model training job"
          job:
            id: ${resources.jobs.model_training.id}
            permission: "CAN_MANAGE_RUN"
        
        - name: "inference-job"
          description: "Batch inference job"
          job:
            id: ${resources.jobs.batch_inference.id}
            permission: "CAN_MANAGE_RUN"
        
        - name: "warehouse"
          description: "Analytics SQL warehouse"
          sql_warehouse:
            id: "warehouse123"
            permission: "CAN_USE"
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py

env:
  - name: TRAINING_JOB_ID
    valueFrom: training-job
  - name: INFERENCE_JOB_ID
    valueFrom: inference-job
  - name: WAREHOUSE_ID
    valueFrom: warehouse
  - name: ENVIRONMENT
    value: "production"
```

---

## 5. Resource Integration

### 5.1 Jobs

**Define Job in resources/job.yml:**
```yaml
resources:
  jobs:
    data_processing:
      name: "Data Processing Job"
      tasks:
        - task_key: process_data
          spark_python_task:
            python_file: ../src/job/process.py
          environment_key: default
          
          # Optional: Job cluster configuration
          new_cluster:
            num_workers: 2
            spark_version: "13.3.x-scala2.12"
            node_type_id: "i3.xlarge"
      
      # Serverless environment (recommended)
      environments:
        - environment_key: default
          spec:
            client: "1"
      
      # Optional: Schedule
      schedule:
        quartz_cron_expression: "0 0 * * * ?"  # Daily at midnight
        timezone_id: "UTC"
```

**Reference in App:**
```yaml
resources:
  apps:
    my-app:
      resources:
        - name: "data-job"
          job:
            id: ${resources.jobs.data_processing.id}
            permission: "CAN_MANAGE_RUN"
```

---

### 5.2 Pipelines (Delta Live Tables)

**Define Pipeline:**
```yaml
resources:
  pipelines:
    etl_pipeline:
      name: "ETL Pipeline"
      target: "production"
      libraries:
        - notebook:
            path: ../src/pipeline/bronze_layer.py
        - notebook:
            path: ../src/pipeline/silver_layer.py
      
      clusters:
        - label: "default"
          num_workers: 2
```

**Reference in App:**
```yaml
resources:
  apps:
    pipeline-monitor:
      resources:
        - name: "etl-pipeline"
          pipeline:
            id: ${resources.pipelines.etl_pipeline.id}
            permission: "CAN_VIEW"
```

---

### 5.3 Model Serving Endpoints

**Define Model Serving Endpoint:**
```yaml
resources:
  model_serving_endpoints:
    prediction_service:
      name: "prediction-service"
      config:
        served_models:
          - model_name: "my_model"
            model_version: "1"
            workload_size: "Small"
            scale_to_zero_enabled: true
```

**Reference in App:**
```yaml
resources:
  apps:
    inference-app:
      resources:
        - name: "model-endpoint"
          serving_endpoint:
            id: ${resources.model_serving_endpoints.prediction_service.id}
            permission: "CAN_QUERY"
```

---

## 6. Target Environments

### 6.1 Development Target

**Purpose:** Local development, testing, frequent deployments

```yaml
targets:
  dev:
    mode: development  # IMPORTANT: Sets development-specific behaviors
    default: true      # Makes this the default target
    
    workspace:
      host: <dev-workspace-url>
      # Optional: Custom root path
      root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}
    
    # Development-specific resource overrides
    resources:
      apps:
        my-app:
          name: "dev-my-app"  # Add prefix for dev environment
      
      jobs:
        my-job:
          name: "dev-my-job"
          # Smaller clusters for dev
          tasks:
            - task_key: main
              new_cluster:
                num_workers: 1
```

**Development Mode Behaviors:**
- Allows cluster overrides via `cluster_id`
- More permissive deployment validation
- Suitable for rapid iteration

---

### 6.2 Production Target

**Purpose:** Production workloads, stable deployments, strict controls

```yaml
targets:
  prod:
    mode: production  # IMPORTANT: Enables production safeguards
    
    workspace:
      host: <prod-workspace-url>
      root_path: /Workspace/Shared/.bundle/${bundle.name}/${bundle.target}
    
    # Production-specific configurations
    presets:
      name_prefix: 'prod_'  # Prefix all resources
      tags:
        environment: production
        owner: data-team
      trigger_pause_status: UNPAUSED  # Ensure jobs are active
    
    # Strict permissions
    permissions:
      - level: CAN_MANAGE
        user_name: admin@company.com
      - level: CAN_VIEW
        group_name: data-analysts
    
    # Override resources for production
    resources:
      apps:
        my-app:
          name: "prod-my-app"
      
      jobs:
        my-job:
          # Larger clusters for production
          tasks:
            - task_key: main
              new_cluster:
                num_workers: 10
                node_type_id: "i3.2xlarge"
```

**Production Mode Behaviors:**
- Enforces stricter validation
- Requires explicit permissions
- Prevents accidental destructive operations
- Suitable for stable, managed workloads

---

### 6.3 Staging Target (Optional)

```yaml
targets:
  staging:
    mode: production  # Use production mode for staging
    
    workspace:
      host: <staging-workspace-url>
    
    presets:
      name_prefix: 'staging_'
      tags:
        environment: staging
    
    resources:
      apps:
        my-app:
          name: "staging-my-app"
```

---

### 6.4 Target-Specific Variables

```yaml
variables:
  warehouse_id:
    description: "SQL Warehouse ID"
    default: "dev-warehouse-123"

targets:
  dev:
    variables:
      warehouse_id: "dev-warehouse-123"
  
  prod:
    variables:
      warehouse_id: "prod-warehouse-456"
```

**Usage in app.yaml:**
```yaml
env:
  - name: WAREHOUSE_ID
    value: ${var.warehouse_id}
```

---

## 7. Best Practices

### 7.1 Naming Conventions

**Bundle Names:**
- Use lowercase with hyphens: `my-analytics-app`
- Be descriptive: `customer-segmentation-dashboard`
- Avoid spaces and special characters

**Resource Identifiers:**
- Use snake_case for resource keys: `etl_pipeline`, `training_job`
- Use descriptive names: `customer_data_job` not `job1`

**Display Names:**
- Use Title Case: `"Customer Analytics Dashboard"`
- Can include spaces and special characters

---

### 7.2 File Organization

**Modular Configuration:**
```yaml
# databricks.yml - Keep minimal
bundle:
  name: my-project
include:
  - resources/*.yml

# resources/app.yml - App definitions
resources:
  apps:
    ...

# resources/job.yml - Job definitions  
resources:
  jobs:
    ...

# resources/pipeline.yml - Pipeline definitions
resources:
  pipelines:
    ...
```

**Benefits:**
- Easier to maintain
- Better separation of concerns
- Enables team collaboration
- Reduces merge conflicts

---

### 7.3 Version Control

**What to Include:**
```
✅ databricks.yml
✅ resources/*.yml
✅ src/**/*.py
✅ src/**/requirements.txt
✅ src/**/app.yaml
✅ README.md
✅ .gitignore
```

**What to Exclude (.gitignore):**
```
❌ .databricks/
❌ __pycache__/
❌ *.pyc
❌ .venv/
❌ .env
❌ *.egg-info/
❌ dist/
```

---

### 7.4 Security Best Practices

**Never Hardcode Secrets:**
```yaml
# ❌ BAD - Never do this
env:
  - name: API_KEY
    value: "sk-1234567890abcdef"

# ✅ GOOD - Use Databricks Secrets
env:
  - name: API_KEY
    value: ${secrets.my_scope.api_key}
```

**Use Service Principals for Production:**
```yaml
targets:
  prod:
    workspace:
      host: <workspace-url>
      client_id: ${DATABRICKS_CLIENT_ID}  # From environment variable
    
    run_as:
      service_principal_name: "app-service-principal"
```

**Set Minimal Permissions:**
```yaml
resources:
  apps:
    my-app:
      resources:
        - name: "readonly-job"
          job:
            id: ${resources.jobs.report_job.id}
            permission: "CAN_VIEW"  # Not CAN_MANAGE if not needed
```

---

### 7.5 Testing

**Unit Tests:**
```python
# src/app/tests/test_app.py
import pytest
from databricks.sdk import WorkspaceClient

def test_workspace_connection():
    """Test Databricks workspace connectivity"""
    w = WorkspaceClient()
    current_user = w.current_user.me()
    assert current_user is not None

def test_job_trigger():
    """Test job triggering logic"""
    # Mock or use test job ID
    pass
```

**Local Testing:**
```bash
# Install dependencies
pip install -r src/app/requirements.txt

# Run tests
python -m pytest src/app/tests/

# Run app locally
streamlit run src/app/app.py
```

**Bundle Validation:**
```bash
# Validate configuration
databricks bundle validate -t dev

# Deploy to dev
databricks bundle deploy -t dev

# Run app
databricks bundle run my-app -t dev
```

---

### 7.6 Documentation

**README.md Template:**
```markdown
# Project Name

## Description
Brief description of what the app does.

## Prerequisites
- Databricks CLI >= 0.218.0
- Python >= 3.11
- Access to Databricks workspace

## Setup
1. Clone repository
2. Install dependencies: `pip install -r src/app/requirements.txt`
3. Configure workspace URLs in `databricks.yml`

## Deployment
### Development
\`\`\`bash
databricks bundle deploy -t dev
databricks bundle run my-app -t dev
\`\`\`

### Production
\`\`\`bash
databricks bundle deploy -t prod
databricks bundle run my-app -t prod
\`\`\`

## Configuration
- Update workspace URLs in `databricks.yml`
- Configure resource IDs in `resources/app.yml`

## Testing
\`\`\`bash
python -m pytest src/app/tests/
\`\`\`
```

---

## 8. Complete Examples

### 8.1 Simple Streamlit Dashboard

**Project Structure:**
```
simple-dashboard/
├── databricks.yml
├── resources/
│   └── app.yml
└── src/
    └── app/
        ├── app.py
        ├── app.yaml
        └── requirements.txt
```

**databricks.yml:**
```yaml
bundle:
  name: simple-dashboard

include:
  - resources/*.yml

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://your-workspace.cloud.databricks.com
```

**resources/app.yml:**
```yaml
resources:
  apps:
    simple-dashboard:
      name: "Simple Dashboard"
      source_code_path: ../src/app
      description: "A basic Streamlit dashboard"
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py
```

**src/app/app.py:**
```python
import streamlit as st
import pandas as pd

st.title("Simple Dashboard")

# Sample data
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 20, 30, 40]
})

st.bar_chart(data.set_index('Category'))
```

**src/app/requirements.txt:**
```
streamlit==1.43.0
pandas==2.1.0
```

---

### 8.2 Job Trigger App with Multiple Environments

**Project Structure:**
```
job-trigger-app/
├── databricks.yml
├── resources/
│   ├── app.yml
│   └── job.yml
└── src/
    ├── app/
    │   ├── app.py
    │   ├── app.yaml
    │   ├── requirements.txt
    │   └── tests/
    │       └── test_app.py
    └── job/
        └── main.py
```

**databricks.yml:**
```yaml
bundle:
  name: job-trigger-app
  databricks_cli_version: ">= 0.218.0"

include:
  - resources/*.yml

variables:
  environment:
    description: "Deployment environment"
    default: "development"

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://dev-workspace.cloud.databricks.com
    variables:
      environment: "development"
    resources:
      apps:
        job-trigger-app:
          name: "dev-job-trigger"
      jobs:
        data_pipeline:
          name: "dev-data-pipeline"
  
  prod:
    mode: production
    workspace:
      host: https://prod-workspace.cloud.databricks.com
      root_path: /Workspace/Shared/.bundle/${bundle.name}/${bundle.target}
    variables:
      environment: "production"
    permissions:
      - level: CAN_MANAGE
        user_name: admin@company.com
      - level: CAN_VIEW
        group_name: analysts
    presets:
      name_prefix: "prod_"
      tags:
        environment: production
        cost_center: engineering
```

**resources/app.yml:**
```yaml
resources:
  apps:
    job-trigger-app:
      name: "Job Trigger App"
      source_code_path: ../src/app
      description: "Trigger and monitor Databricks jobs"
      
      resources:
        - name: "pipeline-job"
          description: "Data pipeline job"
          job:
            id: ${resources.jobs.data_pipeline.id}
            permission: "CAN_MANAGE_RUN"
```

**resources/job.yml:**
```yaml
resources:
  jobs:
    data_pipeline:
      name: "Data Pipeline"
      tasks:
        - task_key: main_task
          spark_python_task:
            python_file: ../src/job/main.py
          environment_key: default
      
      environments:
        - environment_key: default
          spec:
            client: "1"
      
      email_notifications:
        on_failure:
          - data-team@company.com
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py

env:
  - name: JOB_ID
    valueFrom: pipeline-job
  - name: ENVIRONMENT
    value: ${var.environment}
```

**src/app/app.py:**
```python
import os
import streamlit as st
from databricks.sdk import WorkspaceClient
from datetime import datetime

JOB_ID = os.getenv("JOB_ID")
ENVIRONMENT = os.getenv("ENVIRONMENT", "unknown")

w = WorkspaceClient(profile="Oauth")

st.title("🚀 Job Trigger Dashboard")
st.caption(f"Environment: {ENVIRONMENT}")

# Job Information
st.subheader("Job Details")
try:
    job_info = w.jobs.get(job_id=JOB_ID)
    st.write(f"**Job Name:** {job_info.settings.name}")
    st.write(f"**Job ID:** {JOB_ID}")
except Exception as e:
    st.error(f"Error fetching job info: {str(e)}")

# Trigger Job
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Trigger Job", type="primary"):
        try:
            response = w.jobs.run_now(job_id=JOB_ID)
            st.success(f"✅ Job started successfully!")
            st.info(f"Run ID: {response.run_id}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Recent Runs
st.subheader("Recent Job Runs")
try:
    runs = w.jobs.list_runs(job_id=JOB_ID, limit=5)
    
    if runs:
        for run in runs:
            with st.expander(f"Run {run.run_id} - {run.state.life_cycle_state}"):
                st.write(f"**Status:** {run.state.result_state or 'Running'}")
                st.write(f"**Started:** {datetime.fromtimestamp(run.start_time/1000)}")
                if run.end_time:
                    st.write(f"**Ended:** {datetime.fromtimestamp(run.end_time/1000)}")
    else:
        st.info("No recent runs found")
        
except Exception as e:
    st.error(f"Error fetching runs: {str(e)}")
```

**src/app/requirements.txt:**
```
databricks-sdk==0.46.0
streamlit==1.43.0
pytest==8.3.5
```

**src/job/main.py:**
```python
from pyspark.sql import SparkSession
from datetime import datetime

def main():
    spark = SparkSession.builder.appName("DataPipeline").getOrCreate()
    
    # Sample ETL logic
    print(f"Job started at: {datetime.now()}")
    
    # Create sample DataFrame
    data = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
    df = spark.createDataFrame(data, ["id", "name"])
    
    print(f"Processed {df.count()} records")
    
    spark.stop()
    print("Job completed successfully")

if __name__ == "__main__":
    main()
```

---

### 8.3 Advanced ML Operations Dashboard

**Project Structure:**
```
ml-ops-dashboard/
├── databricks.yml
├── resources/
│   ├── app.yml
│   ├── jobs.yml
│   └── models.yml
└── src/
    ├── app/
    │   ├── app.py
    │   ├── app.yaml
    │   └── requirements.txt
    └── jobs/
        ├── training.py
        └── inference.py
```

**databricks.yml:**
```yaml
bundle:
  name: ml-ops-dashboard

include:
  - resources/*.yml

variables:
  model_name:
    description: "ML model name"
    default: "customer_churn_model"
  
  warehouse_id:
    description: "SQL Warehouse ID"
  
  catalog:
    description: "Unity Catalog name"
    default: "main"
  
  schema:
    description: "Schema name"
    default: "ml_models"

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://dev-workspace.cloud.databricks.com
    variables:
      warehouse_id: "dev-warehouse-123"
      catalog: "dev_catalog"
  
  prod:
    mode: production
    workspace:
      host: https://prod-workspace.cloud.databricks.com
    variables:
      warehouse_id: "prod-warehouse-456"
      catalog: "prod_catalog"
    presets:
      name_prefix: "prod_"
    run_as:
      service_principal_name: "ml-ops-service-principal"
```

**resources/app.yml:**
```yaml
resources:
  apps:
    ml-ops-dashboard:
      name: "ML Operations Dashboard"
      source_code_path: ../src/app
      description: "Comprehensive ML operations and monitoring"
      
      resources:
        - name: "training-job"
          description: "Model training job"
          job:
            id: ${resources.jobs.model_training.id}
            permission: "CAN_MANAGE_RUN"
        
        - name: "inference-job"
          description: "Batch inference job"
          job:
            id: ${resources.jobs.batch_inference.id}
            permission: "CAN_MANAGE_RUN"
        
        - name: "analytics-warehouse"
          description: "SQL Warehouse for analytics"
          sql_warehouse:
            id: ${var.warehouse_id}
            permission: "CAN_USE"
```

**resources/jobs.yml:**
```yaml
resources:
  jobs:
    model_training:
      name: "Model Training Pipeline"
      tasks:
        - task_key: prepare_data
          spark_python_task:
            python_file: ../src/jobs/training.py
            parameters:
              - "--stage"
              - "prepare"
          environment_key: default
        
        - task_key: train_model
          depends_on:
            - task_key: prepare_data
          spark_python_task:
            python_file: ../src/jobs/training.py
            parameters:
              - "--stage"
              - "train"
          environment_key: default
      
      environments:
        - environment_key: default
          spec:
            client: "1"
      
      schedule:
        quartz_cron_expression: "0 0 2 * * ?"  # Daily at 2 AM
        timezone_id: "UTC"
    
    batch_inference:
      name: "Batch Inference Pipeline"
      tasks:
        - task_key: inference
          spark_python_task:
            python_file: ../src/jobs/inference.py
          environment_key: default
      
      environments:
        - environment_key: default
          spec:
            client: "1"
```

**src/app/app.yaml:**
```yaml
command:
  - streamlit
  - run
  - app.py
  - --server.port
  - "8000"

env:
  - name: TRAINING_JOB_ID
    valueFrom: training-job
  - name: INFERENCE_JOB_ID
    valueFrom: inference-job
  - name: WAREHOUSE_ID
    valueFrom: analytics-warehouse
  - name: MODEL_NAME
    value: ${var.model_name}
  - name: CATALOG
    value: ${var.catalog}
  - name: SCHEMA
    value: ${var.schema}
```

**src/app/app.py:**
```python
import os
import streamlit as st
from databricks.sdk import WorkspaceClient
from datetime import datetime
import pandas as pd

# Configuration
TRAINING_JOB_ID = os.getenv("TRAINING_JOB_ID")
INFERENCE_JOB_ID = os.getenv("INFERENCE_JOB_ID")
WAREHOUSE_ID = os.getenv("WAREHOUSE_ID")
MODEL_NAME = os.getenv("MODEL_NAME")
CATALOG = os.getenv("CATALOG")
SCHEMA = os.getenv("SCHEMA")

# Initialize client
w = WorkspaceClient(profile="Oauth")

# Page config
st.set_page_config(
    page_title="ML Operations Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ML Operations Dashboard")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Configuration")
    st.write(f"**Model:** {MODEL_NAME}")
    st.write(f"**Catalog:** {CATALOG}.{SCHEMA}")
    st.write(f"**Warehouse ID:** {WAREHOUSE_ID}")
    
    st.divider()
    st.header("Quick Actions")
    
    if st.button("🔄 Train Model", type="primary", use_container_width=True):
        try:
            response = w.jobs.run_now(job_id=TRAINING_JOB_ID)
            st.success(f"Training started! Run ID: {response.run_id}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if st.button("🚀 Run Inference", type="secondary", use_container_width=True):
        try:
            response = w.jobs.run_now(job_id=INFERENCE_JOB_ID)
            st.success(f"Inference started! Run ID: {response.run_id}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Model Metrics", "🔄 Job Runs", "📈 Predictions"])

with tab1:
    st.subheader("Model Performance Metrics")
    
    # Query model metrics from Unity Catalog
    query = f"""
    SELECT 
        model_version,
        accuracy,
        precision,
        recall,
        f1_score,
        training_date
    FROM {CATALOG}.{SCHEMA}.model_metrics
    WHERE model_name = '{MODEL_NAME}'
    ORDER BY training_date DESC
    LIMIT 10
    """
    
    try:
        result = w.sql.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=query,
            wait_timeout="30s"
        )
        
        if result.result and result.result.data_array:
            df = pd.DataFrame(
                result.result.data_array,
                columns=[col.name for col in result.manifest.schema.columns]
            )
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df.set_index('model_version')['accuracy'])
            with col2:
                st.line_chart(df.set_index('model_version')['f1_score'])
        else:
            st.info("No metrics available yet")
    except Exception as e:
        st.error(f"Error fetching metrics: {str(e)}")

with tab2:
    st.subheader("Recent Job Runs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Training Jobs**")
        try:
            training_runs = w.jobs.list_runs(job_id=TRAINING_JOB_ID, limit=5)
            for run in training_runs:
                status_emoji = "✅" if run.state.result_state == "SUCCESS" else "❌"
                with st.expander(f"{status_emoji} Run {run.run_id}"):
                    st.write(f"Status: {run.state.result_state or 'Running'}")
                    st.write(f"Started: {datetime.fromtimestamp(run.start_time/1000)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with col2:
        st.write("**Inference Jobs**")
        try:
            inference_runs = w.jobs.list_runs(job_id=INFERENCE_JOB_ID, limit=5)
            for run in inference_runs:
                status_emoji = "✅" if run.state.result_state == "SUCCESS" else "❌"
                with st.expander(f"{status_emoji} Run {run.run_id}"):
                    st.write(f"Status: {run.state.result_state or 'Running'}")
                    st.write(f"Started: {datetime.fromtimestamp(run.start_time/1000)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab3:
    st.subheader("Recent Predictions")
    
    query = f"""
    SELECT 
        prediction_id,
        customer_id,
        churn_probability,
        prediction_date
    FROM {CATALOG}.{SCHEMA}.predictions
    ORDER BY prediction_date DESC
    LIMIT 100
    """
    
    try:
        result = w.sql.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=query,
            wait_timeout="30s"
        )
        
        if result.result and result.result.data_array:
            df = pd.DataFrame(
                result.result.data_array,
                columns=[col.name for col in result.manifest.schema.columns]
            )
            st.dataframe(df, use_container_width=True)
            
            # Distribution
            st.bar_chart(df['churn_probability'].value_counts())
        else:
            st.info("No predictions available yet")
    except Exception as e:
        st.error(f"Error fetching predictions: {str(e)}")
```

**src/app/requirements.txt:**
```
databricks-sdk==0.46.0
streamlit==1.43.0
pandas==2.1.0
plotly==5.17.0
```

---

## 9. Common Patterns

### 9.1 Environment Variables from Resources

**Pattern:** Pass resource IDs to app as environment variables

```yaml
# app.yml
resources:
  apps:
    my-app:
      resources:
        - name: "my-resource"
          job:
            id: ${resources.jobs.my_job.id}
            permission: "CAN_MANAGE_RUN"

# app.yaml
env:
  - name: RESOURCE_ID
    valueFrom: my-resource  # Must match name above
```

---

### 9.2 Cross-Environment Configuration

**Pattern:** Use variables for environment-specific values

```yaml
variables:
  cluster_size:
    description: "Cluster worker count"

targets:
  dev:
    variables:
      cluster_size: 1
  
  prod:
    variables:
      cluster_size: 10

resources:
  jobs:
    my-job:
      tasks:
        - task_key: main
          new_cluster:
            num_workers: ${var.cluster_size}
```

---

### 9.3 Substitution References

**Common substitutions:**

| Substitution | Description | Example Value |
|--------------|-------------|---------------|
| `${bundle.name}` | Bundle name | `my-app` |
| `${bundle.target}` | Target name | `dev`, `prod` |
| `${workspace.current_user.userName}` | Current user | `user@company.com` |
| `${workspace.root}` | Workspace root path | `/Workspace/Users/...` |
| `${var.variable_name}` | Custom variable | User-defined |
| `${resources.jobs.job_name.id}` | Job resource ID | `123456789` |

---

### 9.4 Resource Dependencies

**Pattern:** Reference other resources

```yaml
resources:
  jobs:
    upstream_job:
      name: "Upstream Job"
      tasks:
        - task_key: main
          spark_python_task:
            python_file: ../src/upstream.py
  
  jobs:
    downstream_job:
      name: "Downstream Job"
      tasks:
        - task_key: main
          spark_python_task:
            python_file: ../src/downstream.py
          depends_on:
            - task_key: ${resources.jobs.upstream_job.tasks[0].task_key}
```

---

### 9.5 Conditional Resource Configuration

**Pattern:** Override resources per target

```yaml
resources:
  apps:
    my-app:
      name: "My App"
      source_code_path: ../src/app

targets:
  dev:
    resources:
      apps:
        my-app:
          name: "dev-my-app"  # Override for dev
          # Inherits source_code_path from base
  
  prod:
    resources:
      apps:
        my-app:
          name: "prod-my-app"  # Override for prod
```

---

## 10. Troubleshooting Guidelines

### 10.1 Common Errors

**Error: "Bundle name is required"**
```yaml
# ❌ Missing bundle name
bundle: {}

# ✅ Correct
bundle:
  name: my-bundle
```

**Error: "No default target specified"**
```yaml
# ❌ No default target
targets:
  dev: {}
  prod: {}

# ✅ Set one as default
targets:
  dev:
    default: true
  prod: {}
```

**Error: "Source code path not found"**
```yaml
# ❌ Incorrect path
resources:
  apps:
    my-app:
      source_code_path: src/app  # Missing ../

# ✅ Correct relative path
resources:
  apps:
    my-app:
      source_code_path: ../src/app
```

---

### 10.2 Validation Commands

```bash
# Validate bundle configuration
databricks bundle validate

# Validate specific target
databricks bundle validate -t prod

# Show computed configuration
databricks bundle validate --var="key=value"

# Dry run deployment
databricks bundle deploy --dry-run
```

---

### 10.3 Debugging Tips

**1. Check bundle structure:**
```bash
databricks bundle schema
```

**2. Inspect computed configuration:**
```bash
databricks bundle validate -t dev --output json
```

**3. Verify resource references:**
```yaml
# Use explicit IDs first to test connectivity
resources:
  apps:
    my-app:
      resources:
        - name: "test-job"
          job:
            id: "12345"  # Hardcode temporarily
            permission: "CAN_VIEW"
```

**4. Test locally first:**
```bash
# Run app locally
streamlit run src/app/app.py

# Run unit tests
python -m pytest src/app/tests/
```

---

### 10.4 Common Pitfalls

**1. Path Issues:**
- All paths in resource files are relative to that file
- Use `../` to go up from resources/ to src/
- Workspace paths must start with `/Workspace` or `/Volumes`

**2. Resource Name Mismatches:**
```yaml
# app.yml
resources:
  - name: "my-job-resource"  # Name here
    job:
      id: ${resources.jobs.my_job.id}

# app.yaml
env:
  - name: JOB_ID
    valueFrom: my-job-resource  # Must match exactly
```

**3. Missing Permissions:**
```yaml
# ✅ Always specify minimum required permission
resources:
  apps:
    my-app:
      resources:
        - name: "job"
          job:
            id: ${resources.jobs.my_job.id}
            permission: "CAN_MANAGE_RUN"  # Don't forget this!
```

**4. Target Mode Confusion:**
```yaml
# ❌ Using development features in production
targets:
  prod:
    mode: development  # Wrong!

# ✅ Correct
targets:
  prod:
    mode: production
```

---

## Summary Checklist

When generating a Databricks App Asset Bundle, ensure:

- [ ] `databricks.yml` exists at root with `bundle.name`
- [ ] At least one target defined with `default: true`
- [ ] `include` section references resource files
- [ ] `resources/app.yml` defines app with correct `source_code_path`
- [ ] `src/app/app.py` contains application code
- [ ] `src/app/app.yaml` defines command and env variables
- [ ] `src/app/requirements.txt` lists all dependencies
- [ ] Resource references use correct substitution syntax
- [ ] Environment variables in app.yaml match resource names in app.yml
- [ ] Permissions specified for all resource access
- [ ] Development and production targets configured appropriately
- [ ] Paths are relative and correct
- [ ] No secrets hardcoded in configuration
- [ ] README.md provides deployment instructions

---

## Additional Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/)
- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/)
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html)
- [Bundle Examples Repository](https://github.com/databricks/bundle-examples)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## Quick Reference Card

### Essential Commands
```bash
# Validate
databricks bundle validate

# Deploy
databricks bundle deploy -t <target>

# Run app
databricks bundle run <app-name> -t <target>

# Destroy
databricks bundle destroy -t <target>
```

### Minimal Bundle Structure
```yaml
bundle:
  name: app-name

include:
  - resources/*.yml

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: <workspace-url>
```

### Minimal App Resource
```yaml
resources:
  apps:
    app-name:
      name: "Display Name"
      source_code_path: ../src/app
```

### Minimal App Runtime
```yaml
command:
  - streamlit
  - run
  - app.py
```

---

**End of Instructions**

Use these guidelines to generate complete, production-ready Databricks Asset Bundle configurations for Databricks Apps. Follow the patterns, best practices, and examples to ensure robust, maintainable infrastructure as code.
