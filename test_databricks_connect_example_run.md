>> (test-mlflow-remote) ⏺ dev/test-mlflow-remote % uv run test_databricks_connect.py                                                                                                                                                                                              ⎇ 
✓ Loaded environment variables from .env file

======================================================================
TESTING DATABRICKS CONNECT
======================================================================

✓ Databricks Connect imported successfully

🔌 Connecting to Databricks serverless compute (profile: DEFAULT)...
✓ Connected to Databricks!
  Spark version: 4.0.0

🧪 Testing basic Spark operations...

✓ Created DataFrame:
+-----+---+-----------+
| name|age| department|
+-----+---+-----------+
|Alice| 34|Engineering|
|  Bob| 45|      Sales|
|Cathy| 29|Engineering|
|David| 38|  Marketing|
+-----+---+-----------+


✓ Performing transformations...
+-----------+-----+
| department|count|
+-----------+-----+
|Engineering|    2|
|      Sales|    1|
|  Marketing|    1|
+-----------+-----+


✓ Testing Spark SQL...
+-----------+-----+
| department|count|
+-----------+-----+
|Engineering|    2|
|      Sales|    1|
|  Marketing|    1|
+-----------+-----+


✅ Databricks Connect test PASSED!
   You can now run Spark code on Databricks from your local IDE!