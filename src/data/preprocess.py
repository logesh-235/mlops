
from src.utils.logger import logger
from sklearn.preprocessing import LabelEncoder
import pandas as pd


data = pd.read_csv("dataset/dataset.csv")
data = data.dropna()  # Handle missing values

# Encode categorical variables
label_encoder = LabelEncoder()
data['Rain'] = label_encoder.fit_transform(data['Rain'])
data.to_csv("dataset/preprocessed_dataset.csv", index=False)
logger.info("Data preprocessing completed successfully.")
print(data.head())

