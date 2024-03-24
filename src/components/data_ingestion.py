import sys
sys.path.append(r'E:\RECIPE RECOMMENDER MLOPS')
from src.logger.logger import logging
import os
import pandas as pd

class DataIngestion:
    def __init__(self, data_path='raw_data/data.csv'):
        logging.info("Data Ingestion Started")
        self.data_path = data_path

    def read_data(self):
        try:
            self.df = pd.read_csv(self.data_path)
            logging.info(f"Data loaded successfully from {self.data_path}. Shape: {self.df.shape}")
        except Exception as e:
            logging.error(f"Error loading data from {self.data_path}: {str(e)}")

    def process_data(self):
        columns_to_drop = ["TotalTimeInMins", "Cleaned-Ingredients", "Ingredient-count", "Cuisine"]
        try:
            self.new_df = self.df.drop(columns=columns_to_drop)
            self.new_df.rename(columns={
                "TranslatedRecipeName": "title",
                "TranslatedIngredients": "ingredients",
                "TranslatedInstructions": "directions",
                "URL": "link"
            }, inplace=True)
            logging.info(f"Data processed successfully. New shape: {self.new_df.shape}")
        except Exception as e:
            logging.error(f"Error processing data: {str(e)}")

    def save_artifacts(self):
        try:
            artifacts_dir = 'artifacts'
            os.makedirs(artifacts_dir, exist_ok=True)
            output_path = os.path.join(artifacts_dir, 'processed_data.csv')
            self.new_df.to_csv(output_path, index=False)
            logging.info(f"Processed data saved to: {output_path}")
            logging.info("Data Ingestion Completed")
        except Exception as e:
            logging.error(f"Error saving artifacts: {str(e)}")

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.read_data()
    data_ingestion.process_data()
    data_ingestion.save_artifacts()
