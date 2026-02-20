import mlflow
import os
from src.utils.logger import logger
import mlflow.sklearn

os.environ["MLFLOW_TRACKING_URI"] = "http://192.168.0.36:5000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://192.168.0.36:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "mladmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mladmin123"

mlflow.set_experiment("Weather Prediction Models")

#Select the best model based on the logged metrics with the highest accuracy
client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("Weather Prediction Models")
runs = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["metrics.accuracy DESC"])
best_run = runs[0]
model_name = best_run.data.tags.get("mlflow.runName", "Best Model")
logger.info(f"Best model selected: {model_name} with Accuracy: {best_run.data.metrics['accuracy']}")
best_model_uri = f"runs:/{best_run.info.run_id}/{model_name}"
best_model = mlflow.sklearn.load_model(best_model_uri)
logger.info(f"Best model loaded successfully from MLflow: {best_model_uri}")

#Deploy the best model on production (for demonstration, we will just print the model details)
logger.info(f"Best Model Details: Run ID: {best_run.info.run_id}, Accuracy: {best_run.data.metrics['accuracy']}, Precision: {best_run.data.metrics['precision']}, Recall: {best_run.data.metrics['recall']}, F1 Score: {best_run.data.metrics['f1_score']}") 

registered_model_name = "weather_prediction_model_production"
result = mlflow.register_model(best_model_uri, registered_model_name)

client.set_registered_model_alias(name=registered_model_name, alias="champion", version=result.version)
logger.info(f"Best model registered and transitioned to Production stage successfully.") 





