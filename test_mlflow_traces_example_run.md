(test-mlflow-remote) ⏺ dev/test-mlflow-remote % uv run python test_mlflow_traces.py                                                                                               ⎇ main*
✓ Loaded environment variables from .env file

======================================================================
TESTING MLFLOW TRACE LOGGING TO DATABRICKS
======================================================================

This test helps debug 403 Forbidden errors when logging traces.

======================================================================
CONFIGURATION CHECK
======================================================================

Required Configuration:
  ✓ MLFLOW_TRACKING_URI: databricks://e2demo...
  ✓ DATABRICKS_PROFILE: e2demo

Optional Configuration:
  ✓ MLFLOW_REGISTRY_URI: databricks-uc
  ✓ DATABRICKS_HOST: https://workspace-name.cloud.databricks.com

✓ Found Databricks config file at: /Users/xavier.armitage/.databrickscfg

✓ MLflow version: 3.0.1

✅ Configuration looks good!
======================================================================


======================================================================
Starting Test 1: Basic Trace Logging
======================================================================

======================================================================
TEST 1: LOG BASIC TRACE TO MLFLOW
======================================================================

📝 Setting experiment: /Workspace/Users/user@company.com/test-mlflow-remote
✓ Experiment created/found: /Users/user@company.com/test-mlflow-remote
  - Experiment ID: 2894186667680403
  - Artifact Location: dbfs:/databricks/mlflow-tracking/2894186667680403

🏃 Starting MLflow run...
✓ Run started: 2ad519e644e247759d388133b8c9c59a

📊 Executing traced function...
  → Starting ML pipeline...
  → Processing data...
✓ Function executed successfully
  - Result: completed

⏳ Waiting for traces to be exported...

✅ Trace logging completed!
   - Run ID: 2ad519e644e247759d388133b8c9c59a
   - Experiment: /Workspace/Users/user@company.com/test-mlflow-remote
🏃 View run trace_test_20251031_142525 at: https://workspace-name.cloud.databricks.com/ml/experiments/2894186667680403/runs/2ad519e644e247759d388133b8c9c59a
🧪 View experiment at: https://workspace-name.cloud.databricks.com/ml/experiments/2894186667680403

======================================================================
Starting Test 2: Trace Retrieval
======================================================================

======================================================================
TEST 2: RETRIEVE TRACES FROM MLFLOW
======================================================================

🔍 Searching for traces...
   - Experiment ID: 2894186667680403
   - Run ID: 2ad519e644e247759d388133b8c9c59a

📥 Attempting to retrieve traces...

✓ Retrieved run information
   - Run Name: trace_test_20251031_142525
   - Status: FINISHED
   - Artifact URI: dbfs:/databricks/mlflow-tracking/2894186667680403/2ad519e644e247759d388133b8c9c59a/artifacts

✓ Listed artifacts for run:
   - No artifacts found yet (traces may still be uploading)

🔍 Attempting to search traces via Tracing API...
⚠ No trace artifacts found
  This could mean:
  1. Traces are still being uploaded
  2. Traces failed to upload (check for 403 errors)
  3. Tracing is not fully configured

✅ Trace retrieval test completed!

======================================================================
Starting Test 3: Manual Trace Logging
======================================================================

======================================================================
TEST 3: MANUAL TRACE CREATION AND LOGGING
======================================================================

🏃 Starting MLflow run for manual trace...

📝 Creating manual trace with start_span()...
  → Executing manual operation...
  → Preprocessing step completed
  → Inference step completed
✓ Manual trace created with nested spans

⏳ Waiting for trace to be exported...

✅ Manual trace logging completed!
   - Run ID: b386ff6fea6f4c8a8e383ac28077fa5f
   - Trace includes: 1 agent span + 2 tool spans
🏃 View run manual_trace_20251031_142532 at: https://workspace-name.cloud.databricks.com/ml/experiments/2894186667680403/runs/b386ff6fea6f4c8a8e383ac28077fa5f
🧪 View experiment at: https://workspace-name.cloud.databricks.com/ml/experiments/2894186667680403

======================================================================
TEST SUMMARY
======================================================================

✅ PASSED: Basic Trace Logging

✅ PASSED: Trace Retrieval

✅ PASSED: Manual Trace Logging

======================================================================
🎉 ALL TESTS PASSED!
======================================================================

Trace logging to MLflow is working correctly!

Check your Databricks workspace MLflow UI to verify trace artifacts.
2025/10/31 14:25:37 INFO mlflow.tracing.export.async_export_queue: Flushing the async trace logging queue before program exit. This may take a while...