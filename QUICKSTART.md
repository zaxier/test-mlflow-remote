# Quick Start Guide

Get up and running with Databricks MLflow from your local IDE in 5 minutes!

## Step 1: Install uv (30 sec)

If you don't have `uv` installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Step 2: Install Dependencies (1 min)

```bash
# This creates a virtual environment and installs all dependencies
uv sync
```

## Step 3: Authenticate with Databricks (1 min)

```bash
databricks auth login --profile my-workspace
```

This will:
- Open your browser for OAuth authentication
- Create `~/.databrickscfg` with your credentials
- Cache your token at `~/.databricks/token-cache.json`

## Step 4: Configure Environment (1 min)

Copy `env.example` to `.env` and update:

```bash
cp env.example .env
```

Edit `.env`:
```bash
DATABRICKS_PROFILE="my-workspace"  # Match the profile name from Step 2
MLFLOW_TRACKING_URI="databricks://my-workspace"
MLFLOW_REGISTRY_URI="databricks-uc"  # For Unity Catalog
```

Or export directly in your terminal:

```bash
export DATABRICKS_PROFILE="my-workspace"
export MLFLOW_TRACKING_URI="databricks://my-workspace"
export MLFLOW_REGISTRY_URI="databricks-uc"
```

## Step 5: Run the Test (1 min)

```bash
# Using uv (automatically uses the project's virtual environment)
uv run python test_mlflow_remote.py

# Or activate the virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python test_mlflow_remote.py
```

This will test:
- ✅ Creating and tracking MLflow experiments
- ✅ Logging runs with parameters and metrics
- ✅ Registering models to Unity Catalog

## What You'll See

```
======================================================================
TESTING MANAGED MLFLOW ON DATABRICKS FROM LOCAL IDE
======================================================================

CONFIGURATION CHECK
----------------------------------------------------------------------
✓ All configuration validated

TEST 1: CREATE AND TRACK MLFLOW EXPERIMENT
----------------------------------------------------------------------
✓ Experiment created
✓ Logged parameters: {'n_estimators': 100, 'max_depth': 5, ...}
✓ Logged metrics: {'accuracy': 0.95, 'f1_score': 0.94}
✓ Logged model artifact
✅ Run completed successfully!

TEST 3: REGISTER MODEL IN UNITY CATALOG
----------------------------------------------------------------------
✓ Model registered in Unity Catalog!
   - Model Name: main.default.test_model_20251030_123456
   - Version: 1

🎉 ALL TESTS COMPLETED!
```

## View Results in Databricks

1. Go to your Databricks workspace
2. Navigate to **Experiments** to see your logged runs
3. Navigate to **Models** (Unity Catalog) to see registered models

## What's Next?

### Use in Your Own Code

```python
import mlflow

# Set tracking URI
mlflow.set_tracking_uri("databricks://my-workspace")

# Create experiment
mlflow.set_experiment("/Users/your-email@company.com/my-project")

# Log a run
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
    
# Register to Unity Catalog
mlflow.set_registry_uri("databricks-uc")
mlflow.register_model(
    f"runs:/{run_id}/model",
    "main.default.my_model"
)
```

### Test Databricks Connect (Optional)

If you want to run Spark code on Databricks from your IDE:

```bash
# Set your cluster ID
export DATABRICKS_CLUSTER_ID="your-cluster-id"

# Run test
uv run python test_databricks_connect.py
```

### Test GenAI Agent Logging (Optional)

```bash
uv run python test_genai_agent.py
```

## Troubleshooting

### Authentication Failed
- Re-run: `databricks auth login --profile my-workspace`
- Check `~/.databrickscfg` exists and has correct host

### MLflow Connection Error
- Verify `MLFLOW_TRACKING_URI` format: `databricks://your-profile`
- Ensure profile name matches in all configurations

### Unity Catalog Error
- Check `MLFLOW_REGISTRY_URI="databricks-uc"`
- Verify you have UC permissions in Databricks
- Ensure catalog and schema exist (default: `main.default`)

### Import Errors
- Run: `uv sync` to reinstall dependencies
- Verify Python version ≥ 3.9 with: `python --version`
- If using wrong Python version, ensure `.python-version` file exists

## Resources

- [Full README](README.md) - Detailed documentation
- [Databricks Connect Docs](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/)
- [OAuth U2M Auth Docs](https://docs.databricks.com/aws/en/dev-tools/auth/oauth-u2m)
- [MLflow GenAI Docs](https://mlflow.org/docs/latest/genai/mlflow-3/genai-agent/)

