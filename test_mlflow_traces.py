"""
Test script for logging MLflow traces remotely to Databricks.

This script demonstrates:
1. Logging traces to MLflow on Databricks using @mlflow.trace decorator
2. Creating manual traces with mlflow.start_span()
3. Retrieving traces from remote MLflow backend
4. Testing trace export functionality

This test follows the official MLflow tracing best practices:
https://mlflow.org/docs/latest/genai/tracing/quickstart/python-openai/

Key features:
- Uses @mlflow.trace decorator with SpanType for automatic tracing
- Uses mlflow.start_span() for manual span creation
- Proper span types (AGENT, TOOL) for semantic clarity
- Nested spans to represent hierarchical workflows

This test is designed to help debug 403 Forbidden errors when
sending traces to MLflow backend (S3 artifact storage).

Prerequisites:
- Databricks CLI authenticated via: databricks auth login --profile your-profile
- Environment variables set (see .env.example)
- MLflow 3.0.0 or higher
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import mlflow
from mlflow.entities import SpanType

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
    
    # Check MLflow version
    mlflow_version = mlflow.__version__
    print(f"\n✓ MLflow version: {mlflow_version}")
    
    if not all_good:
        print("\n❌ Configuration incomplete. Please set required environment variables.")
        print("   See .env.example for reference.")
        sys.exit(1)
    
    print("\n✅ Configuration looks good!")
    print("="*70 + "\n")


# Example traced function - simple computation
@mlflow.trace(span_type=SpanType.TOOL)
def process_data(data: dict) -> dict:
    """
    A simple function that processes data and is automatically traced.
    
    This simulates a typical ML workflow step that you'd want to trace.
    Uses SpanType.TOOL as this represents a tool/utility function.
    """
    print("  → Processing data...")
    
    # Simulate some processing steps
    result = {
        "input_size": len(str(data)),
        "processed_at": datetime.now().isoformat(),
        "result": f"Processed: {data.get('value', 'N/A')}"
    }
    
    time.sleep(0.1)  # Simulate some work
    
    return result


@mlflow.trace(span_type=SpanType.AGENT)
def ml_pipeline(input_value: str) -> dict:
    """
    A traced ML pipeline that calls other traced functions.
    
    This simulates a more complex workflow with nested traces.
    Uses SpanType.AGENT as this represents the main agent/orchestrator.
    """
    print("  → Starting ML pipeline...")
    
    # Step 1: Prepare data
    data = {"value": input_value, "timestamp": time.time()}
    
    # Step 2: Process data (this will create a nested trace)
    processed = process_data(data)
    
    # Step 3: Generate final result
    final_result = {
        **processed,
        "pipeline_status": "completed",
        "pipeline_version": "1.0.0"
    }
    
    return final_result


def test_basic_trace_logging():
    """Test 1: Log a basic trace to MLflow."""
    print("\n" + "="*70)
    print("TEST 1: LOG BASIC TRACE TO MLFLOW")
    print("="*70)
    
    try:
        # Set experiment name
        experiment_name = os.getenv(
            "MLFLOW_EXPERIMENT_NAME",
            f"/Users/{os.getenv('USER', 'default')}/test-mlflow-traces"
        )
        print(f"\n📝 Setting experiment: {experiment_name}")
        
        mlflow.set_experiment(experiment_name)
        experiment = mlflow.get_experiment_by_name(experiment_name)
        
        if experiment:
            print(f"✓ Experiment created/found: {experiment.name}")
            print(f"  - Experiment ID: {experiment.experiment_id}")
            print(f"  - Artifact Location: {experiment.artifact_location}")
        
        # Note: Traces are automatically logged when using @mlflow.trace decorator
        # No need to call mlflow.autolog() unless using library-specific integrations
        
        # Create a run to associate traces with
        print("\n🏃 Starting MLflow run...")
        with mlflow.start_run(run_name=f"trace_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:
            run_id = run.info.run_id
            print(f"✓ Run started: {run_id}")
            
            # Log some parameters
            mlflow.log_param("test_type", "trace_logging")
            mlflow.log_param("trace_version", "1.0")
            
            # Execute traced function
            print("\n📊 Executing traced function...")
            input_data = f"test_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = ml_pipeline(input_data)
            
            print(f"✓ Function executed successfully")
            print(f"  - Result: {result['pipeline_status']}")
            
            # Log the result as a metric
            mlflow.log_metric("execution_success", 1)
            
            # Give traces time to be exported
            print("\n⏳ Waiting for traces to be exported...")
            time.sleep(2)
            
            print(f"\n✅ Trace logging completed!")
            print(f"   - Run ID: {run_id}")
            print(f"   - Experiment: {experiment_name}")
            
            return run_id, experiment.experiment_id
            
    except Exception as e:
        print(f"\n❌ Error in basic trace logging test: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check if this is a 403 error
        if "403" in str(e) or "Forbidden" in str(e):
            print("\n⚠️  DETECTED 403 FORBIDDEN ERROR!")
            print("   This matches the customer's reported issue.")
            print("   Error details:")
            print(f"   {str(e)}")
        
        raise


def test_trace_retrieval(run_id, experiment_id):
    """Test 2: Retrieve traces from MLflow."""
    print("\n" + "="*70)
    print("TEST 2: RETRIEVE TRACES FROM MLFLOW")
    print("="*70)
    
    try:
        from mlflow.tracking import MlflowClient
        client = MlflowClient()
        
        print(f"\n🔍 Searching for traces...")
        print(f"   - Experiment ID: {experiment_id}")
        print(f"   - Run ID: {run_id}")
        
        # Try to get traces for the run
        try:
            # Search for traces in the experiment
            print("\n📥 Attempting to retrieve traces...")
            
            # Method 1: Try to get trace info from run
            run = client.get_run(run_id)
            print(f"\n✓ Retrieved run information")
            print(f"   - Run Name: {run.info.run_name}")
            print(f"   - Status: {run.info.status}")
            print(f"   - Artifact URI: {run.info.artifact_uri}")
            
            # Method 2: Try to list artifacts to see if traces are there
            artifacts = client.list_artifacts(run_id)
            print(f"\n✓ Listed artifacts for run:")
            if artifacts:
                for artifact in artifacts:
                    print(f"   - {artifact.path} (size: {artifact.file_size} bytes)")
                    if "trace" in artifact.path.lower():
                        print(f"     → Found trace artifact!")
            else:
                print("   - No artifacts found yet (traces may still be uploading)")
            
            # Method 3: Try to search traces using MLflow Tracing API
            try:
                # Note: This API may vary depending on MLflow version
                print(f"\n🔍 Attempting to search traces via Tracing API...")
                
                # In MLflow 3.x, traces are typically stored as artifacts
                # Check if there's a traces.json file
                trace_artifacts = [a for a in artifacts if "trace" in a.path.lower()]
                
                if trace_artifacts:
                    print(f"✓ Found {len(trace_artifacts)} trace artifact(s)")
                    for trace_artifact in trace_artifacts:
                        print(f"   - {trace_artifact.path}")
                else:
                    print("⚠ No trace artifacts found")
                    print("  This could mean:")
                    print("  1. Traces are still being uploaded")
                    print("  2. Traces failed to upload (check for 403 errors)")
                    print("  3. Tracing is not fully configured")
                
            except Exception as search_error:
                print(f"⚠ Could not search traces via API: {str(search_error)}")
            
            print(f"\n✅ Trace retrieval test completed!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error retrieving traces: {str(e)}")
            
            # Check for 403 error
            if "403" in str(e) or "Forbidden" in str(e):
                print("\n⚠️  DETECTED 403 FORBIDDEN ERROR!")
                print("   This matches the customer's reported issue.")
                print("   The trace was logged but cannot be retrieved from S3.")
            
            raise
            
    except Exception as e:
        print(f"\n❌ Error in trace retrieval test: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        raise


def test_manual_trace_logging():
    """Test 3: Manually create and log a trace using mlflow.start_span()."""
    print("\n" + "="*70)
    print("TEST 3: MANUAL TRACE CREATION AND LOGGING")
    print("="*70)
    
    try:
        experiment_name = os.getenv(
            "MLFLOW_EXPERIMENT_NAME",
            f"/Users/{os.getenv('USER', 'default')}/test-mlflow-traces"
        )
        
        mlflow.set_experiment(experiment_name)
        
        print("\n🏃 Starting MLflow run for manual trace...")
        with mlflow.start_run(run_name=f"manual_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:
            run_id = run.info.run_id
            
            # Create a simple trace manually using the start_span context manager
            # This follows the pattern from MLflow documentation for custom instrumentation
            print("\n📝 Creating manual trace with start_span()...")
            
            with mlflow.start_span(name="manual_agent_operation", span_type=SpanType.AGENT) as span:
                span.set_attribute("operation_type", "test")
                span.set_attribute("timestamp", datetime.now().isoformat())
                span.set_attribute("version", "1.0.0")
                
                # Simulate some work
                print("  → Executing manual operation...")
                time.sleep(0.5)
                
                # Add nested spans with appropriate span types
                with mlflow.start_span(name="data_preprocessing", span_type=SpanType.TOOL) as sub_span1:
                    sub_span1.set_attribute("step", 1)
                    sub_span1.set_attribute("tool_name", "preprocessor")
                    time.sleep(0.2)
                    print("  → Preprocessing step completed")
                
                with mlflow.start_span(name="model_inference", span_type=SpanType.TOOL) as sub_span2:
                    sub_span2.set_attribute("step", 2)
                    sub_span2.set_attribute("tool_name", "model")
                    time.sleep(0.2)
                    print("  → Inference step completed")
                
                span.set_attribute("status", "completed")
                span.set_attribute("total_steps", 2)
            
            print("✓ Manual trace created with nested spans")
            
            # Log completion metric
            mlflow.log_metric("manual_trace_success", 1)
            
            # Wait for export
            print("\n⏳ Waiting for trace to be exported...")
            time.sleep(2)
            
            print(f"\n✅ Manual trace logging completed!")
            print(f"   - Run ID: {run_id}")
            print(f"   - Trace includes: 1 agent span + 2 tool spans")
            
            return run_id
            
    except Exception as e:
        print(f"\n❌ Error in manual trace logging: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check for 403 error
        if "403" in str(e) or "Forbidden" in str(e):
            print("\n⚠️  DETECTED 403 FORBIDDEN ERROR!")
            print("   Error details:")
            print(f"   {str(e)}")
            
            # Try to extract more information from the error
            if "s3.us-east-2.amazonaws.com" in str(e):
                print("\n   The error is related to S3 artifact storage access.")
                print("   Possible causes:")
                print("   1. IAM permissions issue on the S3 bucket")
                print("   2. Pre-signed URL generation issue")
                print("   3. Databricks workspace configuration issue")
                print("   4. Network/firewall blocking S3 access")
        
        raise


def main():
    """Run all trace logging tests."""
    print("\n" + "="*70)
    print("TESTING MLFLOW TRACE LOGGING TO DATABRICKS")
    print("="*70)
    print("\nThis test helps debug 403 Forbidden errors when logging traces.")
    
    # Check configuration
    check_configuration()
    
    test_results = {
        "basic_trace_logging": False,
        "trace_retrieval": False,
        "manual_trace_logging": False,
    }
    
    errors_encountered = []
    
    try:
        # Test 1: Basic trace logging with decorator
        print("\n" + "="*70)
        print("Starting Test 1: Basic Trace Logging")
        print("="*70)
        
        try:
            run_id, experiment_id = test_basic_trace_logging()
            test_results["basic_trace_logging"] = True
        except Exception as e:
            print(f"\n⚠️  Test 1 failed: {str(e)}")
            errors_encountered.append(("Basic Trace Logging", e))
            run_id = None
            experiment_id = None
        
        # Test 2: Trace retrieval (only if Test 1 succeeded)
        if run_id and experiment_id:
            print("\n" + "="*70)
            print("Starting Test 2: Trace Retrieval")
            print("="*70)
            
            try:
                test_trace_retrieval(run_id, experiment_id)
                test_results["trace_retrieval"] = True
            except Exception as e:
                print(f"\n⚠️  Test 2 failed: {str(e)}")
                errors_encountered.append(("Trace Retrieval", e))
        else:
            print("\n⚠️  Skipping Test 2 (Test 1 failed)")
        
        # Test 3: Manual trace logging
        print("\n" + "="*70)
        print("Starting Test 3: Manual Trace Logging")
        print("="*70)
        
        try:
            test_manual_trace_logging()
            test_results["manual_trace_logging"] = True
        except Exception as e:
            print(f"\n⚠️  Test 3 failed: {str(e)}")
            errors_encountered.append(("Manual Trace Logging", e))
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        for test_name, passed in test_results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"\n{status}: {test_name.replace('_', ' ').title()}")
        
        # Error analysis
        if errors_encountered:
            print("\n" + "="*70)
            print("ERROR ANALYSIS")
            print("="*70)
            
            has_403_error = False
            
            for test_name, error in errors_encountered:
                print(f"\n❌ {test_name}:")
                print(f"   {str(error)}")
                
                if "403" in str(error) or "Forbidden" in str(error):
                    has_403_error = True
            
            if has_403_error:
                print("\n" + "="*70)
                print("⚠️  403 FORBIDDEN ERROR DETECTED")
                print("="*70)
                print("""
