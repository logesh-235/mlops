#ML MODEL TRAINING FOR WHETHER PREDICTION
import os
import numpy as np
import pandas as pd
from mlflow.data import from_pandas
import kaggle
from src.utils.logger import logger
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from minio import Minio
import mlflow
import mlflow.sklearn
import datetime
from zoneinfo import ZoneInfo

os.environ["MLFLOW_TRACKING_URI"] = "http://192.168.0.36:5000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://192.168.0.36:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "mladmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mladmin123"

mlflow.set_experiment("Weather Prediction Models")

data = pd.read_csv("dataset/preprocessed_dataset.csv")
logger.info("Dataset loaded successfully.")

# Split the data into training and testing sets
X = data.drop('Rain', axis=1)  # Features
y = data['Rain']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
logger.info("Data split into training and testing sets.")

def train_evaluate_log(model, model_name=None):
    with mlflow.start_run(run_name=f"{model.__class__.__name__}"):
        dataset = from_pandas(data, source="preprocessed_dataset.csv", name=f"Weather Prediction Dataset", digest="train_data")
        mlflow.set_tag("Date and Time", datetime.datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"))
        mlflow.log_input(dataset=dataset)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        mlflow.sklearn.log_model(model, model.__class__.__name__)
        
        
        logger.info(f"{model.__class__.__name__} - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

train_evaluate_log(LogisticRegression())
train_evaluate_log(RandomForestClassifier())
train_evaluate_log(XGBClassifier())

logger.info("Model training and evaluation completed successfully.")





