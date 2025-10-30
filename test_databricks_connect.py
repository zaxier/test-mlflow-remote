"""
Test Databricks Connect functionality.

This script tests basic Databricks Connect operations to ensure
you can run Spark code on a Databricks cluster from your local IDE.

Prerequisites:
- Databricks Connect installed (databricks-connect>=13.3.0)
- DATABRICKS_CLUSTER_ID environment variable set
- Authenticated via databricks auth login
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    if Path(".env").exists():
        load_dotenv()
        print("✓ Loaded environment variables from .env file")
except ImportError:
    print("⚠ python-dotenv not installed, using system environment variables")


def test_databricks_connect():
    """Test Databricks Connect connection and basic Spark operations."""
    print("\n" + "="*70)
    print("TESTING DATABRICKS CONNECT")
    print("="*70)

    # Check configuration
    cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")
    profile = os.getenv("DATABRICKS_CONFIG_PROFILE", "DEFAULT")

    try:
        # Import Databricks Connect
        from databricks.connect import DatabricksSession

        print("\n✓ Databricks Connect imported successfully")

        # Initialize Spark session
        if cluster_id:
            print(f"\n🔌 Connecting to Databricks cluster: {cluster_id}")
            spark = DatabricksSession.builder.getOrCreate()
        else:
            print(f"\n🔌 Connecting to Databricks serverless compute (profile: {profile})...")
            spark = DatabricksSession.builder.serverless().profile(profile).getOrCreate()
        
        print("✓ Connected to Databricks!")
        print(f"  Spark version: {spark.version}")
        
        # Test basic Spark operation
        print("\n🧪 Testing basic Spark operations...")
        
        # Create a simple DataFrame
        data = [
            ("Alice", 34, "Engineering"),
            ("Bob", 45, "Sales"),
            ("Cathy", 29, "Engineering"),
            ("David", 38, "Marketing")
        ]
        columns = ["name", "age", "department"]
        
        df = spark.createDataFrame(data, columns)
        
        print("\n✓ Created DataFrame:")
        df.show()
        
        # Perform some transformations
        print("\n✓ Performing transformations...")
        result = df.groupBy("department").count()
        result.show()
        
        # Test SQL
        print("\n✓ Testing Spark SQL...")
        df.createOrReplaceTempView("employees")
        sql_result = spark.sql("SELECT department, COUNT(*) as count FROM employees GROUP BY department")
        sql_result.show()
        
        print("\n✅ Databricks Connect test PASSED!")
        print("   You can now run Spark code on Databricks from your local IDE!")
        
        # Clean up
        spark.stop()
        
    except ImportError as e:
        print(f"\n❌ Databricks Connect not installed: {str(e)}")
        print("   Install with: pip install databricks-connect>=13.3.0")
    except Exception as e:
        print(f"\n❌ Error testing Databricks Connect: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        print("\n   Troubleshooting:")
        print("   1. Verify cluster is running")
        print("   2. Check DATABRICKS_CLUSTER_ID is correct")
        print("   3. Ensure you're authenticated (databricks auth login)")
        print("   4. Verify cluster supports Databricks Connect (Runtime 13.3 LTS+)")
        raise


if __name__ == "__main__":
    test_databricks_connect()