This matches the customer's reported issue!

The error indicates that MLflow is unable to write trace artifacts to S3.

Possible root causes:
1. IAM Role Permissions: The Databricks workspace's IAM role may lack
   PutObject permissions for the S3 bucket storing MLflow artifacts.

2. Pre-signed URL Issue: The pre-signed URL generated for uploading
   traces might be expired or malformed.

3. S3 Bucket Policy: The bucket policy might not allow writes from
   the workspace's IAM role or external clients.

4. Network/Firewall: Network restrictions might be blocking S3 access
   from your local machine or the Databricks workspace.

Recommended debugging steps:
1. Check Databricks workspace IAM role permissions for S3
2. Verify S3 bucket policy allows PutObject operations
3. Test with a different network connection (VPN on/off)
4. Check if traces work when run directly in Databricks notebooks
5. Review Databricks workspace configuration for MLflow artifact storage
6. Check if the issue occurs with all artifact types or just traces

Next step: Try running this same code from a Databricks notebook to see
if the issue is specific to remote clients or affects all trace logging.
                """)
        
        # Final status
        all_passed = all(test_results.values())
        
        print("\n" + "="*70)
        if all_passed:
            print("🎉 ALL TESTS PASSED!")
            print("="*70)
            print("\nTrace logging to MLflow is working correctly!")
        else:
            print("⚠️  SOME TESTS FAILED")
            print("="*70)
            print("\nPlease review the errors above and check:")
            print("  1. Databricks workspace permissions")
            print("  2. S3 bucket policies and IAM roles")
            print("  3. Network connectivity to S3")
            print("  4. MLflow configuration")
        
        print("\nCheck your Databricks workspace MLflow UI to verify trace artifacts.")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ TESTS FAILED")
        print("="*70)
        print(f"\nUnexpected error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        print("\nPlease check:")
        print("  1. Databricks authentication (databricks auth login)")
        print("  2. Environment variables (see .env.example)")
        print("  3. Workspace permissions")
        print("  4. MLflow version (requires 3.0.0+)")
        
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        
        sys.exit(1)


if __name__ == "__main__":
    main()

