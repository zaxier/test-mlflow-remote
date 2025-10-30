>> (test-mlflow-remote) ⏺ dev/test-mlflow-remote % uv run test_genai_agent.py                                                                                                                                                                                                     ⎇ 

======================================================================
TEST: GENAI AGENT WITH MLFLOW
======================================================================

📝 Setting experiment: /Workspace/Users/xavier.armitage@databricks.com/test-mlflow-remote

🤖 Creating GenAI agent...

✓ Agent test:
  Q: What is the capital of France?
  A: Mock response to: What is the capital of France? (from gpt-3.5-turbo)

📦 Logging agent to MLflow...
2025/10/30 16:25:14 WARNING mlflow.models.model: `artifact_path` is deprecated. Please use `name` instead.
/Users/xavier.armitage/Library/CloudStorage/Dropbox/Repositories/dev/test-mlflow-remote/.venv/lib/python3.9/site-packages/mlflow/pyfunc/utils/data_validation.py:155: FutureWarning: Model's `predict` method contains invalid parameters: {'question'}. Only the following parameter names are allowed: context, model_input, and params. Note that invalid parameters will no longer be permitted in future versions.
  param_names = _check_func_signature(func, "predict")
/Users/xavier.armitage/Library/CloudStorage/Dropbox/Repositories/dev/test-mlflow-remote/.venv/lib/python3.9/site-packages/mlflow/pyfunc/utils/data_validation.py:47: UserWarning: Type hint used in the model's predict function is not supported for MLflow's schema validation. Type hints must be wrapped in list[...] because MLflow assumes the predict method to take multiple input instances. Specify your type hint as `list[str]` for a valid signature. Remove the type hint to disable this warning. To enable validation for the input data, specify input example or model signature when logging the model. 
  func_info = _get_func_info_if_type_hint_supported(func)
/Users/xavier.armitage/Library/CloudStorage/Dropbox/Repositories/dev/test-mlflow-remote/.venv/lib/python3.9/site-packages/mlflow/pyfunc/__init__.py:3191: UserWarning: Failed to infer signature from type hint: Type hints must be wrapped in list[...] because MLflow assumes the predict method to take multiple input instances. Specify your type hint as `list[str]` for a valid signature.
  signature_from_type_hints = _infer_signature_from_type_hints(
2025/10/30 16:25:17 WARNING mlflow.utils.environment: Failed to resolve installed pip version. ``pip`` will be added to conda.yaml environment spec without a version specifier.
2025/10/30 16:25:17 WARNING mlflow.models.model: Model logged without a signature and input example. Please set `input_example` parameter when logging the model to auto infer the model signature.
✓ Agent logged successfully

✅ GenAI Agent logged successfully!
   - Run ID: 6938e0c9bc704c5ebbaee48d2ea277d1
🏃 View run genai_agent_20251030_162512 at: https://e2-demo-field-eng.cloud.databricks.com/ml/experiments/2894186667680403/runs/6938e0c9bc704c5ebbaee48d2ea277d1
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