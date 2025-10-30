"""
Test GenAI Agent with MLflow 3.

This script demonstrates creating a simple GenAI agent and logging it
to MLflow on Databricks. This is useful for LLM application development.

Prerequisites:
- MLflow 2.10.0 or higher
- Authenticated with Databricks
- MLFLOW_TRACKING_URI and MLFLOW_REGISTRY_URI set
- OpenAI API key (for testing with real LLM)

Note: This is an example structure. Full implementation would require
additional dependencies and configuration.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

import mlflow

try:
    from dotenv import load_dotenv
    if Path(".env").exists():
        load_dotenv()
except ImportError:
    pass


def create_simple_agent():
    """
    Create a simple example agent.
    
    In production, this would be a more sophisticated agent using
    LangChain, LlamaIndex, or custom implementation.
    """
    
    class SimpleAgent:
        """A simple example agent for demonstration."""
        
        def __init__(self, model_name="gpt-3.5-turbo"):
            self.model_name = model_name
            
        def __call__(self, question: str) -> str:
            """
            Process a question and return an answer.
            
            In production, this would call an LLM API.
            """
            return f"Mock response to: {question} (from {self.model_name})"
        
        def predict(self, context, data):
            """MLflow predict interface."""
            if isinstance(data, dict) and "question" in data:
                return self.__call__(data["question"])
            return self.__call__(str(data))
    
    return SimpleAgent()


def test_genai_agent_logging():
    """Test logging a GenAI agent to MLflow."""
    print("\n" + "="*70)
    print("TEST: GENAI AGENT WITH MLFLOW")
    print("="*70)
    
    try:
        # Set experiment
        experiment_name = os.getenv(
            "MLFLOW_EXPERIMENT_NAME",
            f"/Users/{os.getenv('USER', 'default')}/test-genai-agent"
        )
        print(f"\n📝 Setting experiment: {experiment_name}")
        mlflow.set_experiment(experiment_name)
        
        # Create agent
        print("\n🤖 Creating GenAI agent...")
        agent = create_simple_agent()
        
        # Test the agent
        test_question = "What is the capital of France?"
        test_response = agent(test_question)
        print(f"\n✓ Agent test:")
        print(f"  Q: {test_question}")
        print(f"  A: {test_response}")
        
        # Log to MLflow
        print("\n📦 Logging agent to MLflow...")
        with mlflow.start_run(run_name=f"genai_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            
            # Log parameters
            mlflow.log_param("agent_type", "simple_mock")
            mlflow.log_param("model_name", "gpt-3.5-turbo")
            
            # Log metrics (in production, you'd evaluate the agent)
            mlflow.log_metric("test_passed", 1)
            
            # Log the agent as a model
            # Note: For production GenAI agents, you'd use:
            # mlflow.langchain.log_model() or similar
            mlflow.pyfunc.log_model(
                artifact_path="agent",
                python_model=agent,
                pip_requirements=[
                    "mlflow>=2.10.0",
                ]
            )
            
            print("✓ Agent logged successfully")
            
            # Log example inputs/outputs
            mlflow.log_dict(
                {
                    "example_questions": [
                        "What is the capital of France?",
                        "Explain machine learning",
                        "What is Python?"
                    ],
                    "example_response": test_response
                },
                "examples.json"
            )
            
            run_id = mlflow.active_run().info.run_id
            print(f"\n✅ GenAI Agent logged successfully!")
            print(f"   - Run ID: {run_id}")
        
        print("\n" + "="*70)
        print("📚 NEXT STEPS FOR PRODUCTION GENAI AGENTS:")
        print("="*70)
        print("""
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
        """)
        
    except Exception as e:
        print(f"\n❌ Error in GenAI agent test: {str(e)}")
        raise


if __name__ == "__main__":
    test_genai_agent_logging()

