# Testing Managed MLflow with Databricks from Local IDE

This project tests using Databricks-managed MLflow from a local IDE without needing the Databricks interface. It demonstrates:
- Creating and tracking MLflow experiments
- Registering models to MLflow registry
- Registering models in Unity Catalog

## Prerequisites

1. Access to a Databricks workspace
2. Python 3.9 or higher
3. [uv](https://docs.astral.sh/uv/) package manager installed
4. Appropriate permissions in your Databricks workspace

## Setup Instructions

### Step 1: Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Step 2: Install Dependencies

```bash
# Create virtual environment and install dependencies in one command
uv sync

# Or if you want to install manually
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Step 3: Authenticate with Databricks

The Databricks CLI is already installed via dependencies. Authenticate using OAuth U2M:

```bash
databricks auth login --profile your-profile
```

This will:
- Open your browser for authentication
- Create/update `~/.databrickscfg` with your profile

Your `~/.databrickscfg` should look like:
```
[your-profile]
host      = https://your-workspace-name.cloud.databricks.com
auth_type = databricks-cli
```

### Step 4: Configure Environment Variables

Create a `.env` file (see `.env.example`) or export these variables:

```bash
export DATABRICKS_PROFILE="your-profile"
export MLFLOW_TRACKING_URI="databricks://your-profile"
export MLFLOW_REGISTRY_URI="databricks-uc"
export DATABRICKS_CLUSTER_ID="your-cluster-id"  # Optional, for Databricks Connect
```

**Important Notes:**
- `MLFLOW_TRACKING_URI`: Use `databricks://your-profile` format
- `MLFLOW_REGISTRY_URI`: Use `databricks-uc` for Unity Catalog, or `databricks://your-profile` for legacy Model Registry
- Find your cluster ID in the Databricks UI under Compute > Your Cluster > Configuration

### Step 5: Run the Test Script

```bash
# Using uv (automatically uses the project's virtual environment)
uv run python test_mlflow_remote.py

# Or activate the virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python test_mlflow_remote.py
```

This will test:
1. ✅ Creating an MLflow experiment
2. ✅ Logging a run with parameters and metrics
3. ✅ Registering a model to MLflow registry
4. ✅ Registering a model in Unity Catalog

## Project Structure

```
test-mlflow-remote/
├── README.md                   # This file
├── pyproject.toml              # Project configuration and dependencies (uv)
├── requirements.txt            # Legacy Python dependencies (for reference)
├── .python-version             # Python version specification
├── .env.example               # Environment variable template
├── test_mlflow_remote.py      # Main test script
├── test_genai_agent.py        # GenAI agent example (optional)
└── test_databricks_connect.py # Databricks Connect test (optional)
```

## Testing Individual Components

### Test MLflow Tracking Only
```bash
uv run python -c "import test_mlflow_remote; test_mlflow_remote.test_mlflow_tracking()"
```

### Test Model Registry
```bash
uv run python -c "import test_mlflow_remote; test_mlflow_remote.test_model_registry()"
```

### Test Unity Catalog Model Registration
```bash
uv run python -c "import test_mlflow_remote; test_mlflow_remote.test_unity_catalog_model()"
```

## Common Issues

### Authentication Errors
- Ensure you've run `databricks auth login --profile your-profile`
- Check that `~/.databrickscfg` has the correct host and auth_type
- Verify the token cache at `~/.databricks/token-cache.json`

### MLflow Connection Errors
- Verify `MLFLOW_TRACKING_URI` is set to `databricks://your-profile`
- Ensure your profile name matches in both `.databrickscfg` and environment variables

### Unity Catalog Errors
- Verify you have permission to access Unity Catalog
- Check that the catalog and schema exist in your workspace
- Ensure `MLFLOW_REGISTRY_URI` is set to `databricks-uc`

## References

- [Databricks Connect for Python](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/)
- [OAuth U2M Authentication](https://docs.databricks.com/aws/en/dev-tools/auth/oauth-u2m)
- [MLflow 3 GenAI Agent](https://mlflow.org/docs/latest/genai/mlflow-3/genai-agent/)
- [Unity Catalog Model Management](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)

