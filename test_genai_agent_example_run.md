(test-mlflow-remote) ⏺ dev/test-mlflow-remote % uv run test_genai_agent.py                                                                                                                                                                                                     ⎇ 

======================================================================
TEST: GENAI AGENT WITH MLFLOW
======================================================================

📝 Setting experiment: /Workspace/Users/user@company.com/test-mlflow-remote

🤖 Creating GenAI agent...
$HOME/dev/test-mlflow-remote/.venv/lib/python3.10/site-packages/mlflow/pyfunc/utils/data_validation.py:186: UserWarning: Add type hints to the `predict` method to enable data validation and automatic signature inference during model logging. Check https://mlflow.org/docs/latest/model/python_model.html#type-hint-usage-in-pythonmodel for more details.
  color_warning(

✓ Agent test:
  Q: What is the capital of France?
  A: Mock response to: What is the capital of France? (from gpt-3.5-turbo)

📦 Logging agent to MLflow...
2025/10/30 16:39:48 INFO mlflow.pyfunc: Inferring model signature from input example
2025/10/30 16:39:48 WARNING mlflow.utils.environment: Failed to resolve installed pip version. ``pip`` will be added to conda.yaml environment spec without a version specifier.
✓ Agent logged successfully

✅ GenAI Agent logged successfully!
   - Run ID: 9dfb4a46f4944c129638178747ac7ff6
🏃 View run genai_agent_20251030_163944 at: https://e2-demo-field-eng.cloud.databricks.com/ml/experiments/2894186667680403/runs/9dfb4a46f4944c129638178747ac7ff6
🧪 View experiment at: https://e2-demo-field-eng.cloud.databricks.com/ml/experiments/2894186667680403

======================================================================
📚 NEXT STEPS FOR PRODUCTION GENAI AGENTS:
======================================================================

For production GenAI applications with MLflow 3, you would:

1. Use LangChain or LlamaIndex to build your agent:
   from langchain.agents import create_openai_functions_agent
   from langchain_openai import ChatOpenAI
   
2. Log with specialized flavors:
   mlflow.langchain.log_model(agent, "agent")
   
3. Use MLflow Tracing for observability:
   mlflow.langchain.autolog()
   
4. Evaluate with MLflow's GenAI evaluation:
   mlflow.evaluate(
       model=model_uri,
       data=eval_data,
       targets="ground_truth",
       model_type="question-answering"
   )

5. Deploy to Databricks Model Serving:
   - Register model to Unity Catalog
   - Create serving endpoint
   - Integrate with your application

See: https://mlflow.org/docs/latest/genai/mlflow-3/genai-agent/