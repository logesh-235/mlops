import os
import numpy as np
import pandas as pd
from src.utils.logger import logger
from minio import Minio

# Load the dataset from Minio
client = Minio(
    "192.168.0.36:9000",
    access_key="mladmin",
    secret_key="mladmin123",
    secure=False
)

bucket_name = "dataset"
getObjects = client.list_objects(bucket_name, recursive=True)

#Take latest file from the bucket
latest_file = None
latest_time = None
for obj in getObjects:
    if latest_time is None or obj.last_modified > latest_time:
        latest_time = obj.last_modified
        latest_file = obj.object_name
data = pd.read_csv(client.get_object(bucket_name, latest_file))
data.to_csv("dataset/dataset.csv", index=False)
logger.info("Dataset loaded from Minio successfully.")
