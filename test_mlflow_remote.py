"""
Test script for using managed MLflow on Databricks from local IDE.

This script demonstrates:
1. Creating and tracking MLflow experiments
2. Registering models to MLflow registry
3. Registering models in Unity Catalog

Prerequisites:
- Databricks CLI authenticated via: databricks auth login --profile your-profile
- Environment variables set (see .env.example)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    if Path(".env").exists():
        load_dotenv()
        print("✓ Loaded environment variables from .env file")
except ImportError:
    print("⚠ python-dotenv not installed, using system environment variables")


def check_configuration():
    """Verify that all required configuration is set."""
    print("\n" + "="*70)
    print("CONFIGURATION CHECK")
    print("="*70)
    
    required_vars = {
        "MLFLOW_TRACKING_URI": os.getenv("MLFLOW_TRACKING_URI"),
        "DATABRICKS_PROFILE": os.getenv("DATABRICKS_PROFILE"),
    }
    
    optional_vars = {
        "MLFLOW_REGISTRY_URI": os.getenv("MLFLOW_REGISTRY_URI"),
        "DATABRICKS_HOST": os.getenv("DATABRICKS_HOST"),
        "DATABRICKS_CLUSTER_ID": os.getenv("DATABRICKS_CLUSTER_ID"),
        "UC_CATALOG": os.getenv("UC_CATALOG", "main"),
        "UC_SCHEMA": os.getenv("UC_SCHEMA", "default"),
    }
    
    all_good = True
    
    print("\nRequired Configuration:")
    for var, value in required_vars.items():
        if value:
            # Mask sensitive values
            display_value = value if not value.startswith("databricks") else value[:20] + "..."
            print(f"  ✓ {var}: {display_value}")
        else:
            print(f"  ✗ {var}: NOT SET")
            all_good = False
    
    print("\nOptional Configuration:")
    for var, value in optional_vars.items():
        if value:
            display_value = value if len(value) < 50 else value[:50] + "..."
            print(f"  ✓ {var}: {display_value}")
        else:
            print(f"  ○ {var}: not set (using defaults)")
    
    # Check databrickscfg file
    databrickscfg_path = Path.home() / ".databrickscfg"
    if databrickscfg_path.exists():
        print(f"\n✓ Found Databricks config file at: {databrickscfg_path}")
    else:
        print(f"\n✗ Databricks config file not found at: {databrickscfg_path}")
        print("  Run: databricks auth login --profile your-profile")
        all_good = False
    
    if not all_good:
        print("\n❌ Configuration incomplete. Please set required environment variables.")
        print("   See .env.example for reference.")
        sys.exit(1)
    
    print("\n✅ Configuration looks good!")
    print("="*70 + "\n")


def test_mlflow_tracking():
    """Test 1: Create and track an MLflow experiment."""
    print("\n" + "="*70)
    print("TEST 1: CREATE AND TRACK MLFLOW EXPERIMENT")
    print("="*70)
    
    try:
        # Set experiment name (in Databricks, this should be a path)
        experiment_name = os.getenv(
            "MLFLOW_EXPERIMENT_NAME",
            f"/Users/{os.getenv('USER', 'default')}/test-mlflow-remote"
        )
        print(f"\n📝 Setting experiment: {experiment_name}")
        
        mlflow.set_experiment(experiment_name)
        experiment = mlflow.get_experiment_by_name(experiment_name)
        
        if experiment:
            print(f"✓ Experiment created/found: {experiment.name}")
            print(f"  - Experiment ID: {experiment.experiment_id}")
            print(f"  - Artifact Location: {experiment.artifact_location}")
        
        # Start a run and log parameters/metrics
        print("\n🏃 Starting MLflow run...")
        with mlflow.start_run(run_name=f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:
            # Log parameters
            params = {
                "n_estimators": 100,
                "max_depth": 5,
                "random_state": 42,
                "test": "local_ide"
            }
            mlflow.log_params(params)
            print(f"✓ Logged parameters: {params}")

            # Create a simple model
            X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Extract only model parameters (exclude metadata like 'test')
            model_params = {k: v for k, v in params.items() if k in ["n_estimators", "max_depth", "random_state"]}
            model = RandomForestClassifier(**model_params)
            model.fit(X_train, y_train)
            
            # Log metrics
            y_pred = model.predict(X_test)
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "f1_score": f1_score(y_test, y_pred, average='weighted')
            }
            mlflow.log_metrics(metrics)
            print(f"✓ Logged metrics: {metrics}")

            # Log the model with signature (required for Unity Catalog)
            from mlflow.models import infer_signature
            signature = infer_signature(X_train, model.predict(X_train))
            mlflow.sklearn.log_model(model, "model", signature=signature)
            print("✓ Logged model artifact with signature")
            
            print(f"\n✅ Run completed successfully!")
            print(f"   - Run ID: {run.info.run_id}")
            print(f"   - Run Name: {run.info.run_name}")
            print(f"   - Status: {run.info.status}")
            
            return run.info.run_id, model
            
    except Exception as e:
        print(f"\n❌ Error in MLflow tracking test: {str(e)}")
        raise


def test_model_registry(run_id, model_name="test_sklearn_model"):
    """Test 2: Register a model to MLflow registry (workspace registry)."""
    print("\n" + "="*70)
    print("TEST 2: REGISTER MODEL TO MLFLOW REGISTRY")
    print("="*70)
    
    try:
        # For workspace model registry, we need to use databricks:// URI
        registry_uri = os.getenv("MLFLOW_REGISTRY_URI", "databricks")
        
        # If using UC, skip this test
        if registry_uri == "databricks-uc":
            print("\n⚠ Skipping workspace model registry test (using Unity Catalog)")
            print("  Set MLFLOW_REGISTRY_URI='databricks://your-profile' to test workspace registry")
            return None
        
        print(f"\n📦 Registering model: {model_name}")
        print(f"   From run: {run_id}")
        
        # Construct the model URI
        model_uri = f"runs:/{run_id}/model"
        
        # Register the model
        model_version = mlflow.register_model(model_uri, model_name)
        
        print(f"\n✅ Model registered successfully!")
        print(f"   - Model Name: {model_version.name}")
        print(f"   - Version: {model_version.version}")
        print(f"   - Status: {model_version.status}")
        print(f"   - Source: {model_version.source}")
        
        return model_version
        
    except Exception as e:
        print(f"\n❌ Error in model registry test: {str(e)}")
        print(f"   This might be expected if you're using Unity Catalog exclusively")
        return None


def test_unity_catalog_model(run_id):
    """Test 3: Register a model in Unity Catalog."""
    print("\n" + "="*70)
    print("TEST 3: REGISTER MODEL IN UNITY CATALOG")
    print("="*70)
    
    try:
        # Check if UC is configured
        registry_uri = os.getenv("MLFLOW_REGISTRY_URI", "")
        if registry_uri != "databricks-uc":
            print("\n⚠ Skipping Unity Catalog test (not configured)")
            print("  Set MLFLOW_REGISTRY_URI='databricks-uc' to test Unity Catalog")
            return None
        
        # Get UC configuration
        catalog = os.getenv("UC_CATALOG", "main")
        schema = os.getenv("UC_SCHEMA", "default")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name = f"{catalog}.{schema}.test_model_{timestamp}"
        
        print(f"\n📦 Registering model in Unity Catalog:")
        print(f"   - Full name: {model_name}")
        print(f"   - Catalog: {catalog}")
        print(f"   - Schema: {schema}")
        print(f"   - From run: {run_id}")
        
        # Construct the model URI
        model_uri = f"runs:/{run_id}/model"
        
        # Register the model in Unity Catalog
        model_version = mlflow.register_model(model_uri, model_name)
        
        print(f"\n✅ Model registered in Unity Catalog!")
        print(f"   - Model Name: {model_version.name}")
        print(f"   - Version: {model_version.version}")
        print(f"   - Status: {model_version.status}")
        print(f"   - Source: {model_version.source}")
        
        # Try to add a description and tags
        try:
            from mlflow.tracking import MlflowClient
            client = MlflowClient()
            
            client.update_model_version(
                name=model_name,
                version=model_version.version,
                description="Test model registered from local IDE"
            )
            
            client.set_model_version_tag(
                name=model_name,
                version=model_version.version,
                key="source",
                value="local_ide_test"
            )
            print("✓ Added description and tags to model version")
            
        except Exception as tag_error:
            print(f"⚠ Could not add tags: {str(tag_error)}")
        
        return model_version
        
    except Exception as e:
        print(f"\n❌ Error in Unity Catalog test: {str(e)}")
        print(f"   Error details: {type(e).__name__}")
        raise


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("TESTING MANAGED MLFLOW ON DATABRICKS FROM LOCAL IDE")
    print("="*70)
    
    # Check configuration
    check_configuration()
    
    try:
        # Test 1: MLflow Tracking
        run_id, model = test_mlflow_tracking()
        
        # Test 2: Model Registry (workspace)
        model_version_workspace = test_model_registry(run_id)
        
        # Test 3: Unity Catalog
        model_version_uc = test_unity_catalog_model(run_id)
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print("\n✅ MLflow Tracking: PASSED")
        print(f"   - Run ID: {run_id}")
        
        if model_version_workspace:
            print("\n✅ Model Registry (Workspace): PASSED")
            print(f"   - Model: {model_version_workspace.name} v{model_version_workspace.version}")
        else:
            print("\n⚠ Model Registry (Workspace): SKIPPED")
        
        if model_version_uc:
            print("\n✅ Unity Catalog Model: PASSED")
            print(f"   - Model: {model_version_uc.name} v{model_version_uc.version}")
        else:
            print("\n⚠ Unity Catalog Model: SKIPPED")
        
        print("\n" + "="*70)
        print("🎉 ALL TESTS COMPLETED!")
        print("="*70)
        print("\nYou can now use managed MLflow from your local IDE!")
        print("Check your Databricks workspace to see the logged experiments and models.")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ TESTS FAILED")
        print("="*70)
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("  1. Databricks authentication (databricks auth login)")
        print("  2. Environment variables (see .env.example)")
        print("  3. Workspace permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()

