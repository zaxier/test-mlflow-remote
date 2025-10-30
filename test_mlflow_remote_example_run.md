

>> (test-mlflow-remote) ⏺ dev/test-mlflow-remote % uv run test_mlflow_remote.py                                                                                                                                                                                                   ⎇ 
✓ Loaded environment variables from .env file

======================================================================
TESTING MANAGED MLFLOW ON DATABRICKS FROM LOCAL IDE
======================================================================

======================================================================
CONFIGURATION CHECK
======================================================================

Required Configuration:
  ✓ MLFLOW_TRACKING_URI: databricks://e2demo...
  ✓ DATABRICKS_PROFILE: e2demo

Optional Configuration:
  ✓ MLFLOW_REGISTRY_URI: databricks-uc
  ✓ DATABRICKS_HOST: https://e2-demo-field-eng.cloud.databricks.com
  ○ DATABRICKS_CLUSTER_ID: not set (using defaults)
  ✓ UC_CATALOG: zaxier_dev
  ✓ UC_SCHEMA: default

✓ Found Databricks config file at: /Users/user.name/.databrickscfg

✅ Configuration looks good!
======================================================================


======================================================================
TEST 1: CREATE AND TRACK MLFLOW EXPERIMENT
======================================================================

📝 Setting experiment: /Workspace/Users/user@company.com/test-mlflow-remote
✓ Experiment created/found: /Users/user@company.com/test-mlflow-remote
  - Experiment ID: 2894186667680403
  - Artifact Location: dbfs:/databricks/mlflow-tracking/2894186667680403

🏃 Starting MLflow run...
✓ Logged parameters: {'n_estimators': 100, 'max_depth': 5, 'random_state': 42, 'test': 'local_ide'}
✓ Logged metrics: {'accuracy': 0.88, 'f1_score': 0.8800720072007201}
2025/10/30 16:23:30 WARNING mlflow.models.model: `artifact_path` is deprecated. Please use `name` instead.
2025/10/30 16:23:35 WARNING mlflow.utils.environment: Failed to resolve installed pip version. ``pip`` will be added to conda.yaml environment spec without a version specifier.
✓ Logged model artifact with signature

✅ Run completed successfully!
   - Run ID: f8604cbeb5bc4489a2d474b742dcc061
   - Run Name: test_run_20251030_162328
   - Status: RUNNING
🏃 View run test_run_20251030_162328 at: https://e2-demo-field-eng.cloud.databricks.com/ml/experiments/2894186667680403/runs/f8604cbeb5bc4489a2d474b742dcc061
🧪 View experiment at: https://e2-demo-field-eng.cloud.databricks.com/ml/experiments/2894186667680403

======================================================================
TEST 2: REGISTER MODEL TO MLFLOW REGISTRY
======================================================================

⚠ Skipping workspace model registry test (using Unity Catalog)
  Set MLFLOW_REGISTRY_URI='databricks://your-profile' to test workspace registry

======================================================================
TEST 3: REGISTER MODEL IN UNITY CATALOG
======================================================================

📦 Registering model in Unity Catalog:
   - Full name: zaxier_dev.default.test_model_20251030_162341
   - Catalog: zaxier_dev
   - Schema: default
   - From run: f8604cbeb5bc4489a2d474b742dcc061
Successfully registered model 'zaxier_dev.default.test_model_20251030_162341'.
2025/10/30 16:23:44 WARNING mlflow.tracking._model_registry.fluent: Run with id f8604cbeb5bc4489a2d474b742dcc061 has no artifacts at artifact path 'model', registering model based on models:/m-c2335afaef354bf5bc8100c64e80e88e instead
Downloading artifacts: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:02<00:00,  1.72it/s]
Uploading artifacts: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6/6 [00:06<00:00,  1.01s/it]
Created version '1' of model 'zaxier_dev.default.test_model_20251030_162341'.

✅ Model registered in Unity Catalog!
   - Model Name: zaxier_dev.default.test_model_20251030_162341
   - Version: 1
   - Status: READY
   - Source: models:/m-c2335afaef354bf5bc8100c64e80e88e
✓ Added description and tags to model version

======================================================================
TEST SUMMARY
======================================================================

✅ MLflow Tracking: PASSED
   - Run ID: f8604cbeb5bc4489a2d474b742dcc061

⚠ Model Registry (Workspace): SKIPPED

✅ Unity Catalog Model: PASSED
   - Model: zaxier_dev.default.test_model_20251030_162341 v1

======================================================================
🎉 ALL TESTS COMPLETED!
======================================================================

You can now use managed MLflow from your local IDE!
Check your Databricks workspace to see the logged experiments and models.
```